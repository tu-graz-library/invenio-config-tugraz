# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from flask import Flask
from flask_login import login_required

from . import config
from .custom_fields import ip_network, single_ip
from .views import (
    require_tugraz_authenticated_else_redirect,
    require_tugraz_authenticated_else_render,
)


class InvenioConfigTugraz:
    """invenio-config-tugraz extension."""

    def __init__(self, app: Flask = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_config(app)
        self.add_custom_fields(app)
        app.extensions["invenio-config-tugraz"] = self

    def init_config(self, app: Flask) -> None:
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("CONFIG_TUGRAZ_") or k == "OVERRIDE_INSTANCE_TYPE":
                app.config.setdefault(k, getattr(config, k))

    def add_custom_fields(self, app: Flask) -> None:
        """Add custom fields."""
        app.config.setdefault("RDM_CUSTOM_FIELDS", [])
        app.config["RDM_CUSTOM_FIELDS"].append(ip_network)
        app.config["RDM_CUSTOM_FIELDS"].append(single_ip)


def finalize_app(app: Flask) -> None:
    """Finalize app."""
    rank_blueprint_higher(app)
    guard_view_functions(app)


def guard_view_functions(app: Flask) -> None:
    """Guard view-functions against unauthenticated access."""
    endpoint_guards = {
        "invenio_app_rdm_users.communities": [
            login_required,
            require_tugraz_authenticated_else_redirect,
        ],
        "invenio_app_rdm_users.requests": [
            login_required,
            require_tugraz_authenticated_else_redirect,
        ],
        "invenio_app_rdm_users.uploads": [
            login_required,
            require_tugraz_authenticated_else_render,
        ],
        "invenio_records_lom.uploads": [
            login_required,
            # No tugraz_authenticated check here — LOM's own view handles it:
            # users with oer_certified_user see the dashboard,
            # everyone else (incl. edugain) sees not_licensed_text.html
        ],
        "invenio_records_marc21.uploads_marc21": [
            login_required,
            require_tugraz_authenticated_else_redirect,
        ],
    }

    for endpoint, guarding_decorators in endpoint_guards.items():
        view_func = app.view_functions.get(endpoint)
        if not view_func:
            continue

        for guarding_decorator in reversed(guarding_decorators):
            view_func = guarding_decorator(view_func)

        app.view_functions[endpoint] = view_func


def rank_blueprint_higher(app: Flask) -> None:
    """Rank this module's blueprint higher than blueprint of security module.

    Needed in order to overwrite email templates.

    Since the blueprints are in a dict and the order of insertion is
        retained, popping and reinserting all items (except ours), ensures
        our blueprint will be in front.
    """
    bps = app.blueprints
    for blueprint_name in list(bps.keys()):
        if blueprint_name != "invenio_config_tugraz":
            bps.update({blueprint_name: bps.pop(blueprint_name)})
