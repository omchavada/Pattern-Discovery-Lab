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
        Executes the full data pipeline with strict audit profiling.
        """
        ctx = PipelineContext(ticker=ticker, source="Yahoo")
        from src.data_engine.audit import StepProfiler # Ensure this is imported at top
        
        logger.info(f"--- Starting Profiled Pipeline for {ctx.ticker} ---")
        
        try:
            # 1. Download & Save Raw
            with StepProfiler(ctx.audit, "Download"):
                ctx.raw_data = self.downloader.fetch_historical(ctx.ticker, start, end)
                
            with StepProfiler(ctx.audit, "Store_Raw"):
                self.raw_storage.save(ctx.raw_data, f"{ctx.ticker}_raw")
            
            # 2. Standardize (Now creating market_data)
            with StepProfiler(ctx.audit, "Standardize"):
                ctx.market_data = self.standardizer.standardize(ctx.raw_data, ctx.ticker)
            
            # 3. Validate
            with StepProfiler(ctx.audit, "Validate"):
                _, ctx.validation_report = self.validator_pipeline.run(ctx.market_data, ctx.ticker)
            
            # 4. Store Validated & Finalize Audit
            with StepProfiler(ctx.audit, "Store_Validated"):
                if ctx.validation_report.passed:
                    self.validated_storage.save(ctx.market_data, ctx.ticker)
                    
            # Lock in the cryptographic lineage
            ctx.audit.record_lineage(ctx.market_data)
            
            logger.info(
                f"Pipeline SUCCESS. Score: {ctx.validation_report.quality_score}/100. "
                f"Total Time: {ctx.audit.total_execution_ms}ms"
            )
            return ctx
            
        except Exception as e:
            logger.error(f"Pipeline FAILED for {ctx.ticker} - {str(e)}")
            ctx.metadata['error'] = str(e)
            return ctx