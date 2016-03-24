"""Module for testing."""

from unittest import TestCase

from grortir.main.model.core.AbstractStage import AbstractStage


class TestAbstractStage(TestCase):
    """Class for testing AbstractStage."""

    def test___init__(self):
        """Constructor test."""
        tested_object = AbstractStage()
        self.assertIsNotNone(tested_object)
