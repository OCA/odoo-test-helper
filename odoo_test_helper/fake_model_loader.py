# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE (http://www.acsone.eu).
# @author: Laurent Mignon <laurent.mignon@acsone.eu>
# Copyright 2018 Camptocamp SA (http://www.camptocamp.com).
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# Copyright 2020 Akretion (http://www.akretion.com).
# @author: Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import models
from odoo.release import version_info
from odoo.tools import OrderedSet

try:
    from unittest import mock
except ImportError:
    import mock

from .whitelist import WHITELIST

module_to_models = models.MetaModel.module_to_models
_logger = logging.getLogger(__name__)


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
        if hasattr(self.env.registry["base"], "_get_addon_name"):
            # Only before V14
            self._module_name = self.env.registry["base"]._get_addon_name(__module__)
        else:
            self._module_name = __module__.split(".")[2]

    def _check_wrong_import(self):
        version = str(version_info[0])
        modules_to_ignore = WHITELIST.get(version, [])
        for module, odoo_models in module_to_models.items():
            for model in odoo_models:
                module_path = model.__module__
                path = module_path.split(".")
                if module_path not in modules_to_ignore and path[3] == "tests":
                    _logger.warning(
                        "Wrong Import in module {}, the class {} have been already "
                        "imported.\nPlease take a look to the README on how to "
                        "import test class".format(module, model)
                    )

    def backup_registry(self):
        self._check_wrong_import()
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
        # Since V13 field are computed at the end
        # In the setup of your test if you create or modify a record that
        # need to be recomputed we need to recompute them before reloading
        # the registry
        if hasattr(self.env, "flush_all"):  # Odoo 16 and later
            self.env.flush_all()
        elif hasattr(self.env.all, "tocompute"):
            to_recompute_models = set()
            for field, _vals in self.env.all.tocompute.items():
                to_recompute_models.add(field.model_name)
            for model in to_recompute_models:
                self.env[model].recompute()

        # In case that you are re-using fake model from an other module
        # Odoo have already modify the module_to_models variable
        # It updated everytime we import a python file
        # So we need first to clean this variable
        # then we can inject the fake class in the module_to_models
        # so we can reload the registry correctly with only the given class
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
            if hasattr(model, "_BaseModel__base_classes"):  # As of 15.0
                model._BaseModel__base_classes = ori["base"]
            model.__bases__ = ori["base"]
            model._inherit_children = ori["_inherit_children"]
            model._inherits_children = ori["_inherits_children"]
            for field in model._fields:
                if field not in ori["_fields"]:
                    if hasattr(model, field):
                        delattr(model, field)
            model._fields = ori["_fields"]

        # delete 1st models w/out children
        sorted_models = sorted(
            self.env.registry.models.items(), key=lambda x: x[1]._inherit_children
        )
        for name, __ in sorted_models:
            if name not in self._original_registry:
                del self.env.registry.models[name]

        self._clean_module_to_model()

        # reload is need to reset correctly the field on the record
        with mock.patch.object(self.env.cr, "commit"):
            # Only before V15
            if hasattr(self.env.registry, "model_cache"):
                self.env.registry.model_cache.clear()
            model_names = self.env.registry.load(
                self.env.cr, FakePackage(self._module_name)
            )
            self.env.registry.setup_models(self.env.cr)
            self.env.registry.init_models(
                self.env.cr, model_names, {"module": self._module_name}
            )
