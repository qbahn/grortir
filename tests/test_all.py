"""Sample integration test module."""
# pylint: disable=no-self-use,missing-docstring

import unittest

from grortir import sample


class TestGrortir(unittest.TestCase):

    """Sample integration test class."""

    @staticmethod
    def test_network_stuff():
        """Example Test method."""
        assert sample.function_with_network_stuff() is True

    @staticmethod
    def test_disk_stuff():
        """Another example Test method."""
        assert sample.function_with_disk_stuff() is False
