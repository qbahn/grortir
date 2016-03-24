"""Module represent single stage in process."""


class AbstractStage:
    """Class represent single stage in process."""

    def __init__(self, input_vector=()):
        """Constructor."""
        self.input_vector = input_vector
        self.control_params = []
        self.output = self.input_vector[:]
