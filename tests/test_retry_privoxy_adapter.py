# -*- coding: utf-8 -*-

"""Tests for :class:`requests_proxy_adapter.RetryPrivoxyAdapter` class."""

import requests
from flaky import flaky
from pytest import raises
from requests.exceptions import RetryError, ConnectionError

from requests_proxy_adapter import RetryPrivoxyAdapter
from tests import PROXY_HOST


@flaky
def test_http():
    s = requests.Session()
    adapter = RetryPrivoxyAdapter(proxy_url='http://%s:8118' % PROXY_HOST)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    with raises(RetryError):
        s.get('http://localhost:9999')


@flaky
def test_timeout():
    s = requests.Session()
    adapter = RetryPrivoxyAdapter(proxy_url='http://%s:8118' % PROXY_HOST)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    with raises(ConnectionError):
        s.get('http://httpbin.org/delay/2', timeout=1)


@flaky
def test_error_500():
    s = requests.Session()
    adapter = RetryPrivoxyAdapter(proxy_url='http://%s:8118' % PROXY_HOST)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    with raises(RetryError):
        s.get('http://httpbin.org/status/500')


def test_repr():
    adapter = RetryPrivoxyAdapter(proxy_url='http://%s:8118' % PROXY_HOST)
    assert str(adapter)
    assert str(adapter).startswith('<RetryPrivoxyAdapter')
    assert ' url:' in str(adapter)
    assert ' retries:' in str(adapter)
    assert ' backoff factor:' in str(adapter)
    assert ' retry wait:' in str(adapter)
    assert ' status_forcelist:' in str(adapter)
