"""Module contains class CallsStage."""
from grortir.main.model.core.abstract_stage import AbstractStage


class CallsStage(AbstractStage):
    """Implementation of basic stage.

    Cost is calculated by number of calls of cost function.
    Attributes:
        cost (float): Actual cost of stage.
        max_calls (int): Maximum possible calls of cost quality function
        name (str): Name of stage
    """

    def __init__(self, name, max_calls, input_vector=()):
        """Constructor."""
        super().__init__(input_vector)
        self.max_calls = max_calls
        self.name = name
        self.control_params = [0] * len(self.input_vector)
        self.cost = 0

    def get_quality(self):
        """
        Return quality of actual output.

        Returns:
            quality (float): quality

        """
        self.cost += 1
        return self.calculate_quality()

    def calculate_quality(self):
        """
        Function for calculating quality.

        Returns:
            quality (float): quality

        Raises:
            AssertionError: If length of `control_params`
                is not equal length of `current_vector`
        """
        assert len(self.control_params) == len(self.current_vector)
        quality = 0
        for i in enumerate(self.control_params):
            quality += (self.control_params[i[0]] - self.current_vector[
                i[0]]) ** 2
        return quality

    def get_cost(self):
        """
        Return actual cost of stage.

        Returns:
            cost (float): cost
        """
        return self.cost

    def could_be_optimized(self):
        """Return answer if it is still possible to optimize that stage."""
        return self.get_cost() < self.max_calls
