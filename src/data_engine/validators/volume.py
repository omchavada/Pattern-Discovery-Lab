"""
Validates trading volume logic.
"""

from src.data_engine.types import MarketData
from src.data_engine.validators.base import BaseValidator
from src.data_engine.validators.report import Severity, ValidationIssue, ValidationReport


class VolumeValidator(BaseValidator):

    @property
    def name(self) -> str:
        return "VolumeValidator"

    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        if "volume" not in data.columns:
            return data

        invalid_vol = data[data["volume"] < 0]
        invalid_rows = len(invalid_vol)

        if invalid_rows > 0:
            report.issues.append(
                ValidationIssue(
                    severity=Severity.CRITICAL,
                    rule_name=self.name,
                    message="Negative volume detected.",
                    affected_rows=invalid_rows,
                )
            )

        return data
