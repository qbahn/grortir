"""Module which contains CumulatedCallsStage"""
from grortir.main.model.stages.calls_stage import CallsStage


class CumulatedCallsStage(CallsStage):
    """In this class last coordinate of input vector is value which will
    be added  to quality. Other mechanism is the same as in parent class.
    Simply in process we will put as last coordinate in output current quality
    and add this value to quality in children steps."""

    def __init__(self, name, max_calls, input_vector=(),
                 maximum_acceptable_quality=0.01):
        super().__init__(name, max_calls, input_vector,
                         maximum_acceptable_quality)
        self.control_params = [0] * (len(self.input_vector) - 1)
        dimensions = len(self.control_params)
        self.lower_bounds = [-1] * dimensions
        self.upper_bounds = [1] * dimensions

    @staticmethod
    def calculate_quality(input_vector, control_params):
        """Override Calls Stage method - here last coordinate of input is
        simply added to value calculated by remaining coordinates."""
        assert len(input_vector) - 1 == len(control_params)
        return CallsStage.calculate_quality(input_vector[: -1], control_params)

    def get_output_of_stage(self, input_vector, control_params):
        """We return here control params (as in CallsStage) and additionally
        in the last coordinate we put current quality."""
        current_quality = self.calculate_quality(input_vector, control_params)
        function_output = CallsStage.get_output_of_stage(self,
                                                         input_vector[:-1],
                                                         control_params)
        return function_output + [current_quality]
