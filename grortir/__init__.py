"""Package for Grortir."""

import sys

__project__ = 'Grortir'
__version__ = '0.1.7'

VERSION = "{0} v{1}".format(__project__, __version__)

PYTHON_VERSION = 3, 3

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    sys.exit("Python {0}.{1}+ is required.".format(*PYTHON_VERSION))
