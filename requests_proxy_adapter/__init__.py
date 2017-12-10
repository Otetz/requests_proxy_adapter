# -*- coding: utf-8 -*-

import logging

from .api import PrivoxyAdapter, RetryPrivoxyAdapter  # noqa: F401
from .version import __version__  # noqa: F401

logging.getLogger("urllib3").setLevel(logging.ERROR)

__author__ = "Alexey Shevchenko"
__email__ = 'otetz@me.com'
__copyright__ = "Copyright 2017, Alexey Shevchenko"
