"""Representation of a particle in swarm."""
# pylint: disable=too-many-instance-attributes
# pylint: disable=redefined-variable-type

import numpy as np

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.pso.position_updater import PositionUpdater
from grortir.main.pso.velocity_calculator import VelocityCalculator


class Particle(object):
    """Implementation of particle."""

    def __init__(self, stages, process):
        self.stages = stages
        self.process = process
        self.position_updaters = {}
        self.velocity_calculators = {}
        self.current_velocities = {}
        self.current_quality = {}
        self.best_quality = np.inf
        self.best_positions = {}
        self.current_control_params = {}
        self.current_input = {}

    def initialize(self):
        """Initialization of single particle."""
        for stage in self.stages:
            self.current_control_params[stage] = stage.control_params
            self.current_input[stage] = stage.input_vector
            self.position_updaters[stage] = PositionUpdater(stage,
                                                            self.current_control_params)
            self.velocity_calculators[stage] = VelocityCalculator()
            stage.optimization_status = OptimizationStatus.in_progress
            self.current_quality[stage] = np.inf
        self._set_initial_positions()
        self._set_initial_velocities()

    def _set_initial_positions(self):
        for stage in self.stages:
            self.position_updaters[stage].set_initial_control_params()

    def _set_initial_velocities(self):
        for stage in self.stages:
            self.current_velocities[stage] = self.velocity_calculators[
                stage].calculate_initial_velocity(
                self.current_control_params[stage])

    def update_values(self):
        """Update values in swarm."""
        self.update_input_vectors()
        self.calculate_current_quality()
        self._update_stages_status()
        self._update_best_position()

    def _update_best_position(self):
        current_quality = self.get_the_overall_quality()
        if current_quality < self.best_quality:
            self.best_quality = current_quality
            for stage in self.stages:
                self.best_positions[stage] = self.current_control_params[stage]

    def update_input_vectors(self):
        """Update input vectors in all stages."""
        for stage in self.stages:
            current_output = stage.get_output_of_stage(
                self.current_input[stage], self.current_control_params[stage])
            successors = self.process.successors(stage)
            for successor in successors:
                successor.input_vector = current_output
                self.current_input[successor] = current_output

    def calculate_current_quality(self):
        """Calculate current quality."""
        for stage in self.stages:
            self.current_quality[stage] = stage.get_quality(self.current_input[stage],
                self.current_control_params[stage])

    def get_the_overall_quality(self):
        """Return overall quality of stages."""
        stage = max(self.current_quality, key=self.current_quality.get)
        return self.current_quality[stage]

    def move(self):
        """Move particle."""
        for stage in self.stages:
            velocity = self.current_velocities[stage]
            self.position_updaters[stage].update_position(velocity)

    def update_velocities(self, best_particle):
        """Update velocities in swarm."""
        for stage in self.stages:
            velocity = self.velocity_calculators[stage].calculate(
                self.best_positions[stage],
                best_particle.best_positions[stage],
                self.current_control_params[stage])
            self.current_velocities[stage] = velocity

    def _update_stages_status(self):
        for stage in self.stages:
            if stage.is_enough_quality(self.current_quality[stage]):
                stage.optimization_status = OptimizationStatus.success
            if not stage.could_be_optimized():
                stage.optimization_status = OptimizationStatus.failed
