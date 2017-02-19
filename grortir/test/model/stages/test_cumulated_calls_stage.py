"""Test class for module calls_stage."""

from unittest import TestCase
from unittest.mock import Mock

from grortir.main.model.stages.cumulated_calls_stage import CumulatedCallsStage

MAX_CALLS = 100
CONTRL_PARAMS = [1, 1, 1, 1, 1, 1.5]


class TestCumulatedCallsStage(TestCase):
    """Test class for CumulatedCallsStage."""

    def test__init__(self):
        tested_object = CumulatedCallsStage("Tested obj",
                                            MAX_CALLS, (1, 2, 3), 0.03)
        self.assertEquals(tested_object.control_params, [0, 0])
        self.assertEquals(tested_object.name, "Tested obj")
        self.assertEquals(tested_object.max_calls, MAX_CALLS)
        self.assertEquals(tested_object.maximum_acceptable_quality, 0.03)
        self.assertEquals(tested_object.lower_bounds, [-1, -1])
        self.assertEquals(tested_object.upper_bounds, [1, 1])

    def test_calculate_quality_ex(self):
        """Test case when control are wrong."""
        input_vector = (2, 3, 4, 5, 6)
        tested_object = CumulatedCallsStage('name', MAX_CALLS, input_vector)
        tested_object.control_params = [2, 2, 2, 2, 2]
        with self.assertRaises(AssertionError):
            tested_object.calculate_quality(input_vector,
                                            tested_object.control_params)

    def test_calculate_quality_ok(self):
        """Test case when control params and input are okay."""
        input_vector = (2, 3, 4, 5, 6, 1, 99)
        tested_object = CumulatedCallsStage('name', MAX_CALLS, input_vector)
        tested_object.control_params = CONTRL_PARAMS
        result = tested_object.calculate_quality(input_vector,
                                                 tested_object.control_params)
        self.assertEqual(result, 55.25)

    def test_get_output_of_stage_empty(self):
        """Test returning output."""
        tested_object = CumulatedCallsStage('name', MAX_CALLS)
        with self.assertRaises(AssertionError):
            tested_object.get_output_of_stage([], [])

    def test_get_output_of_stage(self):
        tested_object = Mock()
        tested_object.calculate_quality.return_value = 999
        result = CumulatedCallsStage.get_output_of_stage(tested_object,
                                                         [1, 2, 3, 4, 99],
                                                         [5, 6, 7, 8])
        self.assertEqual([5, 6, 7, 8, 999], result)
