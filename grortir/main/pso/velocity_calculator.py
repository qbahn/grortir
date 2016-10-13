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

    @staticmethod
    def calculate_initial_velocity(control_params):
        """Calculate initial velocity."""
        velocities = {}
        for stage in control_params:
            random_factor = np.random.rand(len(control_params[stage]))
            velocity = 0.02 * random_factor - 0.01
            velocities[stage] = velocity
        return velocities

    def calculate(self, current_velocities, particle_best_positions,
                  leader_best_positions,
                  control_params):
        """Calculate velocity."""
        rand_1 = np.random.rand()
        rand_2 = np.random.rand()
        velocities = {}
        for stage in control_params:
            s_0 = self._s0(current_velocities[stage])
            s_1 = self.c_1 * self._s1(rand_1, leader_best_positions[stage],
                                      control_params[stage])
            s_2 = self.c_2 * self._s2(rand_2, particle_best_positions[stage],
                                      control_params[stage])
            velocity = s_0 + s_1 + s_2
            velocities[stage] = velocity
        return velocities

    @staticmethod
    def _s2(random_factor, particle_best_position, control_params):
        return random_factor * (
            np.asarray(particle_best_position) - np.asarray(
                control_params))

    @staticmethod
    def _s1(random_factor, leader_best_position, control_params):
        return random_factor * (
            np.asarray(leader_best_position) - np.asarray(
                control_params))

    def _s0(self, current_velocity):
        return self.w_factor * current_velocity
