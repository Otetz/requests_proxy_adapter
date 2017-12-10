# -*- coding: utf-8 -*-

"""
requests_proxy_adapter.api
~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of Proxy Transport Adapters for module :mod:`requests`.
"""

import time

from requests import PreparedRequest  # noqa: F401
from requests.adapters import HTTPAdapter
from requests.exceptions import ProxyError
from urllib3 import Retry, HTTPResponse  # noqa: F401

from .exceptions import (
    PrivoxyError4Retry, ForwardingFailedError, NoServerDataError, ConnectionTimeoutError, PrivoxyError,
)


class PrivoxyAdapter(HTTPAdapter):
    """
    The transport adapter for Requests to use Privoxy proxy-server with retries when backend errors occurred.

    Implements Requests's :class:`HTTPAdapter` API.

    If privoxy backend raises `500 Internal Privoxy Error` in suitable cases make `retries` number of internal
    retries with delay of `retry_wait` seconds.

    :param str proxy_url: Complete URL-address of Privoxy proxy instance (scheme, host & port).
    :param int retry_wait: (optional) Waiting in seconds before next retry if backend raise specified errors.
        Default 1 second.
    :param int retries: (optional) Maximum number of retries. Default 3 times.
    :param kwargs: (optional) Arbitrary keyword arguments for parent class :class:`HTTPAdapter`.
    """

    __attrs__ = HTTPAdapter.__attrs__ + ['_proxies', 'retry_wait', 'proxy_url', '_retries', '_count']

    def __init__(self, proxy_url, retry_wait=1, retries=3, **kwargs):
        self.proxy_url = proxy_url
        self._proxies = {
            'http': proxy_url, 'https': proxy_url,
        }
        self.retry_wait = retry_wait
        self._retries = retries
        self._count = 0
        super(PrivoxyAdapter, self).__init__(**kwargs)

    def send(self, *args, **kwargs):
        """
        Sends :class:`PreparedRequest` object. Returns Response object.

        Replace `proxies` in kwargs if present with adapter-initialised value.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: Response object
        :rtype: :class:`Response`
        """
        kwargs.pop('proxies', None)
        self._count += 1
        try:
            res = super(PrivoxyAdapter, self).send(proxies=self._proxies, *args, **kwargs)
        except PrivoxyError4Retry:
            if self._count == self._retries:
                raise PrivoxyError("Too many retries: %d" % self._count)
            time.sleep(self.retry_wait)
            return self.send(*args, **kwargs)
        return res

    def build_response(self, req, resp):
        """
        Builds a :class:`Response <requests.Response>` object from a urllib3 response.

        Build response are doing by parent class :class:`HTTPAdapter`. This code detect 500 in response status code and
        search in text of response specific strings.

        :param PreparedRequest req: The :class:`PreparedRequest` used to generate the response.
        :param HTTPResponse resp: The urllib3 :class:`HTTPResponse` object.
        :return: :class:`Response <requests.Response>` object
        :rtype: :class:`Response <requests.Response>`
        """
        r = super(PrivoxyAdapter, self).build_response(req, resp)
        if r.status_code == 500 and r.text is not None and '500 Internal Privoxy Error' in r.text:
            if '<code>forwarding-failed</code>' in r.text:
                raise ForwardingFailedError
            if '<code>no-server-data</code>' in r.text:  # pragma: no cover
                raise NoServerDataError
            if '<code>connection-timeout</code>' in r.text:  # pragma: no cover
                raise ConnectionTimeoutError
            if '<title>500 Internal Privoxy Error</title>' in r.text:  # pragma: no cover
                raise PrivoxyError(str(r.text))
            raise ProxyError(r.text)  # pragma: no cover
        return r

    def __repr__(self):
        return '<{class_name} url:{url} retry wait:{wait} s>'.format(class_name=self.__class__.__name__,
                                                                     url=self.proxy_url, wait=self.retry_wait)


class RetryPrivoxyAdapter(PrivoxyAdapter):
    """
    The transport adapter for Requests to use Privoxy proxy-server with retries when backend errors occurred and
    retries if errors occured on target site by :class:`Retry` module.

    Implements Requests's :class:`HTTPAdapter` API. Extend class :class:`PrivoxyAdapter`

    :param int retries: Total number of retries to allow. Takes precedence over other counts.
    :param float backoff_factor: A backoff factor to apply between attempts after the second try (most errors are
        resolved immediately by a second try without a delay).
    :param set status_forcelist: A set of integer HTTP status codes that we should force a retry on.
    :param args: Variable length argument list.
    :param kwargs: Arbitrary keyword arguments.
    """

    __attrs__ = PrivoxyAdapter.__attrs__ + ['retries', 'backoff_factor', 'status_forcelist']

    def __init__(self, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), *args, **kwargs):
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor,
                      status_forcelist=status_forcelist)
        super(RetryPrivoxyAdapter, self).__init__(max_retries=retry, *args, **kwargs)

    def __repr__(self):
        return '<{class_name} url:{url} retries:{retires} backoff factor:{backoff} retry wait:{wait} s ' \
               'status_forcelist:{statuses}>'.format(class_name=self.__class__.__name__, url=self.proxy_url,
                                                     wait=self.retry_wait, retires=self.retries,
                                                     backoff=self.backoff_factor, statuses=self.status_forcelist)
