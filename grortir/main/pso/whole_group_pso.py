"""Contains WholeGroupPso class."""
from grortir.main.pso.optimization_controller import OptimizationController
from grortir.main.pso.swarm import Swarm

from grortir.main.pso.swarm import Swarm


class WholeGroupPso(object):
    """Optimize whole group."""

    def __init__(self, process, number_of_particles):
        self.process = process
        self.number_of_particles = number_of_particles

    def optimize(self, ordered_stages_to_optimize):
        """Optimize whole group of stages.

            Parameters:
                ordered_stages_to_optimize (list): List of stages which need
                 to be optimized
        """
        swarm = Swarm(self.process, ordered_stages_to_optimize,
                      self.number_of_particles)
        swarm.initialize()
        while OptimizationController.should_continue(
                ordered_stages_to_optimize):
            swarm.do_single_iteration()
