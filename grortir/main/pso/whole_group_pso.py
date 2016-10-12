"""Contains WholeGroupPso class."""

from grortir.main.pso.swarm import Swarm


class WholeGroupPso(object):
    """Optimize whole group."""

    def __init__(self, process, number_of_particles):
        self.process = process
        self.number_of_particles = number_of_particles

    def optimize(self, ordered_stages_to_optimize, group_optimization_strategy):
        """Optimize whole group of stages.

         Parameters:
            group_optimization_strategy (GroupOptimizationStrategy):
                strategy for optimizing groups
            ordered_stages_to_optimize (list): List of stages which need
                 to be optimized
        """
        swarm = Swarm(self.process, ordered_stages_to_optimize,
                      self.number_of_particles)
        swarm.initialize()
        group_optimization_strategy.initialize()
        while group_optimization_strategy.should_continue(swarm.best_particle):
            swarm.do_single_iteration()
        swarm.post_processing()
        print("Optimization for group finished.")
