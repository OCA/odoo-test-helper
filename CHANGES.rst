Changes
~~~~~~~

.. Future (?)
.. ----------
.. - ...

2.1.0
-----

- [IMP] Allow to ignore Odoo core modules to avoid warning

2.0.5
-----

- .gitignore added

2.0.4
-----

- [FIX] AttributeError in Odoo 15+, regression introduced in 2.0.3

2.0.3
-----

- [FIX] restore_registry in Odoo 16

    See odoo/odoo@cd12293

    This new attribute is the source of truth for the base classes
    and in setup_models (called further down in the modified code in this PR),
    the model's base classes are reset from it:

    https://github.com/odoo/odoo/blob/e1f06479a526c703ccabc441b1e194646206b966/odoo/models.py#L2728-L2730.

    The test failure fixed by this PR can be inspected in
    https://app.travis-ci.com/github/OCA/odoo-test-helper/builds/258453331


2.0.2
-----

- Fix ``mock`` import for v15

2.0.1
-----

- Fix support for Odoo 15.0


2.0.0
-----

- Move to OCA
- Re-license to LGPL


1.1.0
-----

- Refactoring (misc imp/fix)


1.0.0
-----

- Initial release
