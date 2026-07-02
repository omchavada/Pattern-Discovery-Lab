"""
The pure processing unit for market data ETL.
"""
import logging

from src.experiment.context import ExperimentContext
from src.data_engine.downloaders.yahoo import YahooDownloader
from src.data_engine.standardizers.yahoo import YahooStandardizer
from src.data_engine.validators.pipeline import ValidationPipeline
from src.data_engine.validators.price import PriceValidator
from src.data_engine.validators.missing_data import MissingDataValidator
from src.data_engine.validators.duplicate import DuplicateValidator
from src.data_engine.validators.date import DateOrderValidator
from src.data_engine.validators.volume import VolumeValidator
from src.data_engine.audit import StepProfiler

logger = logging.getLogger(__name__)

class DataEngine:
    """
    Executes the Download -> Standardize -> Validate pipeline, 
    populating the ExperimentContext. Storage is handled externally.
    """
    
    def __init__(self):
        self.downloader = YahooDownloader()
        self.standardizer = YahooStandardizer()
        
        self.validator_pipeline = ValidationPipeline([
            PriceValidator(),
            MissingDataValidator(),
            DuplicateValidator(),
            DateOrderValidator(),
            VolumeValidator()
        ])
        
        logger.info("DataEngine initialized (Pure Processing Mode).")
        
    def run_pipeline(self, ctx: ExperimentContext, start: str, end: str) -> ExperimentContext:
        """
        Executes the ETL pipeline and populates the provided ExperimentContext.
        """
        try:
            # 1. Download
            with StepProfiler(ctx.audit, "Download"):
                ctx.raw_data = self.downloader.fetch_historical(ctx.ticker, start, end)
            
            # 2. Standardize
            with StepProfiler(ctx.audit, "Standardize"):
                ctx.market_data = self.standardizer.standardize(ctx.raw_data, ctx.ticker)
            
            # 3. Validate
            with StepProfiler(ctx.audit, "Validate"):
                _, ctx.validation_report = self.validator_pipeline.run(ctx.market_data, ctx.ticker)
            
            # 4. Lock in Lineage
            ctx.audit.record_lineage(ctx.market_data)
            
        except Exception as e:
            logger.error(f"DataEngine FAILED for {ctx.ticker} - {str(e)}")
            ctx.metadata['error'] = str(e)
            
        return ctx