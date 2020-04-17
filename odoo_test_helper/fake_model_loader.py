# -*- coding: utf-8 -*-

import mock
from odoo import models
from odoo.tools import OrderedSet

module_to_models = models.MetaModel.module_to_models


class FakePackage(object):  # noqa
    def __init__(self, name):
        self.name = name


class FakeModelLoader(object):

    _original_registry = None
    _original_module2modules = None
    _module_name = None

    @classmethod
    def _backup_registry(cls):
        cls._module_name = cls.env.registry["base"]._get_addon_name(cls.__module__)
        cls._original_registry = {}
        cls._original_module_to_models = {}
        for model_name, model in cls.env.registry.models.items():
            cls._original_registry[model_name] = {
                "base": model.__bases__,
                "_fields": model._fields.copy(),
                "_inherit_children": OrderedSet(model._inherit_children._map.keys()),
                "_inherits_children": set(model._inherits_children),
            }
        for key in module_to_models:
            cls._original_module_to_models[key] = list(module_to_models[key])

    @classmethod
    def _update_registry(cls, odoo_models):
        # Ensure that fake model are in your module
        # If you test are re-using fake model form an other module
        # the following code will inject it like it was in your module
        for model in odoo_models:
            if model not in module_to_models[cls._module_name]:
                module_to_models[cls._module_name].append(model)

        with mock.patch.object(cls.env.cr, "commit"):
            model_names = cls.env.registry.load(
                cls.env.cr, FakePackage(cls._module_name)
            )
            cls.env.registry.setup_models(cls.env.cr)
            cls.env.registry.init_models(
                cls.env.cr, model_names, {"module": cls._module_name}
            )

    @classmethod
    def _restore_registry(cls):
        for key in cls._original_registry:
            ori = cls._original_registry[key]
            model = cls.env.registry[key]
            model.__bases__ = ori["base"]
            model._inherit_children = ori["_inherit_children"]
            model._inherits_children = ori["_inherits_children"]
            for field in model._fields:
                if field not in ori["_fields"]:
                    if hasattr(model, field):
                        delattr(model, field)
            model._fields = ori["_fields"]
        for key, _model in cls.env.registry.models.items():
            if key not in cls._original_registry:
                del cls.env.registry.models[key]

        for key in cls._original_module_to_models:
            module_to_models[key] = cls._original_module_to_models[key]

        # reload is need to resetup correctly the field on the record
        with mock.patch.object(cls.env.cr, "commit"):
            cls.env.registry.model_cache.clear()
            model_names = cls.env.registry.load(
                cls.env.cr, FakePackage(cls._module_name)
            )
            cls.env.registry.setup_models(cls.env.cr)
            cls.env.registry.init_models(
                cls.env.cr, model_names, {"module": cls._module_name}
            )
