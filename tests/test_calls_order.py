"""This test is checking that algorithm with grouping is working correctly."""
# pylint: disable=too-many-instance-attributes,too-many-arguments
# pylint: disable=signature-differs,arguments-differ

import unittest.mock as mock
from unittest import TestCase

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm
from tests.framework.calls.calls_registry import CallsRegistry
from tests.framework.calls.input_validator import InputValidator


class TestGroupedOptimizer(TestCase):
    """Class for testing Optimizer."""

    def setUp(self):
        """Set up environment."""
        self.some_process = AbstractProcess()
        self.first_stage = AbstractStage()
        self.second_stage = AbstractStage()
        self.third_stage_a = mock.Mock()
        self.third_stage_b = mock.Mock()
        self.some_process.add_path([self.first_stage, self.second_stage,
                                    self.third_stage_a])
        self.some_process.add_edge(self.second_stage, self.third_stage_b)

    def test___init__(self):
        """Testing creating object."""
        optimizer = GroupedOptimizer(self.some_process, mock.Mock(),
                                     mock.Mock())
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.process, self.some_process)

    def test_calling_functions(self):
        """Test correct order of calling function."""
        optimizer = GroupedOptimizer(TESTED_PROCESS, GROUPING_STRATEGY,
                                     PSO_ALGORITHM)
        optimizer.optimize_process()
        input_validator = InputValidator(CALLS_REGISTRY)
        is_valid = input_validator.validate_input(GROUPING_STRATEGY,
                                                  TESTED_PROCESS)
        self.assertTrue(is_valid)


CALLS_REGISTRY = CallsRegistry()


class DeterministicStage(AbstractStage):
    def __init__(self, name, max_get_output_of_stage_count=10,
                 max_is_enough_quality_count=10,
                 max_could_be_optimized_count=10, max_get_quality_count=10,
                 max_get_cost_count=10):
        super().__init__((0, 0, 0, 0))
        self.name = name
        self.get_cost_count = 0
        self.get_quality_count = 0
        self.could_be_optimized_count = 0
        self.is_enough_quality_count = 0
        self.get_output_of_stage_count = 0
        self.get_maximal_acceptable_cost_count = 0
        self.maximum_acceptable_quality = 1
        self.maximal_acceptable_cost = 100
        self.max_get_cost_count = max_get_cost_count
        self.max_get_quality_count = max_get_quality_count
        self.max_could_be_optimized_count = max_could_be_optimized_count
        self.max_is_enough_quality_count = max_is_enough_quality_count
        self.max_get_output_of_stage_count = max_get_output_of_stage_count
        CALLS_REGISTRY.add_call(self.name, '__init__',
                                [name, max_get_output_of_stage_count,
                                 max_is_enough_quality_count,
                                 max_could_be_optimized_count,
                                 max_get_quality_count,
                                 max_get_cost_count], None, 1)

    def get_cost(self):
        self.get_cost_count += 1
        CALLS_REGISTRY.add_call(self.name, "get_cost", [], self.get_cost_count,
                                self.get_cost_count)
        return self.get_cost_count

    def get_quality(self, input_vector, control_params=None):
        self.get_quality_count += 1
        result = 0.1 if self.get_quality_count > int(self.name) else 1000
        CALLS_REGISTRY.add_call(self.name, "get_quality",
                                [input_vector, control_params], result,
                                self.get_quality_count)
        return result

    def could_be_optimized(self):
        self.could_be_optimized_count += 1
        CALLS_REGISTRY.add_call(self.name, "could_be_optimized", [], True,
                                self.could_be_optimized_count)
        return True

    def is_enough_quality(self, value):
        self.is_enough_quality_count += 1
        result = value < 1
        CALLS_REGISTRY.add_call(self.name, "is_enough_quality", [value], result,
                                self.is_enough_quality_count)
        return result

    def get_output_of_stage(self, input_vector, control_params):
        self.get_output_of_stage_count += 1
        output = [self.get_output_of_stage_count] * len(input_vector)
        output[0] = int(self.name)
        CALLS_REGISTRY.add_call(self.name, "get_output_of_stage",
                                [input_vector, control_params], output,
                                self.get_output_of_stage_count)
        return output

    def get_maximal_acceptable_cost(self):
        self.get_maximal_acceptable_cost_count += 1
        CALLS_REGISTRY.add_call(self.name, "get_maximal_acceptable_cost",
                                [], self.maximal_acceptable_cost,
                                self.get_output_of_stage_count)
        return self.maximal_acceptable_cost


class ExampleProcess(AbstractProcess):
    pass


TESTED_PROCESS = ExampleProcess()
stages = {}
for i in range(7):
    stages[i] = DeterministicStage(str(i))

# Our graph:
#   0
#   |
#   1
#   |\
#   2 4
#   | |\
#   3 5 6
# All edges directed to down
# Order of nodes is the same as names
TESTED_PROCESS.add_edge(stages[0], stages[1])
TESTED_PROCESS.add_edge(stages[1], stages[2])
TESTED_PROCESS.add_edge(stages[2], stages[3])

TESTED_PROCESS.add_edge(stages[1], stages[4])
TESTED_PROCESS.add_edge(stages[4], stages[5])
TESTED_PROCESS.add_edge(stages[4], stages[6])

# Groups:
#   (0)0
#      |
#   (0)1
#      |\
#   (0)2 4(1)
#      | | \
#   (1)3 5(1)6(2)

GROUPING_STRATEGY = GroupingStrategy(list(stages.values()))
GROUPING_STRATEGY.define_group((stages[0], stages[1], stages[2]))
GROUPING_STRATEGY.define_group((stages[3], stages[4], stages[5]))
GROUPING_STRATEGY.define_group((stages[6],))

OPTIMIZATION_STARTEGY = CallsOptimizationStrategy()

PSO_ALGORITHM = PsoAlgorithm(TESTED_PROCESS, GROUPING_STRATEGY,
                             OPTIMIZATION_STARTEGY, 2)
