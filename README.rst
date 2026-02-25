odoo-test-helper
================

.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. image:: https://badge.fury.io/py/odoo-test-helper.svg
    :target: http://badge.fury.io/py/odoo-test-helper

odoo-test-helper is a toolbox for writing odoo tests.

IMPORTANT: This library is not needed for Odoo 19+. You can achieve the same using native
code. See https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-19.0 for
the explanation looking for `odoo-test-helper` text.

Loading Fake models
~~~~~~~~~~~~~~~~~~~

Sometimes, you build an abstract module that can be use by many modules.
In such case, if you want to test it with real records, you need to register real models.

One solution is to create a `module_test` module
with a little implementation that use your abstract model.

Other solution is to define test only models and load them in tests.
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

How to import
~~~~~~~~~~~~~~~

Be careful importing the fake class. It must be done in the right way.
Importing a file will automatically add all the class in the "module_to_models"
variable. The import **must** be done after the backup !

Wrong way
----------

.. code-block:: python

   from odoo.tests import SavepointCase

   from odoo_test_helper import FakeModelLoader

   # The fake class is imported here !! It's wrong
   # And be carefull even if you only import ResPartner
   # all class in the file models will be proceded by odoo
   # so no **direct import** of a file that contain fake model
   from .models import ResPartner


   class FakeModel(SavepointCase):
       @classmethod
       def setUpClass(cls):
           super(FakeModel, cls).setUpClass()
           cls.loader = FakeModelLoader(cls.env, cls.__module__)
           cls.loader.backup_registry()

           cls.loader.update_registry((ResPartner,))

       @classmethod
       def tearDownClass(cls):
           cls.loader.restore_registry()
           super(FakeModel, cls).tearDownClass()

       def test_create(self):
           partner = self.env["res.partner"].create({"name": "BAR", "test_char": "youhou"})
           self.assertEqual(partner.name, "FOO-BAR")
           self.assertEqual(partner.test_char, "youhou")

Right Way (up to v17)
---------------------

.. code-block:: python

    from odoo.tests import SavepointCase

    from odoo_test_helper import FakeModelLoader


    class FakeModel(SavepointCase):
        @classmethod
        def setUpClass(cls):
            super(FakeModel, cls).setUpClass()
            cls.loader = FakeModelLoader(cls.env, cls.__module__)
            cls.loader.backup_registry()

            # The fake class is imported here !! After the backup_registry
            from .models import ResPartner

            cls.loader.update_registry((ResPartner,))

        @classmethod
        def tearDownClass(cls):
            cls.loader.restore_registry()
            super(FakeModel, cls).tearDownClass()

        def test_create(self):
            partner = self.env["res.partner"].create({"name": "BAR", "test_char": "youhou"})
            self.assertEqual(partner.name, "FOO-BAR")
            self.assertEqual(partner.test_char, "youhou")

Right Way (v18)
---------------

.. code-block:: python

    from odoo.tests import TransactionCase

    from odoo_test_helper import FakeModelLoader


    class FakeModel(TransactionCase):
        def setUp(self):
            super().setUp()
            self.loader = FakeModelLoader(self.env, self.__module__)
            self.loader.backup_registry()

            # The fake class is imported here !! After the backup_registry
            from .models import ResPartner

            self.loader.update_registry((ResPartner,))

        def tearDown(self):
            self.loader.restore_registry()
            super().tearDown()

        def test_create(self):
            partner = self.env["res.partner"].create({"name": "BAR", "test_char": "youhou"})
            self.assertEqual(partner.name, "FOO-BAR")
            self.assertEqual(partner.test_char, "youhou")

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
