"""Basic optimizer."""
import networkx as nx

from grortir.externals.pyswarm.pso import pso
from grortir.main.model.core.optimization_status import OptimizationStatus


class Optimizer(object):
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
        for stage in self.ordered_stages:
            if not self.process.predecessors(stage):
                self.run_pso(stage)
            elif len(self.process.predecessors(stage)) == 1:
                predecessor = self.process.predecessors(stage)[0]
                stage.input_vector = predecessor.get_output_of_stage()
                self.run_pso(stage)
            else:
                raise AttributeError('Incorrect process structure.')

            if stage.optimization_status != OptimizationStatus.success:
                return False
        return True

    def run_pso(self, stage):
        """Run pso with predefined parameters."""
        pso(stage, swarmsize=self.swarm_size)
