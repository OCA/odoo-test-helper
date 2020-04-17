# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

long_description = []
with open(os.path.join("README.rst")) as f:
    long_description.append(f.read())
with open(os.path.join("CHANGES.rst")) as f:
    long_description.append(f.read())


setup(
    name="odoo-test-helper",
    description="Odoo Test Helper",
    long_description="\n".join(long_description),
    use_scm_version=True,
    packages=["odoo_test_helper"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    license="AGPLv3+",
    author="Akretion",
    author_email="contact@akretion.com",
    url="http://github.com/akretion/odoo-test-helper",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Odoo",
    ],
)
