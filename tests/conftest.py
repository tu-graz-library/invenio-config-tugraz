# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_db import InvenioDB, db
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from invenio_config_tugraz import InvenioConfigTugraz


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture()
def create_app(request):
    """Basic Flask application."""
    instance_path = tempfile.mkdtemp()
    app = Flask("testapp")
    DB = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")
    app.config.update(
        INVENIO_CONFIG_TUGRAZ_SINGLE_IP=["127.0.0.1", "127.0.0.2"],
        INVENIO_CONFIG_TUGRAZ_IP_RANGES=[
            ["127.0.0.2", "127.0.0.99"],
            ["127.0.1.3", "127.0.1.5"],
        ],
        SQLALCHEMY_DATABASE_URI=DB,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    Babel(app)
    InvenioConfigTugraz(app)
    InvenioDB(app)

    with app.app_context():
        db_url = str(db.engine.url)
        if db_url != "sqlite://" and not database_exists(db_url):
            create_database(db_url)
        db.create_all()

    def teardown():
        with app.app_context():
            db_url = str(db.engine.url)
            db.session.close()
            if db_url != "sqlite://":
                drop_database(db_url)
            shutil.rmtree(instance_path)

    request.addfinalizer(teardown)
    app.test_request_context().push()

    return app


@pytest.fixture(scope='function')
def open_record():
    """Open record data as dict coming from the external world."""
    return {
        "access": {
            "metadata": False,
            "files": False,
            "owned_by": [1],
            "access_right": "open"
        },
        "metadata": {
            "publication_date": "2020-06-01",
            "resource_type": {
                "type": "image",
                "subtype": "image-photo"
            },
            # Technically not required
            "creators": [{
                "name": "Troy Brown",
                "type": "personal"
            }, {
                "name": "Phillip Lester",
                "type": "personal",
                "identifiers": {"orcid": "0000-0002-1825-0097"},
                "affiliations": [{
                    "name": "Carter-Morris",
                    "identifiers": {"ror": "03yrm5c26"}
                }]
            }, {
                "name": "Steven Williamson",
                "type": "personal",
                "identifiers": {"orcid": "0000-0002-1825-0097"},
                "affiliations": [{
                    "name": "Ritter and Sons",
                    "identifiers": {"ror": "03yrm5c26"}
                }, {
                    "name": "Montgomery, Bush and Madden",
                    "identifiers": {"ror": "03yrm5c26"}
                }]
            }],
            "title": "A Romans story"
        }
    }


@pytest.fixture(scope='function')
def singleip_record():
    """Single Ip record data as dict coming from the external world."""
    return {
        "access": {
            "metadata": False,
            "files": False,
            "owned_by": [1],
            "access_right": "singleip"
        },
        "metadata": {
            "publication_date": "2020-06-01",
            "resource_type": {
                "type": "image",
                "subtype": "image-photo"
            },
            # Technically not required
            "creators": [{
                "name": "Troy Brown",
                "type": "personal"
            }, {
                "name": "Phillip Lester",
                "type": "personal",
                "identifiers": {"orcid": "0000-0002-1825-0097"},
                "affiliations": [{
                    "name": "Carter-Morris",
                    "identifiers": {"ror": "03yrm5c26"}
                }]
            }, {
                "name": "Steven Williamson",
                "type": "personal",
                "identifiers": {"orcid": "0000-0002-1825-0097"},
                "affiliations": [{
                    "name": "Ritter and Sons",
                    "identifiers": {"ror": "03yrm5c26"}
                }, {
                    "name": "Montgomery, Bush and Madden",
                    "identifiers": {"ror": "03yrm5c26"}
                }]
            }],
            "title": "A Romans story"
        }
    }
