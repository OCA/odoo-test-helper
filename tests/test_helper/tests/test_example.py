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


class TestMixin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestMixin, cls).setUpClass()

        # Creating a record before loading a fake model should work
        cls.env["res.partner"].create({"name": "Setup Class Foo"})

        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ResPartner

        cls.loader.update_registry((ResPartner,))

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super(TestMixin, cls).tearDownClass()

    def test_create(self):
        partner = self.env["res.partner"].create(
            {"name": "BAR", "test_char": "youhou", "extra2": "quod"}
        )
        self.assertEqual(partner.name, "FOO-BAR")
        self.assertEqual(partner.test_char, "youhou")
        self.assertEqual(partner.extra2, "quod")
