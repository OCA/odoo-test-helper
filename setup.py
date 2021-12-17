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

LICENSE = "GNU Lesser General Public License v3 or later (LGPLv3+)"

setup(
    name="odoo-test-helper",
    use_scm_version=True,
    description="Odoo Test Helper",
    long_description="\n".join(long_description),
    long_description_content_type="text/x-rst",
    packages=["odoo_test_helper"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
    license="LGPLv3+",
    author="Odoo Community Association (OCA)",
    author_email="support@odoo-community.org",
    url="http://github.com/OCA/odoo-test-helper",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: " + LICENSE,
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Odoo",
    ],
)
