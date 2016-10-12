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

    @staticmethod
    def set_initial_control_params(control_params):
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

    @staticmethod
    def _fix_coordinates(stage, control_params):
        for index, single_param in enumerate(control_params):
            if single_param > stage.upper_bounds[index]:
                control_params[index] = stage.upper_bounds[index]
            elif single_param < stage.lower_bounds[index]:
                control_params[index] = stage.lower_bounds[index]
        return control_params
