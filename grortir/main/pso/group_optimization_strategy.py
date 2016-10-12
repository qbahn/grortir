"""Represents optimization strategy for group in PSO."""


class GroupOptimizationStrategy:
    """Represents optimization strategy for group in PSO."""

    @staticmethod
    def initialize():
        """
        Initialize strategy.

        Raises:
            NotImplementedError: if not  implemented.
        """
        raise NotImplementedError

    @staticmethod
    def should_continue(best_particle):
        """
        Strategic method.

        Args:
            best_particle (Particle): best particle in swarm

        Raises:
            NotImplementedError: if not implemented.
        '"""
        raise NotImplementedError
