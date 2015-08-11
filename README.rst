=========
py-cgmail
=========

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        | |codecov|
    * - package
      - |version| |downloads|

.. |docs| image:: https://readthedocs.org/projects/py-cgmail/badge/?style=flat
    :target: https://readthedocs.org/projects/py-cgmail
    :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/giovino/py-cgmail/master.svg?style=flat&label=Travis
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/giovino/py-cgmail

.. |appveyor| image:: https://img.shields.io/appveyor/ci/giovino/py-cgmail/master.svg?style=flat&label=AppVeyor
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/giovino/py-cgmail


.. |codecov| image:: https://img.shields.io/codecov/c/github/giovino/py-cgmail/master.svg?style=flat&label=Codecov
    :alt: Coverage Status
    :target: https://codecov.io/github/giovino/py-cgmail




.. |version| image:: https://img.shields.io/pypi/v/cgmail.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/cgmail

.. |downloads| image:: https://img.shields.io/pypi/dm/cgmail.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/cgmail

"A module that leverages pyzmail to parse email messages into json and parses urls out of the message body"

* Free software: BSD license

Installation
============

::

    pip install cgmail

Documentation
=============

https://py-cgmail.readthedocs.org/

Development
===========

To run the all tests run::

    tox
