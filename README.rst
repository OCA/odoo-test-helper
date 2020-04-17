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
