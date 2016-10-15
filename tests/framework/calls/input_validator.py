"""Validator for input."""
from grortir.main.model.core.abstract_stage import AbstractStage
from tests.framework.calls.calls_registry import CallsRegistry


class InputValidator:
    """
        Attributes:
            calls_registry (CallsRegistry): calls registry
    """

    def __init__(self, calls_registry: CallsRegistry):
        """

        Args:
            calls_registry (CallsRegistry): registry of calls
        """
        self.calls_registry = calls_registry

    def validate_input(self, grouping_strategy, process):
        """
        Validate if input in stage successors are the same as output in stage.

        Args:
            grouping_strategy (GroupingStrategy): grouping strategy
            process (AbstractProcess): validated process
        Returns:
            bool: True if inputs are valid
        """
        all_stages = process.nodes()
        for stage in all_stages:
            groupies = grouping_strategy.get_items_from_the_same_group(stage)
            for successor in process.successors(stage):
                if successor in groupies:
                    result = self._validate_for_groupies(stage, successor)
                else:
                    result = self._validate_for_non_groupies(stage, successor)
                if result is False:
                    return False
        return True

    def _validate_for_groupies(self, stage, successor):
        stage_outputs = self.calls_registry. \
            get_method_calls(stage.name, "get_output_of_stage")
        successor_inputs = self.calls_registry. \
            get_method_calls(successor.name, "get_quality")
        output_values = []
        inputs = []
        for stage_output in stage_outputs:
            output_values.append(stage_output['call'].output)

        for successor_input in successor_inputs:
            inputs.append(successor_input['call'].input_parms_list[0])
        print("aa")
        return output_values == inputs

    def _validate_for_non_groupies(self, stage: AbstractStage, successor):
        stage_outputs = self.calls_registry. \
            get_method_calls(stage.name, "get_output_of_stage")
        successor_inputs = self.calls_registry. \
            get_method_calls(successor.name, "get_quality")
        print("bb")
        if len(stage_outputs) == 0:
            return len(successor_inputs) == 0
        else:
            last_output = stage_outputs[-1]['call'].output
            first_input = successor_inputs[0]['call'].input_parms_list[0]
            return last_output == first_input
