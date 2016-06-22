"""Testing grouping strategy."""
from unittest import TestCase

from grortir.main.optimizers.grouping_strategy import GroupingStrategy


class TestGroupingStrategy(TestCase):
    def test___init__(self):
        grouping_strategy = GroupingStrategy()
        self.assertIsNotNone(grouping_strategy)
