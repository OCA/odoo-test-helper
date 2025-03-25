# -*- coding: utf-8 -*-
# Copyright 2020 Akretion (http://www.akretion.com).
# @author: Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TestMixin(models.AbstractModel):
    _name = "test.mixin"
    _description = "Test Mixin"

    test_char = fields.Char()

    @api.model
    def create(self, vals):
        vals["name"] = "FOO-{}".format(vals["name"])
        return super(TestMixin, self).create(vals)
