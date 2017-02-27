"""Represents optimization strategy for PSO."""


class OptimizationStrategy:
    """Represents optimization strategy for PSO."""

    def get_group_optimization_strategy(self, stages_in_group, process):
        """
            Return optimization strategy for group.
        Args:
            process (AbstractProcess): optimized process
            stages_in_group (list): stages  in group

        Raises:
            NotImplementedError: when method not implemented.
        """
        raise NotImplementedError
