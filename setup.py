# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "pytest-invenio>=1.4.0",
    "SQLAlchemy-Utils>=0.33.1,<0.36",
    "invenio-rdm-records~=0.20.8",
    "invenio-search[elasticsearch7]>=1.4.0",
    "psycopg2-binary>=2.8.6",
]

extras_require = {
    "docs": [
        "Sphinx>=3",
    ],
    "tests": tests_require,
}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup_requires = [
    "Babel>=1.3",
    "pytest-runner>=3.0.0,<5",
]

install_requires = [
    "Flask-BabelEx>=0.9.4",
    "elasticsearch_dsl>=7.2.1",
    "sqlalchemy-continuum>=1.3.11",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("invenio_config_tugraz", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="invenio-config-tugraz",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio, config, Tu Graz",
    license="MIT",
    author="Mojib Wali",
    author_email="mb_wali@hotmail.com",
    url="https://github.com/tu-graz-library/invenio-config-tugraz",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_base.apps": [
            "invenio_config_tugraz = invenio_config_tugraz:InvenioConfigTugraz",
        ],
        "invenio_i18n.translations": [
            "messages = invenio_config_tugraz",
        ],
        "invenio_config.module": [
            "invenio_config_tugraz = invenio_config_tugraz.config",
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
    ],
)
