"""Test class for module calls_stage."""

from unittest import TestCase
from unittest.mock import Mock, sentinel

from grortir.main.model.stages.calls_stage import CallsStage


class TestCallsStage(TestCase):
    """Test class for CallsStage."""

    def test_get_quality(self):
        """Test for get_quality method."""
        tested_object = Mock()
        tested_object.cost = 7
        tested_object.calculate_quality.return_value = sentinel.quality
        result = CallsStage.get_quality(tested_object)
        self.assertEqual(tested_object.cost, 8)
        tested_object.calculate_quality.assert_called_with()
        self.assertEqual(result, sentinel.quality)

    def test_get_cost(self):
        """Test for get_cost method."""
        tested_object = Mock()
        tested_object.cost = sentinel.cost
        result = CallsStage.get_cost(tested_object)
        self.assertEqual(result, sentinel.cost)

    def test_calculate_quality_ex(self):
        """Test case when control are wrong."""
        input_vector = (2, 3, 4, 5, 6)
        tested_object = CallsStage('name', input_vector)
        tested_object.control_params = [2, 2]
        with self.assertRaises(AssertionError):
            tested_object.calculate_quality()

    def test_calculate_quality_ok(self):
        """Test case when control params and input are okay."""
        input_vector = (2, 3, 4, 5, 6, 1)
        tested_object = CallsStage('name', input_vector)
        tested_object.control_params = [1, 1, 1, 1, 1, 1.5]
        result = tested_object.calculate_quality()
        self.assertEqual(result, 55.25)
