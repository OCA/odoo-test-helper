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

* `test_example.py <https://github.com/akretion/odoo-test-helper/blob/master/tests/test_helper/tests/test_example.py>`_.

This example load the class ResPartner from the file:

* `models.py <https://github.com/akretion/odoo-test-helper/blob/master/tests/test_helper/tests/models.py>`_.


Real implementation case can be found in the following module

* `connector_search_engine <https://github.com/OCA/search-engine/tree/12.0/connector_search_engine>`_.
* `base_url <https://github.com/shopinvader/odoo-shopinvader/tree/12.0/base_url>`_.


Contributor
~~~~~~~~~~~~

* Sébastien BEAU <sebastien.beau@akretion.com>
* Laurent Mignon <laurent.mignon@acsone.eu>
* Simone Orsi <simone.orsi@camptocamp.com>


History
~~~~~~~~

This module is inspired of the following mixin code that can be found in OCA and shopinvader repository

* Mixin in OCA: https://github.com/OCA/search-engine/blob/7fd85a74180cfff30e212fca01ebeba6c54ee294/connector_search_engine/tests/models_mixin.py

* Mixin in Shopinvader: https://github.com/shopinvader/odoo-shopinvader/blob/b81b921ea52c911e5b33afac88adb8f9a1c02626/base_url/tests/models_mixin.py

Intial Authors are

* Laurent Mignon <laurent.mignon@acsone.eu>
* Simone Orsi <simone.orsi@camptocamp.com>

Refactor/extraction have been done by

* Sébastien BEAU <sebastien.beau@akretion.com>

This refactor try to load all class correctly like Odoo does with the exact same syntax

Note this refactor/extraction have been done to fix the test of the following issue

https://github.com/shopinvader/odoo-shopinvader/pull/607
