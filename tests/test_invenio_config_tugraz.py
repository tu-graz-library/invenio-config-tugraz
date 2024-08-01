# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask
from invenio_saml.handlers import acs_handler_factory, default_account_setup

from invenio_config_tugraz import InvenioConfigTugraz


def test_version() -> None:
    """Test version import."""
    from invenio_config_tugraz import __version__

    assert __version__


def test_init() -> None:
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioConfigTugraz(app)
    assert "invenio-config-tugraz" in app.extensions

    app = Flask("testapp")
    ext = InvenioConfigTugraz()
    assert "invenio-config-tugraz" not in app.extensions
    ext.init_app(app)
    assert "invenio-config-tugraz" in app.extensions


def test_create_acs_handler() -> None:
    """Just to see whether creating acs_handlers breaks CI..."""
    acs_handler = acs_handler_factory("idp", account_setup=default_account_setup)
    assert callable(acs_handler)
