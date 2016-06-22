"""Base optimizer."""
import networkx as nx


class BaseOptimizer(object):
    """Optimizer is object which optimize process."""

    def __init__(self, process):
        self.process = process
        self.ordered_stages = nx.topological_sort(self.process)
        self.swarm_size = 40

    def set_custom_optimizing_order(self, ordered_stages):
        """Set custom order.

        Raises:
            ValueError: When order doesn't contain all stages.
        """
        if set(self.ordered_stages) == set(ordered_stages) and len(
                self.ordered_stages) == len(ordered_stages):
            self.ordered_stages = ordered_stages
        else:
            raise ValueError("List of stages must contain all stages.")

    def optimize_process(self):
        """Optimize process.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError
