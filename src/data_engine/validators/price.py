"""
Validates standard OHLC price logic.
"""
from src.data_engine.types import MarketData
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import ValidationReport, ValidationIssue, Severity

class PriceValidator(BaseValidator):
    
    @property
    def name(self) -> str:
        return "PriceLogicValidator"

    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        # Check 1: Negative Prices
        if not (data[['open', 'high', 'low', 'close']] >= 0).all().all():
            invalid_rows = len(data[~((data[['open', 'high', 'low', 'close']] >= 0).all(axis=1))])
            report.issues.append(
                ValidationIssue(
                    severity=Severity.CRITICAL,
                    rule_name=self.name,
                    message="Negative prices detected.",
                    affected_rows=invalid_rows
                )
            )
            
        # Check 2: High/Low Logic
        invalid_hl = data[data['high'] < data['low']]
        if not invalid_hl.empty:
            report.issues.append(
                ValidationIssue(
                    severity=Severity.CRITICAL,
                    rule_name=self.name,
                    message="High price is lower than Low price.",
                    affected_rows=len(invalid_hl)
                )
            )
            
        return data