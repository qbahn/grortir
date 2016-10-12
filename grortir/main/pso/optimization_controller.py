"""Contains optimization controller."""
from grortir.main.model.core.optimization_status import OptimizationStatus


class OptimizationController(object):
    """Controller for optimization process."""

    @staticmethod
    def should_continue(stages):
        """Return true only if optimization should be continued."""
        for stage in stages:
            if OptimizationStatus.failed == stage.optimization_status:
                return False
        for stage in stages:
            if OptimizationStatus.success != stage.optimization_status:
                return True
        return False
