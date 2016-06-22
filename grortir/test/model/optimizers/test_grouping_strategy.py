"""Testing grouping strategy."""
from unittest import TestCase
from unittest.mock import Mock

from grortir.main.optimizers.grouping_strategy import GroupingStrategy


class TestGroupingStrategy(TestCase):
    def setUp(self):
        self.stage_1 = Mock()
        self.stage_2 = Mock()
        self.stage_3 = Mock()
        self.ordered_stages = [self.stage_1, self.stage_2, self.stage_3]
        self.tested_object = GroupingStrategy(self.ordered_stages)

    def test___init__(self):
        grouping_strategy = GroupingStrategy([])
        self.assertIsNotNone(grouping_strategy)

    def test_define_group_success(self):
        self.perform_simple_grouping()
        self.assertEqual(self.tested_object.groups[self.stage_1], 0)
        self.assertEqual(self.tested_object.groups[self.stage_2], 1)
        self.assertEqual(self.tested_object.groups[self.stage_3], 1)

    def perform_simple_grouping(self):
        self.tested_object.define_group((self.stage_1,))
        self.tested_object.define_group((self.stage_2, self.stage_3))

    def test_define_group_failed(self):
        self.tested_object.define_group((self.stage_1,))
        with self.assertRaisesRegex(ValueError, "Stage already added."):
            self.tested_object.define_group((self.stage_1,))

    def test_define_group_failed_not_cons(self):
        with self.assertRaisesRegex(ValueError,
                                    "Stage not considered in strategy."):
            self.tested_object.define_group((Mock(),))

    def test_get_actual_number_of_groups_0(self):
        tested_strategy = GroupingStrategy([self.stage_1, self.stage_2])
        result = tested_strategy.get_actual_numbers_of_groups()
        self.assertEqual(result, 0)

    def test_get_actual_number_of_groups_2(self):
        self.perform_simple_grouping()
        result = self.tested_object.get_actual_numbers_of_groups()
        self.assertEqual(result, 2)

    def test_get_items_from_the_same_group_1(self):
        self.perform_simple_grouping()
        result = self.tested_object.get_items_from_the_same_group(self.stage_1)
        self.assertListEqual(result, [self.stage_1])

    def test_get_items_from_the_same_group_2(self):
        self.perform_simple_grouping()
        result = self.tested_object.get_items_from_the_same_group(self.stage_2)
        self.assertEqual(set(result), set([self.stage_2, self.stage_3]))

    def test_get_items_from_the_same_group_0(self):
        with self.assertRaises(ValueError):
            self.tested_object.get_items_from_the_same_group(Mock())
