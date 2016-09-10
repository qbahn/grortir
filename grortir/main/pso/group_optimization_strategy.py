"""Represents optimization strategy for group in PSO."""


class GroupOptimizationStrategy():
    """Represents optimization strategy for group in PSO."""

    @staticmethod
    def initialize(self):
        raise NotImplementedError

    @staticmethod
    def should_continue(self):
        raise NotImplementedError
