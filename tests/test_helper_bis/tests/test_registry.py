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
    def test_update_and_restore(self):
        """
        Ensure that a test model defined into an addon without model
        is correctly removed from the registry after the test.
        """
        loader = FakeModelLoader(self.env, self.__module__)
        loader.backup_registry()
        from .models import ResPartner, ResPartnerExtra

        self.assertNotIn("res.partner.extra", self.env.registry)

        loader.update_registry([ResPartner, ResPartnerExtra])
        self.assertIn("res.partner.extra", self.env.registry)

        loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)

    def test_load_res_partner(self):
        """
        Check that a model extended by a test model in an addon without models
        is correctly reset after the test.
        """
        loader = FakeModelLoader(self.env, self.__module__)
        loader.backup_registry()

        self.assertIn("res.partner", self.env.registry)
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("extra2", self.env["res.partner"]._fields)

        from .models import ResPartner

        loader.update_registry([ResPartner])

        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertIn("extra2", self.env["res.partner"]._fields)

        loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)
        self.assertNotIn("extra2", self.env["res.partner"]._fields)
        self.assertIn("res.partner", self.env.registry)

    def test_load_res_partner_extra(self):
        loader = FakeModelLoader(self.env, self.__module__)
        loader.backup_registry()

        self.assertNotIn("res.partner.extra", self.env.registry)

        from .models import ResPartnerExtra

        loader.update_registry([ResPartnerExtra])

        self.assertIn("res.partner.extra", self.env.registry)
        self.assertNotIn("extra2", self.env["res.partner"]._fields)

        loader.restore_registry()
        self.assertNotIn("res.partner.extra", self.env.registry)
