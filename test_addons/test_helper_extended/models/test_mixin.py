# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TestMixin(models.AbstractModel):
    _inherit = "test.mixin"
    _description = "Test Mixin Extension"

    test_char_02 = fields.Char()
