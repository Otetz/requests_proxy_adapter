# -*- coding: utf-8 -*-

"""Unit test package for requests_proxy_adapter."""

import os

PROXY_HOST = os.getenv('PROXY_HOST')
URL_HTTP = 'http://httpbin.org/ip'

assert PROXY_HOST
