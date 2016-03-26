"""Module contains class CallsStage."""
from grortir.main.model.core.abstract_stage import AbstractStage


class CallsStage(AbstractStage):
    """Implementation of basic stage.

    Cost is calculated by number of calls of cost function.
    """

    def __init__(self, input_vector=()):
        """Constructor."""
        super().__init__(input_vector)
        self.control_params = [0] * len(self.input_vector)
        self.cost = 0

    def get_quality(self):
        """
        Return quality of actual output.

        :return: quality
        """
        self.cost += 1
        return self.calculate_quality()

    def calculate_quality(self):
        """
        Function for calculating quality.

        :return:
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

        :return: cost
        """
        return self.cost
