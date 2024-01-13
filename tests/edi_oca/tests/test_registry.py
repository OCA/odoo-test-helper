# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.release import version_info
from odoo.tests.common import tagged

if version_info[0] < 15:
    from odoo.tests import SavepointCase as TransactionCase
else:
    # Odoo 15 and later: TransactionCase rolls back between tests
    from odoo.tests import TransactionCase

from odoo_test_helper import FakeModelLoader


@tagged("-at_install", "post_install")
class TestEdi(TransactionCase):
    def test_edi(self):
        loader = FakeModelLoader(self.env, "odoo.addons.edi_oca")
        loader.backup_registry()

        from .fake_models import EdiExchangeConsumerTest

        loader.update_registry((EdiExchangeConsumerTest,))
