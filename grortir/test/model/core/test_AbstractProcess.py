"""Module for testing."""

import unittest

from grortir.main.model.core.AbstractProcess import AbstractProcess


class test_AbstractProcess(unittest.TestCase):
    """Class for testing."""
    def test_constructor(self):
        """Method which check constructor."""
        tested_object = AbstractProcess()
        self.assertIsNotNone(tested_object)
