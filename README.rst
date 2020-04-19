odoo-test-helper
================

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. image:: https://badge.fury.io/py/odoo-test-helper.svg
    :target: http://badge.fury.io/py/odoo-test-helper

odoo-test-helper is toolbox for writing odoo test


Loading Fake models
~~~~~~~~~~~~~~~~~~~

Sometime you build an abstract module that can be use by many modules.
In such case, if you want to test it with real records you need to register real models.

One solution is to create a `module_test` module
with a little implementation that use your abstract model.

One other solution is define test only models and load them in tests.
This lib makes this possible and easy.

Example
~~~~~~~

There is an example of test here:
[test_example.py](test/test_helper/tests/test_example.py)

This example load the class ResPartner from the file
[models.py](test/test_helper/tests/models.py)


Real implementation case can be found in the following module

[connector_search_engine](https://github.com/OCA/search-engine/tree/12.0/connector_search_engine)
[base_url](https://github.com/shopinvader/odoo-shopinvader/tree/12.0/base_url)
