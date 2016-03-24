"""Module for testing."""

import unittest

from grortir.main.model.core.abstract_process import AbstractProcess


class TestAbstractProcess(unittest.TestCase):
    """Class for testing."""
    def test___init__(self):
        """Method which check constructor."""
        tested_object = AbstractProcess()
        self.assertIsNotNone(tested_object)
