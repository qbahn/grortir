"""Represents swarm."""
import logging

import numpy as np

from grortir.main.pso.particle import Particle

LOG = logging.getLogger(__name__)


class Swarm(object):
    """Class which represent swarm."""

    def __init__(self, process, stages, number_of_particles):
        self.stages = stages
        self.process = process
        self.number_of_particles = number_of_particles
        self.particles = [Particle(stages, self.process, i) for i in
                          range(number_of_particles)]
        self.best_particle_quality = np.inf
        self.best_particle = self.particles[0]
        LOG.debug('Swarm created.')

    def initialize(self):
        """Initialize all particles in swarm."""
        LOG.debug('Initialize swarm.')
        for particle in self.particles:
            particle.initialize()

    def do_single_iteration(self):
        """Iterate one time."""
        for particle in self.particles:
            particle.update_values()
        self._update_best_particle()
        self._update_velocieties()
        for particle in self.particles:
            particle.move()

    def _update_best_particle(self):
        for particle in self.particles:
            if particle.best_quality < self.best_particle_quality:
                LOG.debug('Update best particle.')
                self.best_particle = particle
                self.best_particle_quality = particle.best_quality
                LOG.debug('Current best quality is: ' + str(
                    self.best_particle_quality))
        LOG.debug('The best particle is: ' + str(self.best_particle.number))

    def _update_velocieties(self):
        for particle in self.particles:
            particle.update_velocities(self.best_particle)

    def post_processing(self):
        """Method which should be done after all iterations."""
        best_control_params = self.best_particle.best_positions
        # calculate output:
        for stage in self.stages:
            current_output = stage.get_output_of_stage(
                stage.input_vector, best_control_params[stage])
            successors = self.process.successors(stage)
            for successor in successors:
                successor.input_vector = current_output
            stage.final_output = current_output
            stage.final_cost = stage.get_cost()
            stage.final_quality = stage.get_quality(
                stage.input_vector, best_control_params[stage])
            LOG.debug('Final stage status: ' + str(stage))
