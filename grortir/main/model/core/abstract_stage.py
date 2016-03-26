"""Module represent single stage in process."""


class AbstractStage:
    """Class represent single stage in process."""

    def __init__(self, input_vector=()):
        """Constructor."""
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
