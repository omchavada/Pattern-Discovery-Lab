"""
Validates chronological order of the dataset.
"""
from src.data_engine.types import MarketData
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import ValidationReport, ValidationIssue, Severity

class DateOrderValidator(BaseValidator):
    
    @property
    def name(self) -> str:
        return "DateOrderValidator"

    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        if 'date' not in data.columns or len(data) < 2:
            return data
            
        # Check if dates are strictly monotonically increasing
        is_sorted = data['date'].is_monotonic_increasing
        
        if not is_sorted:
            report.issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    rule_name=self.name,
                    message="Dates are not in strictly ascending chronological order.",
                    affected_rows=len(data)  # Affects the whole dataset's temporal integrity
                )
            )
            
        return data