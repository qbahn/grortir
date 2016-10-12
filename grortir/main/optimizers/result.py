"""Represents result."""
# pylint: disable=redefined-variable-type
from grortir.main.model.core.optimization_status import OptimizationStatus


class Result(object):
    """Represents result.

        Attributes:
        process (AbstarctProcess): optimized process
    """

    def __init__(self, process):
        self.process = process
        self.summary_result = OptimizationStatus.not_started
        self.detailed_result = {}

    def generate(self):
        """Generate process optimization result."""
        for stage in self.process.nodes():
            self.detailed_result[str(stage)] = stage.optimization_status
        for stage in self.process.nodes():
            if stage.optimization_status != OptimizationStatus.success:
                self.summary_result = OptimizationStatus.failed
                return
        self.summary_result = OptimizationStatus.success
