"""Module represent single stage in process."""


class AbstractStage:
    """Class represent single stage in process."""

    def __init__(self, input_vector=()):
        """Constructor."""
        self.input_vector = input_vector
        self.control_params = []
        self.output_vector = list(self.input_vector)

    def get_cost(self):
        """Return cost of stage."""
        raise NotImplementedError

    def get_quality(self):
        """Return quality of stage."""
        raise NotImplementedError
