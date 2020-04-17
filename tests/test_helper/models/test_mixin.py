# -*- coding: utf-8 -*-
# Copyright 2020 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TestMixin(models.AbstractModel):
    _name = "test.mixin"

    test_char = fields.Char()

    @api.model
    def create(self, vals):
        vals["name"] = "FOO-{}".format(vals["name"])
        return super(TestMixin, self).create(vals)
