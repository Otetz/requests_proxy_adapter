# -*- coding: utf-8 -*-

"""
requests_proxy_adapter.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests Proxy Adapter's exceptions.
"""

from requests.exceptions import ProxyError


class PrivoxyError(ProxyError):
    """Base class for Privoxy-related exceptions."""
    pass


class PrivoxyError4Retry(PrivoxyError):
    """Base class for cases needed retrying request internally."""
    pass


class ForwardingFailedError(PrivoxyError4Retry):
    """Privoxy error response contains `forwarding-failed` message."""
    pass


class NoServerDataError(PrivoxyError4Retry):
    """Privoxy error response contains `no-server-data` message."""
    pass


class ConnectionTimeoutError(PrivoxyError4Retry):
    """Privoxy error response contains `connection-timeout` message."""
    pass
