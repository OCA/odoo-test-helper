# -*- coding: utf-8 -*-
# Copyright 2020 Akretion (http://www.akretion.com).
# @author: Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.release import version_info

if version_info[0] < 15:
    from odoo.tests import SavepointCase as TransactionCase
else:
    # Odoo 15 and later: TransactionCase rolls back between tests
    from odoo.tests import TransactionCase

from odoo_test_helper import FakeModelLoader


class TestExample(TransactionCase):
    def setUp(self):
        super(TestExample, self).setUp()

        # Creating a record before loading a fake model should work
        self.env["res.partner"].create({"name": "Setup Class Foo"})

        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .models import ResPartner

        self.loader.update_registry((ResPartner,))

    def tearDown(self):
        self.loader.restore_registry()
        super(TestExample, self).tearDown()

    def test_create(self):
        partner = self.env["res.partner"].create(
            {"name": "BAR", "test_char": "youhou", "extra2": "quod"}
        )
        self.assertEqual(partner.name, "FOO-BAR")
        self.assertEqual(partner.test_char, "youhou")
        self.assertEqual(partner.extra2, "quod")
