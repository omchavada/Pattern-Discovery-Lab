"""
Validates the presence of required data points.
"""
from src.data_engine.types import MarketData
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import ValidationReport, ValidationIssue, Severity

class MissingDataValidator(BaseValidator):
    
    @property
    def name(self) -> str:
        return "MissingDataValidator"

    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        
        # We only check columns that actually exist in the dataframe
        available_cols = [col for col in required_cols if col in data.columns]
        
        missing_mask = data[available_cols].isnull().any(axis=1)
        invalid_rows = missing_mask.sum()
        
        if invalid_rows > 0:
            report.issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    rule_name=self.name,
                    message=f"Found {invalid_rows} rows with missing (NaN) values.",
                    affected_rows=int(invalid_rows)
                )
            )
            
        return data