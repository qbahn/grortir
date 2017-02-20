import logging
import os
from unittest import TestCase

from grortir.main.logging.logging_configuration import LoggingConfiguration


class TestLoggingConfiguration(TestCase):
    def test_init(self):
        LoggingConfiguration.init()
        logger = logging.getLogger(__name__)
        stat_info_before = os.stat('grortir.log')
        size_before = stat_info_before.st_size
        logger.info('Test INFO level')
        logger.debug('Test DEBUG level')
        stat_info_after = os.stat('grortir.log')
        size_after = stat_info_after.st_size
        self.assertTrue(size_before < size_after)
