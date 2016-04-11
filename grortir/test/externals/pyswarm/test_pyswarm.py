"""Tests for pyswarm."""
from unittest import TestCase
from grortir.externals.pyswarm.pso import pso


class TestPso(TestCase):
    """Class for tests pyswarm."""

    def test_run_simple_pso(self):
        """Test running library."""
        lower_bound = [-3, -1]
        upper_bound = [2, 6]

        x_opt, f_opt = pso(myfunc, lower_bound, upper_bound)
        self.assertIsNotNone(x_opt)
        self.assertIsNotNone(f_opt)


def myfunc(input_vector):
    """Simple function for tests.

    Args:
        input_vector (list): input vector

    Returns:
        object : value of function
    """
    x_1 = input_vector[0]
    x_2 = input_vector[1]
    return x_1 ** 4 - 2 * x_2 * x_1 ** 2 + x_2 ** 2 + x_1 ** 2 - 2 * x_1 + 5
