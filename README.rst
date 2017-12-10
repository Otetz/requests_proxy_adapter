######################
Requests Proxy Adapter
######################


.. image:: https://img.shields.io/pypi/v/requests_proxy_adapter.svg
        :target: https://pypi.python.org/pypi/requests_proxy_adapter

.. image:: https://img.shields.io/travis/Otetz/requests_proxy_adapter.svg
        :target: https://travis-ci.org/Otetz/requests_proxy_adapter

.. image:: https://api.codeclimate.com/v1/badges/9f40b1896cbea3ac418a/maintainability
   :target: https://codeclimate.com/github/Otetz/requests_proxy_adapter/maintainability
   :alt: Maintainability

.. image:: https://readthedocs.org/projects/requests-proxy-adapter/badge/?version=latest
        :target: https://requests-proxy-adapter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Otetz/requests_proxy_adapter/shield.svg
     :target: https://pyup.io/repos/github/Otetz/requests_proxy_adapter/
     :alt: Updates


Set of Proxy Transport Adapters for `Requests <http://docs.python-requests.org/en/latest/>`_.

* Free software: MIT license
* Documentation: https://requests-proxy-adapter.readthedocs.io.


Features
********

* `PrivoxyAdapter <./requests_proxy_adapter.html#requests_proxy_adapter.api.PrivoxyAdapter>`_ -- The transport adapter
  for `Requests <http://docs.python-requests.org/en/latest/>`_ to use Privoxy proxy-server with retries when backend
  errors occurred.
* `RetryPrivoxyAdapter <./requests_proxy_adapter.html#requests_proxy_adapter.api.RetryPrivoxyAdapter>`_ -- The transport
  adapter for Requests to use Privoxy proxy-server with retries when backend errors occurred and retries if errors
  occured on target site by
  `urllib3.util.retry <http://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry>`_
  module.


.. include:: usage

.. include:: ../AUTHORS
