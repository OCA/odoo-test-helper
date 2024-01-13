# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "edi.exchange.consumer.mixin"]

    edi_disable_auto = fields.Boolean(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
