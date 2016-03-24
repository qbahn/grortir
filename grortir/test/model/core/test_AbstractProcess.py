import unittest

import grortir
from grortir.main.model.core.AbstractProcess import AbstractProcess


class test_AbstractProcess(unittest.TestCase):
    def test_constructor(self):
        tested_object = AbstractProcess()
        self.assertIsNotNone(tested_object)
