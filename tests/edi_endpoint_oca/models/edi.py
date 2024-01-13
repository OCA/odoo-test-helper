# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EDIExchangeRecord(models.Model):
    _inherit = "edi.exchange.record"

    edi_endpoint_id = fields.Many2one(
        comodel_name="edi.endpoint",
        readonly=True,
        string="Endpoint",
        help="Record generated via this endpoint",
    )


class EDIEndpoint(models.Model):
    _name = "edi.endpoint"


class EDIExchangeConsumerMixin(models.AbstractModel):
    _inherit = "edi.exchange.consumer.mixin"

    origin_edi_endpoint_id = fields.Many2one(
        string="EDI origin endpoint",
        comodel_name="edi.endpoint",
        ondelete="set null",
        related="origin_exchange_record_id.edi_endpoint_id",
        # Store it to ease searching
        store=True,
    )
