"""
The public facade for the Data Engine module.
"""
import logging
from typing import Optional

from src.data_engine.types import Ticker, DateStr, MarketData
from src.data_engine.config import RAW_DATA_PATH, VALIDATED_DATA_PATH
from src.data_engine.context import PipelineContext

# Pipeline Modules
from src.data_engine.downloaders.yahoo import YahooDownloader
from src.data_engine.standardizers.yahoo import YahooStandardizer
from src.data_engine.storage.parquet import ParquetStorage

from src.data_engine.validators.pipeline import ValidationPipeline
from src.data_engine.validators.price import PriceValidator
from src.data_engine.validators.missing_data import MissingDataValidator
from src.data_engine.validators.duplicate import DuplicateValidator
from src.data_engine.validators.date import DateOrderValidator
from src.data_engine.validators.volume import VolumeValidator

logger = logging.getLogger(__name__)

class DataEngine:
    """
    Orchestrates the immutable ETL pipeline for market data.
    """
    
    def __init__(self):
        # 1. External IO
        self.downloader = YahooDownloader()
        self.raw_storage = ParquetStorage(RAW_DATA_PATH)
        self.validated_storage = ParquetStorage(VALIDATED_DATA_PATH)
        
        # 2. Transformations
        self.standardizer = YahooStandardizer()
        
        # 3. Validations
        self.validator_pipeline = ValidationPipeline([
            PriceValidator(),
            MissingDataValidator(),
            DuplicateValidator(),
            DateOrderValidator(),
            VolumeValidator()
        ])
        
        logger.info("DataEngine initialized with PipelineContext ETL.")
        
    def run_pipeline(self, ticker: Ticker, start: DateStr, end: DateStr) -> PipelineContext:
        """
        Executes the full data pipeline and returns the final context state.
        """
        # Initialize the Context
        ctx = PipelineContext(ticker=ticker, source="Yahoo")
        logger.info(f"--- Starting Pipeline for {ctx.ticker} ---")
        
        try:
            # 1. Download & Save Raw
            ctx.raw_data = self.downloader.fetch_historical(ctx.ticker, start, end)
            self.raw_storage.save(ctx.raw_data, f"{ctx.ticker}_raw")
            
            # 2. Standardize
            ctx.standardized_data = self.standardizer.standardize(ctx.raw_data, ctx.ticker)
            
            # 3. Validate
            _, ctx.validation_report = self.validator_pipeline.run(ctx.standardized_data, ctx.ticker)
            
            # 4. Store Validated (If successful)
            if ctx.validation_report.passed:
                self.validated_storage.save(ctx.standardized_data, ctx.ticker)
                logger.info(f"Pipeline SUCCESS. Score: {ctx.validation_report.quality_score}/100. Time: {ctx.execution_time_ms}ms")
            else:
                logger.warning(f"Pipeline HALTED. Critical validation failures.")
                
            return ctx
            
        except Exception as e:
            logger.error(f"Pipeline FAILED for {ctx.ticker} - {str(e)}")
            ctx.metadata['error'] = str(e)
            return ctx

    def load(self, ticker: Ticker, tier: str = "validated") -> MarketData:
        """Loads data from the specified storage tier."""
        if tier == "raw":
            return self.raw_storage.load(f"{ticker}_raw")
        elif tier == "validated":
            return self.validated_storage.load(ticker)
        else:
            raise ValueError(f"Unknown storage tier: {tier}")