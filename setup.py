# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
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
    "invenio-app>=1.3.0,<2.0.0",
]

# Should follow invenio-app-rdm
invenio_search_version = ">=1.4.0,<1.5.0"
invenio_db_version = ">=1.0.9,<1.1.0"

extras_require = {
    "elasticsearch7": [f"invenio-search[elasticsearch7]{invenio_search_version}"],
    "mysql": [f"invenio-db[mysql,versioning]{invenio_db_version}"],
    "postgresql": [f"invenio-db[postgresql,versioning]{invenio_db_version}"],
    "sqlite": [f"invenio-db[versioning]{invenio_db_version}"],
    "docs": [
        "Sphinx>=3",
    ],
    "tests": tests_require,
}

extras_require["all"] = []
for name, reqs in extras_require.items():
    if name[0] == ":" or name in (
        "elasticsearch7",
        "mysql",
        "postgresql",
        "sqlite",
    ):
        continue
    extras_require["all"].extend(reqs)

setup_requires = [
    "Babel>=1.3",
    "pytest-runner>=3.0.0,<5",
]

install_requires = [
    "Flask-BabelEx>=0.9.4",
    # keep this in sync with invenioRDM release
    "invenio_rdm_records>=0.28.0,<0.29.0",
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
        "invenio_base.blueprints": [
            "invenio_config_tugraz = invenio_config_tugraz.views:ui_blueprint",
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
