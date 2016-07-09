"""Describe status of optimization."""
from enum import Enum


class OptimizationStatus(Enum):
    """Enum for describing status of optimization."""
    not_started = "Not started"
    success = "Success"
    in_progress = "In progress"
    failed = "Failed"
