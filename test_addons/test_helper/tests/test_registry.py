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
    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()

    def test_update_and_restore(self):
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)
        from .models import ResPartner, ResPartnerExtra

        self.loader.update_registry([ResPartner, ResPartnerExtra])
        self.assertIn("res.partner.extra", self.env.registry)
        self.assertIn("test_char", self.env["res.partner"]._fields)
        self.loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)

    def test_load_res_partner(self):
        self.loader.backup_registry()

        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("extra2", self.env["res.partner"]._fields)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)

        from .models import ResPartner

        self.loader.update_registry([ResPartner])

        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertIn("extra2", self.env["res.partner"]._fields)
        self.assertIn("test_char", self.env["res.partner"]._fields)

        self.loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("extra2", self.env["res.partner"]._fields)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)

    def test_load_res_partner_extra(self):
        self.loader.backup_registry()

        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)

        from .models import ResPartnerExtra

        self.loader.update_registry([ResPartnerExtra])

        self.assertIn("res.partner.extra", self.env.registry)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)

        self.loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("test_char", self.env["res.partner"]._fields)
