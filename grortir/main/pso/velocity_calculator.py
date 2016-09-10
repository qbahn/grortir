"""Contains things related to calculating velocity."""

import numpy as np


class VelocityCalculator:
    """Calculate Velocity for a single stage.

    Attributes:
        current_velocity (list) : list of coordinates of speed for current stage
        """

    def __init__(self):
        self.c_1 = 1
        self.c_2 = 1
        self.w_factor = 0.8
        self.current_velocity = None

    def calculate_initial_velocity(self, control_params):
        """Calculate initial velocity."""
        velocity = 0.02 * np.random.rand(len(control_params)) - 0.01
        self.current_velocity = velocity
        return velocity

    def calculate(self, particle_best_position, leader_best_position,
                  control_params):
        """Calculate velocity."""
        s0 = self._s0()
        s1 = self.c_1 * self._s1(leader_best_position, control_params)
        s2 = self.c_2 * self._s2(particle_best_position, control_params)
        velocity = s0 + s1 + s2
        self.current_velocity = velocity
        return velocity

    def _s2(self, particle_best_position, control_params):
        return np.random.rand(len(control_params)) * (
            np.asarray(particle_best_position) - np.asarray(
                control_params))

    def _s1(self, leader_best_position, control_params):
        return np.random.rand(len(control_params)) * (
            np.asarray(leader_best_position) - np.asarray(
                control_params))

    def _s0(self):
        return self.w_factor * self.current_velocity
