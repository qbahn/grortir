"""Module for testing grouped optimizer."""

from unittest import TestCase
from unittest.mock import Mock

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.optimizers.grouped_optimizer import GroupedOptimizer


class TestGroupedOptimizer(TestCase):
    """Class for testing Optimizer."""

    def setUp(self):
        """Set up environment."""
        self.some_process = AbstractProcess()
        self.first_stage = AbstractStage()
        self.second_stage = AbstractStage()
        self.third_stage_a = Mock()
        self.third_stage_b = Mock()
        self.some_process.add_path([self.first_stage, self.second_stage,
                                    self.third_stage_a])
        self.some_process.add_edge(self.second_stage, self.third_stage_b)

    def test___init__(self):
        """Testing creating object."""
        optimizer = GroupedOptimizer(self.some_process)
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.process, self.some_process)

    def test_calling_functions(self):
        """Test correct order of calling function."""
