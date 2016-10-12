"""Basic grouped optimizer."""

from grortir.main.optimizers.result import Result


class GroupedOptimizer:
    """Optimizer is object which optimize process."""

    def __init__(self, process, grouping_strategy, pso):
        self.process = process
        self.grouping_strategy = grouping_strategy
        self.pso = pso
        self.result = Result(self.process)

    def optimize_process(self):
        """Optimize process.
        Returns:
            True if success, False otherwise."""
        self.pso.run()
        self.result.generate()
