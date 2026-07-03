"""
Data structures for validation reporting and severity classification.
"""

from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    INFO = "INFO"  # FYI, no action needed (e.g., "Data starts in 2004")
    WARNING = "WARNING"  # Minor issue, pipeline continues (e.g., "Missing 1 day")
    ERROR = "ERROR"  # Major issue, row might be dropped (e.g., "Duplicate timestamp")
    CRITICAL = "CRITICAL"  # Fatal issue, pipeline halts (e.g., "Negative prices")


@dataclass
class ValidationIssue:
    severity: Severity
    rule_name: str
    message: str
    affected_rows: int = 0


@dataclass
class ValidationReport:
    ticker: str
    total_rows: int
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Returns False if there are ANY Critical errors."""
        return not any(issue.severity == Severity.CRITICAL for issue in self.issues)

    @property
    def quality_score(self) -> float:
        """Calculates a baseline quality score from 0 to 100."""
        if self.total_rows == 0:
            return 0.0

        penalty = 0.0
        for issue in self.issues:
            if issue.severity == Severity.INFO:
                penalty += 0
            elif issue.severity == Severity.WARNING:
                penalty += issue.affected_rows * 0.1
            elif issue.severity == Severity.ERROR:
                penalty += issue.affected_rows * 1.0
            elif issue.severity == Severity.CRITICAL:
                return 0.0  # Instant zero for critical data corruption

        score = 100.0 - ((penalty / self.total_rows) * 100)
        return round(max(0.0, score), 2)
