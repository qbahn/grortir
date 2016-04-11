"""Module represent single stage in process."""


class AbstractStage:
    """Class represent single stage in process.

    Attributes:
        input_vector (tuple): initial vector
        control_params (list): actual control params
        current_vector (list): vector of actual input vector

    """

    def __init__(self, input_vector=()):
        """Constructor.

        Args:
            input_vector (tuple): initial vector
        """
        self.input_vector = input_vector
        self.control_params = []
        self.current_vector = list(self.input_vector)

    @staticmethod
    def get_cost():
        """Return cost of stage."""
        raise NotImplementedError

    @staticmethod
    def get_quality():
        """Return quality of stage."""
        raise NotImplementedError

    @staticmethod
    def could_be_optimized():
        """Return answer if it is still possible to optimize that stage."""
        raise NotImplementedError
