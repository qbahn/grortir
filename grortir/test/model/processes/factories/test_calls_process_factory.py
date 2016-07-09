"""Package to test calls_process_factory module."""

from unittest import TestCase

from grortir.main.model.processes.calls_process import CallsProcess
from grortir.main.model.processes.factories.calls_process_factory import \
    CallsProcessFactory

MAX_CALLS = 1000


class TestCallsProcessFactory(TestCase):
    """Class to test CallsProcessFactory."""

    def test_construct_process_linear(self):
        """Test linear process construction."""
        tested_object = CallsProcessFactory("linear", 7, MAX_CALLS)
        result = tested_object.construct_process()
        self.assertIsInstance(result, CallsProcess)

    def test_construct_process_not_ex(self):
        """Test case when structure not implemented."""
        tested_object = CallsProcessFactory("not_existed", 7, MAX_CALLS)
        with self.assertRaises(NotImplementedError):
            tested_object.construct_process()
