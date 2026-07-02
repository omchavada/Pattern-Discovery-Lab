"""
Defines the strictly enforced lifecycle states of a research experiment.
"""
from enum import Enum

class ExperimentState(Enum):
    CREATED = "CREATED"           # ID generated, folders created
    RUNNING = "RUNNING"           # Data pipeline executing
    VALIDATING = "VALIDATING"     # Quality checks executing
    COMPLETED = "COMPLETED"       # Successfully finished and tracked
    FAILED = "FAILED"             # Halted due to critical errors