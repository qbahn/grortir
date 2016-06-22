from unittest import TestCase

from grortir.main.model.core.optimization_status import OptimizationStatus


class TestOptimizationStatus(TestCase):
    def test_equals_positive(self):
        self.assertTrue(OptimizationStatus.failed.__eq__(OptimizationStatus.failed))

    def test_equals_negative(self):
        self.assertFalse(
            OptimizationStatus.failed.__eq__(None))
