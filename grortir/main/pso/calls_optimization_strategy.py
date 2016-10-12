"""Represents optimization strategy for PSO."""
from grortir.main.pso.calls_group_optimization_strategy import \
    CallsGroupOptimizationStrategy
from grortir.main.pso.optimization_strategy import OptimizationStrategy


class CallsOptimizationStrategy(OptimizationStrategy):
    """Represents optimization strategy Calls stages for PSO."""

    def get_group_optimization_strategy(self, stages_in_group):
        """
            Return group optimization strategy.

        Args:
            stages_in_group (list): list of stages

        Returns:
            CallsGroupOptimizationStrategy: strategy for group optimization.
        """
        return CallsGroupOptimizationStrategy(stages_in_group)
