"""Contain mechanism for changing position."""

import numpy as np


class PositionUpdater:
    """Class responsible for moving objects.

        Attributes:
            stage (AbstractStage): Stage in which we are going to move.
            control_params (dict): Control params for stages.
    """

    def __init__(self, control_params):
        self.control_params = control_params

    def set_initial_control_params(self, control_params):
        """Set initial positions."""
        for stage in control_params:
            random = np.random.rand(len(control_params[stage]))
            delta = np.asarray(stage.upper_bounds) - np.asarray(
                stage.lower_bounds)
            new_control_params = np.asarray(stage.lower_bounds) + random * delta
            control_params[stage] = new_control_params.tolist()
        return control_params

    def update_position(self, velocities, control_params):
        """Update positions."""
        for stage in velocities:
            new_control_params = control_params[stage] + velocities[stage]
            control_params[stage] = self._fix_coordinates(stage,
                                                          new_control_params)
        return control_params

    def _fix_coordinates(self, stage, control_params):
        for i in range(len(control_params)):
            if control_params[i] > stage.upper_bounds[i]:
                control_params[i] = stage.upper_bounds[i]
            elif control_params[i] < stage.lower_bounds[i]:
                control_params[i] = stage.lower_bounds[i]
        return control_params
