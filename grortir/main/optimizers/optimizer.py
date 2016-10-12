"""Basic optimizer."""

from grortir.externals.pyswarm.pso import pso
from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.optimizers.base_optimizer import BaseOptimizer


class Optimizer(BaseOptimizer):
    """Optimizer is object which optimize process."""

    def optimize_process(self):
        """Optimize process.
        Raises:
            AttributeError: When project has incorrect structure.

        Returns:
            bool: True if success, False otherwise."""
        for stage in self.ordered_stages:
            if not self.process.predecessors(stage):
                self.run_pso(stage)
            elif len(self.process.predecessors(stage)) == 1:
                predecessor = self.process.predecessors(stage)[0]
                stage.input_vector = predecessor.get_output_of_stage(
                    predecessor.input_vector, predecessor.control_params)
                self.run_pso(stage)
            else:
                raise AttributeError('Incorrect process structure.')

            if stage.optimization_status != OptimizationStatus.success:
                return False
        return True

    def run_pso(self, stage):
        """Run pso with predefined parameters."""
        pso(stage, swarmsize=self.swarm_size)
