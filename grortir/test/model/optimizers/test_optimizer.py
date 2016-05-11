"""Module for testing optimizer."""

from unittest import TestCase
from unittest.mock import patch, Mock, sentinel

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.model.core.optimization_status import OptimizationStatus
from grortir.main.optimizers.optimizer import Optimizer


class TestOptimizer(TestCase):
    """Class for testing Optimizer."""

    def setUp(self):
        """Set up environment."""
        self.some_process = AbstractProcess()
        self.first_stage = AbstractStage()
        self.second_stage = AbstractStage()
        self.some_process.add_path([self.first_stage, self.second_stage])

    def test___init__(self):
        """Testing creating object."""
        optimizer = Optimizer(self.some_process)
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.process, self.some_process)

    def test_set_order(self):
        """Test changing order of optimizing."""
        optimizer = Optimizer(self.some_process)
        optimizer.set_custom_optimizing_order(
            [self.second_stage, self.first_stage])
        self.assertEqual(optimizer.ordered_stages[0], self.second_stage)

    def test_set_order_fail(self):
        """Test changing order of optimizing with incorrect list."""
        optimizer = Optimizer(self.some_process)
        with self.assertRaises(ValueError):
            optimizer.set_custom_optimizing_order(
                [self.second_stage, self.first_stage, self.first_stage])

    @patch('grortir.main.optimizers.optimizer.pso')
    def test_optimize_process(self, pso_mock):
        """Test optimization of initial stage in process."""
        optimizer = Optimizer(self.some_process)
        result = optimizer.optimize_process()
        pso_mock.assert_called_once_with(self.first_stage, swarmsize=40)
        self.assertFalse(result)

    @patch('grortir.main.optimizers.optimizer.pso')
    def test_optimize_whole_process(self, pso_mock):
        """Test whole optimization."""
        optimizer = Optimizer(self.some_process)
        self.first_stage.optimization_status = OptimizationStatus.success
        self.first_stage.get_output_of_stage = Mock(return_value=sentinel)
        self.second_stage.optimization_status = OptimizationStatus.success
        result = optimizer.optimize_process()
        pso_mock.assert_called_with(self.second_stage, swarmsize=40)
        self.assertTrue(result)

    @patch('grortir.main.optimizers.optimizer.pso')
    def test_optimize_incorrect_process(self, pso_mock):
        """Test incorrect process structure."""
        optimizer = Optimizer(self.some_process)
        third_stage = AbstractStage()
        self.some_process.add_edge(third_stage, self.second_stage)
        self.first_stage.optimization_status = OptimizationStatus.success
        self.first_stage.get_output_of_stage = Mock(return_value=sentinel)
        pso_mock.assert_not_called()
        with self.assertRaises(AttributeError):
            optimizer.optimize_process()
