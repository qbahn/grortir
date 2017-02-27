"""Represents optimization strategy for PSO."""
from grortir.main.pso.credit_calls_group_optimization_strategy import \
    CreditCallsGroupOptimizationStrategy
from grortir.main.pso.optimization_strategy import OptimizationStrategy


class CreditCallsOptimizationStrategy(OptimizationStrategy):
    """Represents optimization strategy Calls stages for PSO."""

    def get_group_optimization_strategy(self, stages_in_group, process):
        """
            Return group optimization strategy.

        Args:
            process (AbstractProcess): optimized process
            stages_in_group (list): list of stages

        Returns:
            CallsGroupOptimizationStrategy: strategy for group optimization.
        """
        return CreditCallsGroupOptimizationStrategy(stages_in_group, process)
