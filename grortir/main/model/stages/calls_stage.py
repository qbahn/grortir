"""Module contains class CallsStage."""
from grortir.main.model.core.abstract_stage import AbstractStage


# pylint: disable=arguments-differ,unused-argument


class CallsStage(AbstractStage):
    """Implementation of basic stage.

    Cost is calculated by number of calls of cost function.
    Attributes:
        cost (float): Actual cost of stage.
        max_calls (int): Maximum possible calls of cost quality function
        name (str): Name of stage
        maximum_acceptable_quality (float): max expected quality
    """

    def __init__(self, name, max_calls, input_vector=(),
                 maximum_acceptable_quality=0.01):
        """Constructor."""
        super().__init__(input_vector)
        self.max_calls = max_calls
        self.name = name
        self.control_params = [0] * len(self.input_vector)
        self.maximum_acceptable_quality = maximum_acceptable_quality
        self.cost = 0

    def get_quality(self, input_vector=None, control_params=None):
        """
        Return quality of actual output.

        Returns:
            float: quality

        """
        if control_params is None:
            control_params = self.control_params[:]
        self.cost += 1
        return self.calculate_quality(input_vector, control_params)

    @staticmethod
    def calculate_quality(input_vector, control_params):
        """
        Function for calculating quality.

        Returns:
            float: quality

        Raises:
            AssertionError: If length of `control_params`
                is not equal length of `input_vector`
        """
        assert len(control_params) == len(input_vector)
        quality = 0
        for i in enumerate(control_params):
            quality += (control_params[i[0]] - input_vector[
                i[0]]) ** 2
        return quality

    def get_cost(self):
        """
        Return actual cost of stage.

        Returns:
            float: cost
        """
        return self.cost

    def could_be_optimized(self):
        """Return answer if it is still possible to optimize that stage."""
        return self.get_cost() < self.get_maximal_acceptable_cost()

    def is_enough_quality(self, value):
        """Return True if value is proper quality."""
        return value <= self.maximum_acceptable_quality

    def get_output_of_stage(self, input_vector, control_params):
        """Return output of stage."""
        return control_params

    def get_maximal_acceptable_cost(self):
        """Return maximum acceptable cost."""
        return self.max_calls

    def __str__(self):
        return self.name
