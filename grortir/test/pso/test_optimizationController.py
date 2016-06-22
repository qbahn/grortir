from unittest import TestCase
from unittest.mock import Mock

from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.pso.optimization_controller import OptimizationController


class TestOptimizationController(TestCase):
    def setUp(self):
        self.stage_success = Mock()
        self.stage_success.optimization_status = OptimizationStatus.success
        self.stage_failed = Mock()
        self.stage_failed.optimization_status = OptimizationStatus.failed
        self.stage_in_progress = Mock()
        self.stage_in_progress.optimization_status = OptimizationStatus.in_progress

    def test_should_stop_when_one_failed(self):
        self.assertFalse(OptimizationController.should_continue(
            [self.stage_success, self.stage_failed]))

    def test_should_continue_when_no_failed(self):
        self.assertTrue(OptimizationController.should_continue(
            [self.stage_success, self.stage_in_progress]))

    def test_should_stop_when_all_success(self):
        self.assertFalse((OptimizationController.should_continue(
            [self.stage_success, self.stage_success])))
