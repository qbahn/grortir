"""Contain mechanism for changing position."""

import numpy as np


class PositionUpdater:
    """Class responsible for moving objects.

        Attributes:
            stage (AbstractStage): Stage in which we are going to move.
            control_params (dict): Control params for stages.
    """
    def __init__(self, stage, control_params):
        self.stage = stage
        self.control_params = control_params
        self.lower_bounds = np.asarray(self.stage.lower_bounds)
        self.upper_bounds = np.asarray(self.stage.upper_bounds)

    def set_initial_control_params(self):
        """Set initial positions."""
        random = np.random.rand(len(self.control_params[self.stage]))
        delta = self.upper_bounds - self.lower_bounds
        control_params = self.lower_bounds + random * delta
        self.control_params[self.stage] = control_params.tolist()

    def update_position(self, velocity):
        """Update positions."""
        self.control_params[self.stage] = self.control_params[self.stage] + velocity
        self._fix_coordinates()

    def _fix_coordinates(self):
        for i in range(len(self.control_params[self.stage])):
            if self.control_params[self.stage][i] > self.stage.upper_bounds[i]:
                self.control_params[self.stage][i] = self.stage.upper_bounds[i]
            elif self.control_params[self.stage][i] < self.stage.lower_bounds[i]:
                self.control_params[self.stage][i] = self.stage.lower_bounds[i]
