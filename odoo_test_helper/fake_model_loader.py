# -*- coding: utf-8 -*-

import mock
from odoo import models
from odoo.tools import OrderedSet

module_to_models = models.MetaModel.module_to_models


class FakePackage(object):  # noqa
    def __init__(self, name):
        self.name = name


class FakeModelLoader(object):
    """Loader for Odoo tests fake models.

    Usage on SavepointTestCase:

        from odoo_test_helper import FakeModelLoader

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.loader = FakeModelLoader(cls.env, cls.__module__)
            cls.loader.backup_registry()
            from .fake_models import MyFakeModelClass1, MyFakeModelClass2
            cls.loader.update_registry(
                (MyFakeModelClass1, MyFakeModelClass2)
            )

        @classmethod
        def tearDownClass(cls):
            cls.loader.restore_registry()
            super().tearDownClass()

    Usage on TransactionCase / HttpCase:

        from odoo_test_helper import FakeModelLoader

        def setUp(self):
            super().setUp()
            self.loader = FakeModelLoader(self.env, self.__module__)
            self.loader.backup_registry()
            from .fake_models import MyFakeModelClass1, MyFakeModelClass2
            self.loader.update_registry(
                (MyFakeModelClass1, MyFakeModelClass2)
            )

        def tearDown(self):
            self.loader.restore_registry()
            super().tearDown()
    """

    _original_registry = None
    _original_module2modules = None
    _module_name = None

    def __init__(self, env, __module__):
        self.env = env
        self._module_name = self.env.registry["base"]._get_addon_name(__module__)

    def backup_registry(self):
        self._original_registry = {}
        self._original_module_to_models = {}
        for model_name, model in self.env.registry.models.items():
            self._original_registry[model_name] = {
                "base": model.__bases__,
                "_fields": model._fields.copy(),
                "_inherit_children": OrderedSet(model._inherit_children._map.keys()),
                "_inherits_children": set(model._inherits_children),
            }
        for key in module_to_models:
            self._original_module_to_models[key] = list(module_to_models[key])

    def _clean_module_to_model(self):
        for key in self._original_module_to_models:
            module_to_models[key] = list(self._original_module_to_models[key])

    def update_registry(self, odoo_models):
        # Ensure that fake model are in your module
        # If you test are re-using fake model form an other module
        # the following code will inject it like it was in your module
        self._clean_module_to_model()

        for model in odoo_models:
            if model not in module_to_models[self._module_name]:
                module_to_models[self._module_name].append(model)

        with mock.patch.object(self.env.cr, "commit"):
            model_names = self.env.registry.load(
                self.env.cr, FakePackage(self._module_name)
            )
            self.env.registry.setup_models(self.env.cr)
            self.env.registry.init_models(
                self.env.cr, model_names, {"module": self._module_name}
            )

    def restore_registry(self):
        for key in self._original_registry:
            ori = self._original_registry[key]
            model = self.env.registry[key]
            model.__bases__ = ori["base"]
            model._inherit_children = ori["_inherit_children"]
            model._inherits_children = ori["_inherits_children"]
            for field in model._fields:
                if field not in ori["_fields"]:
                    if hasattr(model, field):
                        delattr(model, field)
            model._fields = ori["_fields"]

        for key in list(self.env.registry.models.keys()):
            if key not in self._original_registry:
                del self.env.registry.models[key]

        self._clean_module_to_model()

        # reload is need to resetup correctly the field on the record
        with mock.patch.object(self.env.cr, "commit"):
            self.env.registry.model_cache.clear()
            model_names = self.env.registry.load(
                self.env.cr, FakePackage(self._module_name)
            )
            self.env.registry.setup_models(self.env.cr)
            self.env.registry.init_models(
                self.env.cr, model_names, {"module": self._module_name}
            )
