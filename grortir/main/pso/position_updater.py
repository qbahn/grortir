"""Contain mechanism for changing position."""

import numpy as np


class PositionUpdater:
    """Class responsible for moving objects.

        Attributes:
            stage (AbstractStage): Stage in which we are going to move.
    """
    def __init__(self, stage):
        self.stage = stage
        self.lower_bounds = np.asarray(self.stage.lower_bounds)
        self.upper_bounds = np.asarray(self.stage.upper_bounds)

    def set_initial_control_params(self):
        """Set initial positions."""
        random = np.random.rand(len(self.stage.control_params))
        delta = self.upper_bounds - self.lower_bounds
        control_params = self.lower_bounds + random * delta
        self.stage.control_params = control_params.tolist()

    def update_position(self, velocity):
        """Update positions."""
        self.stage.control_params = self.stage.control_params + velocity
        self._fix_coordinates()

    def _fix_coordinates(self):
        for i in range(len(self.stage.control_params)):
            if self.stage.control_params[i] > self.stage.upper_bounds[i]:
                self.stage.control_params[i] = self.stage.upper_bounds[i]
            elif self.stage.control_params[i] < self.stage.lower_bounds[i]:
                self.stage.control_params[i] = self.stage.lower_bounds[i]
