"""
Validates temporal uniqueness (no duplicate dates).
"""
from src.data_engine.types import MarketData
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import ValidationReport, ValidationIssue, Severity

class DuplicateValidator(BaseValidator):
    
    @property
    def name(self) -> str:
        return "DuplicateDateValidator"

    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        if 'date' not in data.columns:
            return data
            
        duplicates = data.duplicated(subset=['date'], keep=False)
        invalid_rows = duplicates.sum()
        
        if invalid_rows > 0:
            report.issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    rule_name=self.name,
                    message="Duplicate trading dates detected.",
                    affected_rows=int(invalid_rows)
                )
            )
            
        return data