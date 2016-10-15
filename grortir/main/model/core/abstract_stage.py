"""Module represent single stage in process."""
import numpy as np

from grortir.main.model.core.optimization_status import OptimizationStatus


# pylint: disable=too-many-instance-attributes


class AbstractStage:
    """Class represent single stage in process.

    Attributes:
        input_vector (list): initial vector
        optimization_status (OptimizationStatus): status of optimization
        control_params (list): actual control params
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
        dimensions = len(input_vector)
        self.lower_bounds = [-1] * dimensions
        self.upper_bounds = [1] * dimensions
        self.final_output = None
        self.final_quality = None
        self.final_cost = None

    @staticmethod
    def get_cost():
        """Return cost of stage."""
        raise NotImplementedError

    @staticmethod
    def get_quality(input_vector=None, control_params=None):
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

    @staticmethod
    def get_maximal_acceptable_cost():
        """Return maximum acceptable cost."""
        raise NotImplementedError
