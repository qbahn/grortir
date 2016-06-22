from unittest import TestCase
from unittest.mock import Mock

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.optimizers.result import Result


class TestResult(TestCase):
    def setUp(self):
        self.success_stage = Mock()
        self.success_stage.optimization_status = OptimizationStatus.success
        self.failed_stage = Mock()
        self.failed_stage.optimization_status = OptimizationStatus.failed
        self.process = Mock()

    def test_generate_failed(self):
        tested_object = Result(self.process)
        self.process.nodes.return_value = [self.success_stage,
                                           self.failed_stage]
        tested_object.generate()
        self.assertEqual(tested_object.summary_result,
                         OptimizationStatus.failed)

    def test_generate_success(self):
        tested_object = Result(self.process)
        self.process.nodes.return_value = [self.success_stage,
                                           self.success_stage]
        tested_object.generate()
        self.assertEqual(tested_object.summary_result,
                         OptimizationStatus.success)
