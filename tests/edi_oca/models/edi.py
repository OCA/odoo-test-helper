# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EDIExchangeRecord(models.Model):
    _name = "edi.exchange.record"


class EDIExchangeConsumerMixin(models.AbstractModel):
    _name = "edi.exchange.consumer.mixin"

    origin_exchange_record_id = fields.Many2one(
        string="EDI origin record",
        comodel_name="edi.exchange.record",
        ondelete="set null",
        help="EDI record that originated this document.",
    )
