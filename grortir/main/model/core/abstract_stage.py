"""Module represent single stage in process."""
import numpy as np
from grortir.main.model.core.optimization_status import OptimizationStatus


class AbstractStage:
    """Class represent single stage in process.

    Attributes:
        input_vector (tuple): initial vector
        optimization_status (OptimizationStatus): status of optimization
        control_params (list): actual control params
        current_vector (list): vector of actual input vector
        lower_bounds (list): lower bounds for control params
        upper_bounds (list): upper bounds for control params

    """

    def __init__(self, input_vector=()):
        """Constructor.

        Args:
            input_vector (tuple): initial vector
        """
        self.input_vector = input_vector
        self.optimization_status = OptimizationStatus.not_started
        self.control_params = np.zeros_like(input_vector)
        self.current_vector = list(self.input_vector)
        dimensions = len(input_vector)
        self.lower_bounds = [0] * dimensions
        self.upper_bounds = [1] * dimensions

    @staticmethod
    def get_cost():
        """Return cost of stage."""
        raise NotImplementedError

    @staticmethod
    def get_quality(control_params=None):
        """Return quality of stage."""
        raise NotImplementedError

    @staticmethod
    def could_be_optimized():
        """Return answer if it is still possible to optimize that stage."""
        raise NotImplementedError

    @staticmethod
    def is_enough_quality(value):
        """Return True if value is enough quality."""
        raise NotImplementedError

    @staticmethod
    def get_output_of_stage():
        """Result of processing input with current control params."""
        raise NotImplementedError
