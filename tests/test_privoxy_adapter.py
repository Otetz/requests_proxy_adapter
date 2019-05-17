# -*- coding: utf-8 -*-

"""Tests for :class:`requests_proxy_adapter.PrivoxyAdapter` class."""

import requests
from flaky import flaky
from pytest import raises, fixture

from requests_proxy_adapter import PrivoxyAdapter
from requests_proxy_adapter.exceptions import PrivoxyError
from tests import PROXY_HOST, URL_HTTP


@fixture(scope='module')
def public_ip():
    """
    Pytest fixture for current public IP-address.

    :return: Public IP-address.
    :rtype: str
    """
    assert PROXY_HOST is not None
    r = requests.get(URL_HTTP)
    assert r.status_code == 200
    return r.json()['origin']


@flaky
# noinspection PyShadowingNames
def test_http(public_ip):
    s = requests.Session()
    adapter = PrivoxyAdapter('http://%s:8118' % PROXY_HOST)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    r = s.get(URL_HTTP)
    assert r.status_code == 200
    anon_ip = r.json()['origin']
    assert anon_ip != public_ip


@flaky
# noinspection PyShadowingNames
def test_https(public_ip):
    s = requests.Session()
    adapter = PrivoxyAdapter('http://%s:8118' % PROXY_HOST)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    r = s.get('http://httpbin.org/ip')
    assert r.status_code == 200
    anon_ip = r.json()['origin']
    assert anon_ip != public_ip


@flaky
def test_internal_retry():
    s = requests.Session()
    retries = 2
    adapter = PrivoxyAdapter('http://%s:8118' % PROXY_HOST, retries=retries)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    with raises(PrivoxyError) as pe:
        s.get('http://localhost:9999')
    assert pe.value.args[0] == 'Too many retries: %d' % retries


def test_repr():
    adapter = PrivoxyAdapter('http://%s:8118' % PROXY_HOST)
    assert str(adapter)
    assert str(adapter).startswith('<PrivoxyAdapter')
    assert ' url:' in str(adapter)
    assert ' retry wait:' in str(adapter)
