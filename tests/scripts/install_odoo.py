#!/usr/bin/env python
import subprocess
import sys

odoo_branch = sys.argv[1]


def odoo_installed():
    try:
        import odoo  # noqa

        return True
    except ImportError:
        # odoo < 10
        try:
            import openerp  # noqa

            return True
        except ImportError:
            # odoo not installed
            return False


def install_odoo():
    if odoo_branch in ["10.0", "11.0", "12.0", "13.0"]:
        # setuptools 58 dropped support for 2to3, which is required
        # for dependencies of older Odoo versions
        subprocess.check_call(
            [
                "pip",
                "install",
                "setuptools<58",
            ]
        )
    url = f"https://github.com/odoo/odoo/archive/refs/heads/{odoo_branch}.tar.gz"
    req_url = (
        f"https://raw.githubusercontent.com/odoo/odoo/{odoo_branch}/requirements.txt"
    )
    subprocess.check_call(
        [
            "pip",
            "install",
            url,
        ]
    )
    subprocess.check_call(
        [
            "pip",
            "install",
            "-r",
            req_url,
        ]
    )


def main():
    if not odoo_installed():
        install_odoo()
    return sys.exit(0)


if __name__ == "__main__":
    main()
