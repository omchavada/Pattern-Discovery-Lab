"""
Abstract Base Class for isolated data validation rules.
"""
import abc
from src.data_engine.types import MarketData
from src.data_engine.validators.report import ValidationReport

class BaseValidator(abc.ABC):
    """
    Contract for a single-responsibility validation rule.
    """
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the validation rule."""
        pass
    
    @abc.abstractmethod
    def validate(self, data: MarketData, report: ValidationReport) -> MarketData:
        """
        Inspects the data and appends ValidationIssues to the report.
        Can optionally clean/drop bad rows and return the cleaned DataFrame.
        """
        pass