odoo-test-helper
=================

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. image:: https://badge.fury.io/py/odoo-test-helper.svg
    :target: http://badge.fury.io/py/odoo-test-helper

odoo-test-helper is box tool for writing odoo test


Loading Fake model
~~~~~~~~~~~~~~~~~~~~~~

Sometime you build an abstract module that can be use by many module.
If you want to test it, most of the time you can not write test in this module.
Because your module is so abtract that you can do anything without real implementation.
One solution is to create a "test" module with a little implementation that use you abstract module.
One other solution is to include models and load then in your test.
This lib add a model loader for the test.

Example
~~~~~~~~~

There is an example of test here:
[test_example.py](test/test_helper/tests/test_example.py)

This example load the class ResPartner from the file
[models.py](test/test_helper/tests/models.py)


Real implementation case can be found in the following module

[connector_search_engine](https://github.com/OCA/search-engine/tree/12.0/connector_search_engine)
[base_url](https://github.com/shopinvader/odoo-shopinvader/tree/12.0/base_url)
