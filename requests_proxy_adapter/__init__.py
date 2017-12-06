# -*- coding: utf-8 -*-

"""Top-level package for Requests Proxy Adapter."""

__author__ = """Alexey Shevchenko"""
__email__ = 'otetz@me.com'
__version__ = '0.1.0'

import logging

from .api import PrivoxyAdapter, RetryPrivoxyAdapter

logging.getLogger("urllib3").setLevel(logging.ERROR)
