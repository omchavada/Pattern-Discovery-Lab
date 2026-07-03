"""
Custom exceptions for the Data Engine module.
"""


class DataEngineError(Exception):
    """Base exception for all Data Engine errors."""

    pass


class DataDownloadError(DataEngineError):
    """Raised when data cannot be fetched from the source."""

    pass


class InvalidTickerError(DataEngineError):
    """Raised when a ticker symbol is unrecognized or malformed."""

    pass


class ValidationError(DataEngineError):
    """Raised when data fails quality checks (e.g., missing rows)."""

    pass


class StorageError(DataEngineError):
    """Raised when data cannot be read from or written to disk/DB."""

    pass
