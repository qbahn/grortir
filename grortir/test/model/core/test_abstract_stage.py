"""Module for testing."""

from unittest import TestCase

from grortir.main.model.core.abstract_stage import AbstractStage


class TestAbstractStage(TestCase):
    """Class for testing AbstractStage."""

    def test___init__(self):
        """Constructor test."""
        tested_object = AbstractStage()
        self.assertIsNotNone(tested_object)

    def test___init__arguments_passed(self):
        """Check arguments in constructor."""
        pass
