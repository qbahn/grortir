from unittest import TestCase

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.optimizers.base_optimizer import BaseOptimizer


class TestBaseOptimizer(TestCase):
    """Class for testing Optimizer."""

    def setUp(self):
        """Set up environment."""
        self.some_process = AbstractProcess()
        self.first_stage = AbstractStage()
        self.second_stage = AbstractStage()
        self.some_process.add_path([self.first_stage, self.second_stage])

    def test___init__(self):
        """Testing creating object."""
        optimizer = BaseOptimizer(self.some_process)
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.process, self.some_process)

    def test_set_order(self):
        """Test changing order of optimizing."""
        optimizer = BaseOptimizer(self.some_process)
        optimizer.set_custom_optimizing_order(
            [self.second_stage, self.first_stage])
        self.assertEqual(optimizer.ordered_stages[0], self.second_stage)

    def test_set_order_fail(self):
        """Test changing order of optimizing with incorrect list."""
        optimizer = BaseOptimizer(self.some_process)
        with self.assertRaises(ValueError):
            optimizer.set_custom_optimizing_order(
                [self.second_stage, self.first_stage, self.first_stage])

    def test_optimize_process(self):
        optimizer = BaseOptimizer(self.some_process)
        with self.assertRaises(NotImplementedError):
            optimizer.optimize_process()
