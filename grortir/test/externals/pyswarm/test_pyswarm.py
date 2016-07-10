"""Tests for pyswarm."""
from unittest import TestCase

from grortir.externals.pyswarm.pso import pso
from grortir.main.model.core.abstract_stage import AbstractStage


class TestPso(TestCase):
    """Class for tests pyswarm."""

    def test_run_simple_pso(self):
        """Test running library."""

        stage_to_test = ExampleStage(EXAMPLE_INPUT)
        x_opt, f_opt, iterations = pso(stage=stage_to_test)
        self.assertIsNotNone(x_opt)
        self.assertIsNotNone(f_opt)
        self.assertIsNotNone(iterations)

    def test_not_able_to_optimize_stage(self):
        """Test when stage is not able to optimize."""
        stage_not_able_to_optimize = StageNotAbleToOptimize(EXAMPLE_INPUT)
        x_opt, f_opt, iterations = pso(stage=stage_not_able_to_optimize)
        self.assertIsNotNone(x_opt)
        self.assertIsNotNone(f_opt)
        self.assertIsNotNone(iterations)
        self.assertEqual(iterations, 1)


# Test data:
LOWER_BOUND = [-3, -1]
UPPER_BOUND = [2, 6]
EXAMPLE_INPUT = (-1, 3)


class ExampleStage(AbstractStage):
    """Stage for testing."""

    def __init__(self, input_vector):
        super().__init__(input_vector)
        self.lower_bounds = LOWER_BOUND
        self.upper_bounds = UPPER_BOUND
        self.counter = 0

    @staticmethod
    def get_cost():
        """No costs."""
        return 0

    def get_quality(self, vector=None):
        """Return quality."""
        self.control_params = vector
        self.counter += 1
        return myfunc(self.control_params)

    @staticmethod
    def could_be_optimized():
        """Return True."""
        return True

    def is_enough_quality(self, value):
        """Return False."""
        return False

    @staticmethod
    def get_output_of_stage():
        """Return None."""
        return None


class StageNotAbleToOptimize(ExampleStage):
    """Stage which couldn't be optimized."""

    @staticmethod
    def could_be_optimized():
        """Returns false."""
        return False

    @staticmethod
    def get_output_of_stage():
        """Return None."""
        return None


def myfunc(input_vector):
    """Simple function for tests.

    Args:
        input_vector (list): input vector

    Returns:
        float: value of function
    """
    x_1 = input_vector[0]
    x_2 = input_vector[1]
    return x_1 ** 4 - 2 * x_2 * x_1 ** 2 + x_2 ** 2 + x_1 ** 2 - 2 * x_1 + 5
