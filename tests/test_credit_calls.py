"""Test for intelligent credits."""
from unittest import TestCase

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.model.stages.calls_stage import CallsStage
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.credit_calls_optimization_strategy import \
    CreditCallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm


class TestInteligentCredits(TestCase):
    def test_credit_strategy_success(self):
        pso_algorithm, stages = prepare_data()
        stages[7].max_calls += 27
        pso_algorithm.run()
        is_success = pso_algorithm.process.optimization_status \
            == OptimizationStatus.success
        self.assertTrue(is_success)

    def test_credit_strategy_fail_at_last_step(self):
        pso_algorithm, stages = prepare_data()
        stages[7].max_calls += 26
        pso_algorithm.run()
        is_success = pso_algorithm.process.optimization_status \
            == OptimizationStatus.success
        self.assertFalse(is_success)

    def test_credit_strategy_fail_between_groups(self):
        pso_algorithm, stages = prepare_data()
        stages[0].max_calls = 60
        stages[1].max_calls = 60
        stages[2].max_calls = 60
        stages[3].max_calls = 60
        stages[4].max_calls = 60
        stages[5].max_calls = 0
        stages[6].max_calls = 0
        stages[7].max_calls = 0
        pso_algorithm.run()
        is_success = pso_algorithm.process.optimization_status \
            == OptimizationStatus.success
        self.assertFalse(is_success)
        for i in range(3, 8):
            self.assertIsNone(stages[i].final_output)
            self.assertIsNone(stages[i].final_cost)
            self.assertIsNone(stages[i].final_quality)
            self.assertEqual(stages[i].optimization_status,
                             OptimizationStatus.failed)
        for i in range(0, 3):
            self.assertEqual(stages[i].optimization_status,
                             OptimizationStatus.success)

    def test_credit_strategy_fail_on_group(self):
        pso_algorithm, stages = prepare_data()
        stages[0].max_calls = 60
        stages[1].max_calls = 60
        stages[2].max_calls = 60
        stages[3].max_calls = 60
        stages[4].max_calls = 60
        stages[5].max_calls = 3
        stages[6].max_calls = 0
        stages[7].max_calls = 0
        pso_algorithm.run()
        is_success = pso_algorithm.process.optimization_status \
            == OptimizationStatus.success
        self.assertFalse(is_success)
        for i in range(3, 6):
            self.assertEqual(stages[i].final_cost, 2)
            self.assertEqual(stages[i].final_quality, 10000)
            self.assertEqual(stages[i].optimization_status,
                             OptimizationStatus.failed)
        for i in range(6, 8):
            self.assertIsNone(stages[i].final_output)
            self.assertIsNone(stages[i].final_cost)
            self.assertIsNone(stages[i].final_quality)
            self.assertEqual(stages[i].optimization_status,
                             OptimizationStatus.failed)
        for i in range(0, 3):
            self.assertEqual(stages[i].optimization_status,
                             OptimizationStatus.success)


class ExampleProcess(AbstractProcess):
    pass


class FixedCallsStage(CallsStage):
    def __init__(self, name, max_calls, input_vector, on_which_cost_success):
        super().__init__(name, max_calls, input_vector)
        self.on_which_cost_success = on_which_cost_success

    def is_enough_quality(self, value):
        return self.on_which_cost_success <= self.get_cost()

    def calculate_quality(self, input_vector, control_params):
        if self.is_enough_quality(1):
            return 0
        return 10000

    def get_output_of_stage(self, input_vector, control_params):
        return input_vector


def prepare_data():
    stages = {}
    for i in range(8):
        stages[i] = FixedCallsStage(str(i), 70, (0, 0, 0), (100 - i * 10))
    # Summary max_calls is equal to 560
    tested_process = ExampleProcess()
    # Our graph:
    #   0
    #   |
    #   1
    #   |\
    #   2 4
    #   | |\
    #   3 5 6
    #        \
    #         7
    # All edges directed to down
    # Order of nodes is the same as names
    tested_process.add_edge(stages[0], stages[1])
    tested_process.add_edge(stages[1], stages[2])
    tested_process.add_edge(stages[2], stages[3])
    tested_process.add_edge(stages[1], stages[4])
    tested_process.add_edge(stages[4], stages[5])
    tested_process.add_edge(stages[4], stages[6])
    tested_process.add_edge(stages[6], stages[7])
    # Groups:
    #   (0)0
    #      |
    #   (0)1
    #      |\
    #   (0)2 4(1)
    #      | | \
    #   (1)3 5(1)6(2)
    #             \
    #              7(3)
    # Minimum required steps to success: 3*101+3*71+1*41+1*31= 588
    grouping_strategy = GroupingStrategy(list(stages.values()))
    grouping_strategy.define_group((stages[0], stages[1], stages[2]))
    grouping_strategy.define_group((stages[3], stages[4], stages[5]))
    grouping_strategy.define_group((stages[6],))
    grouping_strategy.define_group((stages[7],))
    optimization_strategy = CreditCallsOptimizationStrategy()
    pso_algorithm = PsoAlgorithm(tested_process, grouping_strategy,
                                 optimization_strategy, 2)
    return pso_algorithm, stages
