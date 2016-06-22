"""Contains things related to calculating velocity."""

import numpy as np


class VelocityCalculator:
    """Calculate Velocity for single stage.

    Attributes:
        current_velocity (list) : list of coordinates of speed for current stage
        """

    def __init__(self, stage):
        self.stage = stage
        self.c_1 = 0.5
        self.c_2 = 0.5
        self.w_factor = 0.8
        self.current_velocity = None

    def calculate_initial_velocity(self):
        """Calculate initial velocity."""
        velocity = 0.02 * np.random.rand(len(self.stage.control_params)) - 0.01
        self.current_velocity = velocity
        return velocity

    def calculate(self, particle_best_position, leader_best_position):
        """Calculate velocity."""
        velocity = self._s0() + self.c_1 * self._s1(
            leader_best_position) + self.c_2 * self._s2(particle_best_position)
        self.current_velocity = velocity
        return velocity

    def _s2(self, particle_best_position):
        return np.random.rand(len(self.stage.control_params)) * (
            np.asarray(particle_best_position) - np.asarray(
                self.stage.control_params))

    def _s1(self, leader_best_position):
        return np.random.rand(len(self.stage.control_params)) * (
            np.asarray(leader_best_position) - np.asarray(
                self.stage.control_params))

    def _s0(self):
        return self.w_factor * self.current_velocity
