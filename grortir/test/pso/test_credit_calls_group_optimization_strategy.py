from unittest import TestCase
from unittest.mock import Mock

from grortir.main.pso.credit_calls_group_optimization_strategy import \
    CreditCallsGroupOptimizationStrategy


class TestCreditCallsGroupOptimizationStrategy(TestCase):
    def test_initialize(self):
        process, stages = self.get_basic_process()
        tested_object = CreditCallsGroupOptimizationStrategy(stages, process)

        tested_object.initialize()

        self.assertEqual(tested_object.max_calls_for_group, 60)
        self.assertEqual(tested_object.expected_quality, 1)

    def get_basic_process(self):
        stages = []
        for i in range(1, 4):
            stages.append(Mock())
            stages[i - 1].get_cost.return_value = 0
            stages[i - 1].get_maximal_acceptable_cost.return_value = i * 10
            stages[i - 1].maximum_acceptable_quality = i
        process = Mock()
        process.nodes.return_value = stages
        return process, stages

    def test_initialize_exception(self):
        stages = []
        for i in range(1, 4):
            stages.append(Mock())
            stages[i - 1].get_cost.return_value = 0
        process = Mock()
        process.nodes.return_value = stages
        stages[0].get_cost.return_value = 1
        tested_object = CreditCallsGroupOptimizationStrategy(stages, process)
        with self.assertRaises(ValueError):
            tested_object.initialize()

    def test_should_continue_true(self):
        process, stages = self.get_basic_process()
        tested_object = CreditCallsGroupOptimizationStrategy(stages, process)
        tested_object.initialize()
        stages[0].get_cost.return_value = 20
        stages[1].get_cost.return_value = 20
        stages[2].get_cost.return_value = 20
        best_particle = Mock()
        best_particle.best_quality = 2
        result = tested_object.should_continue(best_particle)
        self.assertTrue(result)

    def test_should_continue_false_enough_quality(self):
        process, stages = self.get_basic_process()
        tested_object = CreditCallsGroupOptimizationStrategy(stages, process)
        tested_object.initialize()
        best_particle = Mock()
        stages[0].get_cost.return_value = 20
        stages[1].get_cost.return_value = 20
        stages[2].get_cost.return_value = 20
        best_particle.best_quality = 0.5
        result = tested_object.should_continue(best_particle)
        self.assertFalse(result)

    def test_should_continue_false_not_safe_cost(self):
        process, stages = self.get_basic_process()
        tested_object = CreditCallsGroupOptimizationStrategy(stages, process)
        tested_object.initialize()
        best_particle = Mock()
        best_particle.best_quality = 2
        stages[0].get_cost.return_value = 20
        stages[1].get_cost.return_value = 20
        stages[2].get_cost.return_value = 21
        result = tested_object.should_continue(best_particle)
        self.assertFalse(result)
