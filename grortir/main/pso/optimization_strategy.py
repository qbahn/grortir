"""Represents optimization strategy for PSO."""


class OptimizationStrategy:
    """Represents optimization strategy for PSO."""

    def get_group_optimization_strategy(self, stages_in_group):
        """
            Return optimization strategy for group.
        Args:
            stages_in_group (list): stages  in group

        Raises:
            NotImplementedError: when method not implemented.
        """
        raise NotImplementedError
