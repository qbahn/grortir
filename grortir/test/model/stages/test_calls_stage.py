"""Test class for module calls_stage."""

from unittest import TestCase
from unittest.mock import Mock, sentinel

from grortir.main.model.stages.calls_stage import CallsStage

MAX_CALLS = 100
CONTRL_PARAMS = [1, 1, 1, 1, 1, 1.5]


class TestCallsStage(TestCase):
    """Test class for CallsStage."""

    def test_get_quality(self):
        """Test for get_quality method."""
        tested_object = Mock()
        tested_object.cost = 7
        tested_object.calculate_quality.return_value = sentinel.quality
        tested_object.control_params = CONTRL_PARAMS
        result = CallsStage.get_quality(tested_object, CONTRL_PARAMS)
        self.assertEqual(tested_object.cost, 8)
        tested_object.calculate_quality.assert_called_with(CONTRL_PARAMS)
        self.assertEqual(result, sentinel.quality)

    def test_get_quality_without_vector(self):
        """Test for get_quality method when no arguments passed."""
        tested_object = Mock()
        tested_object.cost = 9
        tested_object.calculate_quality.return_value = sentinel.quality
        tested_object.control_params = CONTRL_PARAMS
        CallsStage.get_quality(tested_object)
        self.assertEqual(tested_object.cost, 10)
        tested_object.calculate_quality.assert_called_with(CONTRL_PARAMS)

    def test_get_cost(self):
        """Test for get_cost method."""
        tested_object = Mock()
        tested_object.cost = sentinel.cost
        result = CallsStage.get_cost(tested_object)
        self.assertEqual(result, sentinel.cost)

    def test_calculate_quality_ex(self):
        """Test case when control are wrong."""
        input_vector = (2, 3, 4, 5, 6)
        tested_object = CallsStage('name', MAX_CALLS, input_vector)
        tested_object.control_params = [2, 2]
        with self.assertRaises(AssertionError):
            tested_object.calculate_quality(tested_object.control_params)

    def test_calculate_quality_ok(self):
        """Test case when control params and input are okay."""
        input_vector = (2, 3, 4, 5, 6, 1)
        tested_object = CallsStage('name', MAX_CALLS, input_vector)
        tested_object.control_params = CONTRL_PARAMS
        result = tested_object.calculate_quality(tested_object.control_params)
        self.assertEqual(result, 55.25)

    def test_could_be_optimized_pos(self):
        """Positive case for test could_be_optimized method."""
        tested_object = Mock()
        tested_object.get_cost.return_value = MAX_CALLS - 1
        tested_object.max_calls = MAX_CALLS
        result = CallsStage.could_be_optimized(tested_object)
        self.assertTrue(result)

    def test_could_be_optimized_neg(self):
        """Negative case for test could_be_optimized method."""
        tested_object = Mock()
        tested_object.get_cost.return_value = MAX_CALLS + 1
        tested_object.max_calls = MAX_CALLS
        result = CallsStage.could_be_optimized(tested_object)
        self.assertFalse(result)

    def test_is_enough_quality(self):
        """Test is_enough_quality method."""
        tested_object = Mock()
        tested_object.maximum_acceptable_quality = 7
        result = CallsStage.is_enough_quality(tested_object, 8)
        self.assertFalse(result)

    def test_get_output_of_stage(self):
        """Test returning output."""
        tested_object = CallsStage('name', MAX_CALLS)
        result = tested_object.get_output_of_stage()
        self.assertEqual([], result)
