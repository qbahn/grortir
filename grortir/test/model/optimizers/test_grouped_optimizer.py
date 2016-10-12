"""Module for testing grouped optimizer."""

import unittest.mock as mock
from unittest import TestCase

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
