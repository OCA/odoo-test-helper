# -*- coding: utf-8 -*-
# Copyright 2020 Akretion (http://www.akretion.com).
# @author: Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = ["res.partner", "test.mixin"]
    _name = "res.partner"

    extra2 = fields.Char()


class ResPartnerExtra(models.Model):
    _name = "res.partner.extra"
    _description = "Res Partner Extra"

    partner_id = fields.Many2one("res.partner", "Partner")
    extra = fields.Char()
