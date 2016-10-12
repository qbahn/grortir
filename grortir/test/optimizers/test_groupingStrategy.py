from unittest import TestCase
from unittest.mock import Mock

from grortir.main.optimizers.grouping_strategy import GroupingStrategy


class TestGroupingStrategy(TestCase):
    def test_get_items_from_group(self):
        grouping_strategy = Mock()
        grouping_strategy.get_actual_numbers_of_groups.return_value = 3
        with self.assertRaises(ValueError):
            GroupingStrategy.get_items_from_group(grouping_strategy, 4)
