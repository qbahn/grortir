"""Describe status of optimization."""
from enum import Enum


class OptimizationStatus(Enum):
    """Enum for describing status of optimization.
    not_started - nothing was optimized yet
    in_progress - optimization is in progress
    success - optimization successfully completed
    failed - optimization couldn't be done
    """
    not_started = "Not started"
    success = "Success"
    in_progress = "In progress"
    failed = "Failed"

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == other.value
