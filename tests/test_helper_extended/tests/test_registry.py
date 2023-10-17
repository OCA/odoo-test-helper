# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.release import version_info

if version_info[0] >= 15:
    from odoo.tests import TransactionCase

    from odoo_test_helper import FakeModelLoader

    class TestMixin(TransactionCase):
        def test_mixin_after_reloading_parent_module(self):
            self.assertIn("test.mixin", self.env.registry)
            self.assertIn("test_char", self.env["test.mixin"]._fields)
            self.assertIn("test_char_02", self.env["test.mixin"]._fields)

            loader = FakeModelLoader(self.env, "odoo.addons.test_helper")
            loader.backup_registry()

            # trigger reload of parent module: test_helper
            loader.update_registry(())

            self.assertIn("test.mixin", self.env.registry)
            self.assertIn("test_char", self.env["test.mixin"]._fields)
            # new field should not be there anymore
            self.assertNotIn("test_char_02", self.env["test.mixin"]._fields)

            # but now we restore registry
            loader.restore_registry()

            self.assertIn("test.mixin", self.env.registry)
            self.assertIn("test_char", self.env["test.mixin"]._fields)
            # new field should be there again
            self.assertIn("test_char_02", self.env["test.mixin"]._fields)
