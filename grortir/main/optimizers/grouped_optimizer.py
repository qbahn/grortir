"""Basic grouped optimizer."""
import networkx as nx


class GroupedOptimizer(object):
    """Optimizer is object which optimize process."""

    def __init__(self, process):
        self.process = process
        self.ordered_stages = nx.topological_sort(self.process)
        self.swarm_size = 40

    def set_custom_optimizing_order(self, ordered_stages):
        """Set custom order."""
        if set(self.ordered_stages) == set(ordered_stages) and len(
                self.ordered_stages) == len(ordered_stages):
            self.ordered_stages = ordered_stages
        else:
            raise ValueError("List of stages must contain all stages.")

    def optimize_process(self):
        """Optimize process.
        Returns:
            True if success, False otherwise."""
        pass
