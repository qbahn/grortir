"""Module for testing grouped optimizer."""

from unittest import TestCase

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm

import unittest.mock as mock


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
        optimizer = GroupedOptimizer(self.some_process, mock.Mock(), mock.Mock())
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.process, self.some_process)

    def test_calling_functions(self):
        """Test correct order of calling function."""
        optimizer = GroupedOptimizer(TESTED_PROCESS, GROUPING_STRATEGY,
                                     PSO_ALGORITHM)
        expected_calls = [mock.call.method_name('0', '__init__'),
                          mock.call.method_name('1', '__init__'),
                          mock.call.method_name('2', '__init__'),
                          mock.call.method_name('3', '__init__'),
                          mock.call.method_name('4', '__init__'),
                          mock.call.method_name('5', '__init__'),
                          mock.call.method_name('6', '__init__'),
                          mock.call.method_name('0', 'get_output_of_stage', 1),
                          mock.call.method_name('1', 'get_output_of_stage', 1),
                          mock.call.method_name('2', 'get_output_of_stage', 1),
                          mock.call.method_name('0', 'get_quality', 1),
                          mock.call.method_name('1', 'get_quality', 1),
                          mock.call.method_name('2', 'get_quality', 1),
                          mock.call.method_name('0', 'is_enough_quality', 1),
                          mock.call.method_name('0', 'could_be_optimized', 1),
                          mock.call.method_name('1', 'is_enough_quality', 1),
                          mock.call.method_name('1', 'could_be_optimized', 1),
                          mock.call.method_name('2', 'is_enough_quality', 1),
                          mock.call.method_name('2', 'could_be_optimized', 1),
                          mock.call.method_name('0', 'get_output_of_stage', 2),
                          mock.call.method_name('1', 'get_output_of_stage', 2),
                          mock.call.method_name('2', 'get_output_of_stage', 2),
                          mock.call.method_name('0', 'get_quality', 2),
                          mock.call.method_name('1', 'get_quality', 2),
                          mock.call.method_name('2', 'get_quality', 2),
                          mock.call.method_name('0', 'is_enough_quality', 2),
                          mock.call.method_name('0', 'could_be_optimized', 2),
                          mock.call.method_name('1', 'is_enough_quality', 2),
                          mock.call.method_name('1', 'could_be_optimized', 2),
                          mock.call.method_name('2', 'is_enough_quality', 2),
                          mock.call.method_name('2', 'could_be_optimized', 2),
                          mock.call.method_name('0', 'get_output_of_stage', 3),
                          mock.call.method_name('1', 'get_output_of_stage', 3),
                          mock.call.method_name('2', 'get_output_of_stage', 3),
                          mock.call.method_name('0', 'get_quality', 3),
                          mock.call.method_name('1', 'get_quality', 3),
                          mock.call.method_name('2', 'get_quality', 3),
                          mock.call.method_name('0', 'is_enough_quality', 3),
                          mock.call.method_name('0', 'could_be_optimized', 3),
                          mock.call.method_name('1', 'is_enough_quality', 3),
                          mock.call.method_name('1', 'could_be_optimized', 3),
                          mock.call.method_name('2', 'is_enough_quality', 3),
                          mock.call.method_name('2', 'could_be_optimized', 3),
                          mock.call.method_name('0', 'get_output_of_stage', 4),
                          mock.call.method_name('1', 'get_output_of_stage', 4),
                          mock.call.method_name('2', 'get_output_of_stage', 4),
                          mock.call.method_name('0', 'get_quality', 4),
                          mock.call.method_name('1', 'get_quality', 4),
                          mock.call.method_name('2', 'get_quality', 4),
                          mock.call.method_name('0', 'is_enough_quality', 4),
                          mock.call.method_name('0', 'could_be_optimized', 4),
                          mock.call.method_name('1', 'is_enough_quality', 4),
                          mock.call.method_name('1', 'could_be_optimized', 4),
                          mock.call.method_name('2', 'is_enough_quality', 4),
                          mock.call.method_name('2', 'could_be_optimized', 4),
                          mock.call.method_name('0', 'get_output_of_stage', 5),
                          mock.call.method_name('1', 'get_output_of_stage', 5),
                          mock.call.method_name('2', 'get_output_of_stage', 5),
                          mock.call.method_name('0', 'get_quality', 5),
                          mock.call.method_name('1', 'get_quality', 5),
                          mock.call.method_name('2', 'get_quality', 5),
                          mock.call.method_name('0', 'is_enough_quality', 5),
                          mock.call.method_name('0', 'could_be_optimized', 5),
                          mock.call.method_name('1', 'is_enough_quality', 5),
                          mock.call.method_name('1', 'could_be_optimized', 5),
                          mock.call.method_name('2', 'is_enough_quality', 5),
                          mock.call.method_name('2', 'could_be_optimized', 5),
                          mock.call.method_name('0', 'get_output_of_stage', 6),
                          mock.call.method_name('1', 'get_output_of_stage', 6),
                          mock.call.method_name('2', 'get_output_of_stage', 6),
                          mock.call.method_name('0', 'get_quality', 6),
                          mock.call.method_name('1', 'get_quality', 6),
                          mock.call.method_name('2', 'get_quality', 6),
                          mock.call.method_name('0', 'is_enough_quality', 6),
                          mock.call.method_name('0', 'could_be_optimized', 6),
                          mock.call.method_name('1', 'is_enough_quality', 6),
                          mock.call.method_name('1', 'could_be_optimized', 6),
                          mock.call.method_name('2', 'is_enough_quality', 6),
                          mock.call.method_name('2', 'could_be_optimized', 6),
                          mock.call.method_name('3', 'get_output_of_stage', 1),
                          mock.call.method_name('4', 'get_output_of_stage', 1),
                          mock.call.method_name('5', 'get_output_of_stage', 1),
                          mock.call.method_name('3', 'get_quality', 1),
                          mock.call.method_name('4', 'get_quality', 1),
                          mock.call.method_name('5', 'get_quality', 1),
                          mock.call.method_name('3', 'is_enough_quality', 1),
                          mock.call.method_name('3', 'could_be_optimized', 1),
                          mock.call.method_name('4', 'is_enough_quality', 1),
                          mock.call.method_name('4', 'could_be_optimized', 1),
                          mock.call.method_name('5', 'is_enough_quality', 1),
                          mock.call.method_name('5', 'could_be_optimized', 1),
                          mock.call.method_name('3', 'get_output_of_stage', 2),
                          mock.call.method_name('4', 'get_output_of_stage', 2),
                          mock.call.method_name('5', 'get_output_of_stage', 2),
                          mock.call.method_name('3', 'get_quality', 2),
                          mock.call.method_name('4', 'get_quality', 2),
                          mock.call.method_name('5', 'get_quality', 2),
                          mock.call.method_name('3', 'is_enough_quality', 2),
                          mock.call.method_name('3', 'could_be_optimized', 2),
                          mock.call.method_name('4', 'is_enough_quality', 2),
                          mock.call.method_name('4', 'could_be_optimized', 2),
                          mock.call.method_name('5', 'is_enough_quality', 2),
                          mock.call.method_name('5', 'could_be_optimized', 2),
                          mock.call.method_name('3', 'get_output_of_stage', 3),
                          mock.call.method_name('4', 'get_output_of_stage', 3),
                          mock.call.method_name('5', 'get_output_of_stage', 3),
                          mock.call.method_name('3', 'get_quality', 3),
                          mock.call.method_name('4', 'get_quality', 3),
                          mock.call.method_name('5', 'get_quality', 3),
                          mock.call.method_name('3', 'is_enough_quality', 3),
                          mock.call.method_name('3', 'could_be_optimized', 3),
                          mock.call.method_name('4', 'is_enough_quality', 3),
                          mock.call.method_name('4', 'could_be_optimized', 3),
                          mock.call.method_name('5', 'is_enough_quality', 3),
                          mock.call.method_name('5', 'could_be_optimized', 3),
                          mock.call.method_name('3', 'get_output_of_stage', 4),
                          mock.call.method_name('4', 'get_output_of_stage', 4),
                          mock.call.method_name('5', 'get_output_of_stage', 4),
                          mock.call.method_name('3', 'get_quality', 4),
                          mock.call.method_name('4', 'get_quality', 4),
                          mock.call.method_name('5', 'get_quality', 4),
                          mock.call.method_name('3', 'is_enough_quality', 4),
                          mock.call.method_name('3', 'could_be_optimized', 4),
                          mock.call.method_name('4', 'is_enough_quality', 4),
                          mock.call.method_name('4', 'could_be_optimized', 4),
                          mock.call.method_name('5', 'is_enough_quality', 4),
                          mock.call.method_name('5', 'could_be_optimized', 4),
                          mock.call.method_name('3', 'get_output_of_stage', 5),
                          mock.call.method_name('4', 'get_output_of_stage', 5),
                          mock.call.method_name('5', 'get_output_of_stage', 5),
                          mock.call.method_name('3', 'get_quality', 5),
                          mock.call.method_name('4', 'get_quality', 5),
                          mock.call.method_name('5', 'get_quality', 5),
                          mock.call.method_name('3', 'is_enough_quality', 5),
                          mock.call.method_name('3', 'could_be_optimized', 5),
                          mock.call.method_name('4', 'is_enough_quality', 5),
                          mock.call.method_name('4', 'could_be_optimized', 5),
                          mock.call.method_name('5', 'is_enough_quality', 5),
                          mock.call.method_name('5', 'could_be_optimized', 5),
                          mock.call.method_name('3', 'get_output_of_stage', 6),
                          mock.call.method_name('4', 'get_output_of_stage', 6),
                          mock.call.method_name('5', 'get_output_of_stage', 6),
                          mock.call.method_name('3', 'get_quality', 6),
                          mock.call.method_name('4', 'get_quality', 6),
                          mock.call.method_name('5', 'get_quality', 6),
                          mock.call.method_name('3', 'is_enough_quality', 6),
                          mock.call.method_name('3', 'could_be_optimized', 6),
                          mock.call.method_name('4', 'is_enough_quality', 6),
                          mock.call.method_name('4', 'could_be_optimized', 6),
                          mock.call.method_name('5', 'is_enough_quality', 6),
                          mock.call.method_name('5', 'could_be_optimized', 6),
                          mock.call.method_name('6', 'get_output_of_stage', 1),
                          mock.call.method_name('6', 'get_quality', 1),
                          mock.call.method_name('6', 'is_enough_quality', 1),
                          mock.call.method_name('6', 'could_be_optimized', 1),
                          mock.call.method_name('6', 'get_output_of_stage', 2),
                          mock.call.method_name('6', 'get_quality', 2),
                          mock.call.method_name('6', 'is_enough_quality', 2),
                          mock.call.method_name('6', 'could_be_optimized', 2),
                          mock.call.method_name('6', 'get_output_of_stage', 3),
                          mock.call.method_name('6', 'get_quality', 3),
                          mock.call.method_name('6', 'is_enough_quality', 3),
                          mock.call.method_name('6', 'could_be_optimized', 3),
                          mock.call.method_name('6', 'get_output_of_stage', 4),
                          mock.call.method_name('6', 'get_quality', 4),
                          mock.call.method_name('6', 'is_enough_quality', 4),
                          mock.call.method_name('6', 'could_be_optimized', 4),
                          mock.call.method_name('6', 'get_output_of_stage', 5),
                          mock.call.method_name('6', 'get_quality', 5),
                          mock.call.method_name('6', 'is_enough_quality', 5),
                          mock.call.method_name('6', 'could_be_optimized', 5),
                          mock.call.method_name('6', 'get_output_of_stage', 6),
                          mock.call.method_name('6', 'get_quality', 6),
                          mock.call.method_name('6', 'is_enough_quality', 6),
                          mock.call.method_name('6', 'could_be_optimized', 6)]
        optimizer.optimize_process()
        self.assertListEqual(CALLS_COUNTER.method_calls, expected_calls)


CALLS_COUNTER = mock.Mock(name="CallsCounter")


class DeterministicStage(AbstractStage):
    def __init__(self, name, max_get_output_of_stage_count=10,
                 max_is_enough_quality_count=10,
                 max_could_be_optimized_count=10, max_get_quality_count=10,
                 max_get_cost_count=10):
        super().__init__((0, 0, 0, 0))
        self.name = name
        CALLS_COUNTER.method_name(self.name, "__init__")
        self.get_cost_count = 0
        self.get_quality_count = 0
        self.could_be_optimized_count = 0
        self.is_enough_quality_count = 0
        self.get_output_of_stage_count = 0
        self.max_get_cost_count = max_get_cost_count
        self.max_get_quality_count = max_get_quality_count
        self.max_could_be_optimized_count = max_could_be_optimized_count
        self.max_is_enough_quality_count = max_is_enough_quality_count
        self.max_get_output_of_stage_count = max_get_output_of_stage_count

    def get_cost(self):
        self.get_cost_count += 1
        CALLS_COUNTER.method_name(self.name, "get_cost", self.get_cost_count)
        return self.get_cost_count

    def get_quality(self, control_params=None):
        self.get_quality_count += 1
        CALLS_COUNTER.method_name(self.name, "get_quality",
                                  self.get_quality_count)
        return self.get_quality_count

    def could_be_optimized(self):
        self.could_be_optimized_count += 1
        CALLS_COUNTER.method_name(self.name, "could_be_optimized",
                                  self.could_be_optimized_count)
        return self.is_enough_quality_count < 8

    def is_enough_quality(self, value):
        self.is_enough_quality_count += 1
        CALLS_COUNTER.method_name(self.name, "is_enough_quality",
                                  self.is_enough_quality_count)
        return self.is_enough_quality_count >= 5

    def get_output_of_stage(self):
        self.get_output_of_stage_count += 1
        output = [self.get_output_of_stage_count] * len(self.input_vector)
        output[0] = int(self.name)
        CALLS_COUNTER.method_name(self.name, "get_output_of_stage",
                                  self.get_output_of_stage_count)
        return output


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
# All adges directed to down
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

PSO_ALGORITHM = PsoAlgorithm(TESTED_PROCESS, GROUPING_STRATEGY, 2)
