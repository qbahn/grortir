"""Module for testing."""

from unittest import TestCase
from unittest.mock import Mock

from grortir.main.model.core.abstract_stage import AbstractStage


class TestAbstractStage(TestCase):
    """Class for testing AbstractStage."""

    def test___init__(self):
        """Constructor test."""
        tested_object = AbstractStage()
        self.assertIsNotNone(tested_object)

    def test___init__arguments_passed(self):
        """Check arguments in constructor."""
        abstract_stage_mock = Mock()
        input_vector = (1, 2, 3)
        AbstractStage.__init__(abstract_stage_mock, input_vector)
        self.assertEqual(abstract_stage_mock.input_vector, input_vector)

    def test___init__output_mutability(self):
        """Check fields in object."""
        input_vector = (1, 2, 3)
        tested_object = AbstractStage(input_vector)
        tested_object.current_vector[2] += 1
        self.assertEqual(tested_object.current_vector[2], 4)

    def test_get_cost(self):
        """Check get_cost method."""
        tested_object = AbstractStage()
        with self.assertRaises(NotImplementedError):
            tested_object.get_cost()

    def test_get_quality(self):
        """Check get_quality method."""
        tested_object = AbstractStage()
        with self.assertRaises(NotImplementedError):
            tested_object.get_quality()
