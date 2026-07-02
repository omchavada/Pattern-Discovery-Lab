"""
Orchestrates the execution of all validation rules.
"""
import logging
from typing import List

from src.data_engine.types import MarketData, Ticker
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import ValidationReport, Severity
from src.data_engine.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ValidationPipeline:
    """Runs a DataFrame through a sequence of BaseValidator rules."""
    
    def __init__(self, validators: List[BaseValidator]):
        self.validators = validators
        
    def run(self, data: MarketData, ticker: Ticker) -> tuple[MarketData, ValidationReport]:
        """
        Executes all validation rules and generates a final report.
        """
        report = ValidationReport(ticker=ticker, total_rows=len(data))
        current_data = data.copy()
        
        for validator in self.validators:
            # Each validator inspects (and potentially cleans) the data
            current_data = validator.validate(current_data, report)
            
            # Fast-fail if a CRITICAL error was just added
            if not report.passed:
                logger.error(f"Validation Pipeline Halted for {ticker}. CRITICAL error in {validator.name}.")
                raise ValidationError(f"Critical data corruption in {ticker}. See report for details.")
                
        logger.info(f"Pipeline complete for {ticker}. Quality Score: {report.quality_score}/100")
        return current_data, report