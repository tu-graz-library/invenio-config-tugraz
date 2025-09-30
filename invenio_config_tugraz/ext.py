# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from flask import Flask
from invenio_app_rdm.config import NOTIFICATIONS_BUILDERS
from invenio_curations.config import CURATIONS_FACETS, CURATIONS_NOTIFICATIONS_BUILDERS
from invenio_curations.services.events import CurationCommentEventType
from invenio_requests.customizations import LogEventType

from . import config
from .custom_fields import ip_network, single_ip


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
            if k.startswith("INVENIO_CONFIG_TUGRAZ_"):
                app.config.setdefault(k, getattr(config, k))

    def add_custom_fields(self, app: Flask) -> None:
        """Add custom fields."""
        app.config.setdefault("RDM_CUSTOM_FIELDS", [])
        app.config["RDM_CUSTOM_FIELDS"].append(ip_network)
        app.config["RDM_CUSTOM_FIELDS"].append(single_ip)


def finalize_app(app: Flask) -> None:
    """Finalize app."""
    rank_blueprint_higher(app)
    configure_curations(app)


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


def configure_curations(app: Flask) -> None:
    """Configurations needed for invenio-curations.

    Setup here because of potential package load timings.

    See https://github.com/tu-graz-library/invenio-curations.
    """

    # Enable notifications when a curation event happened.
    app.config["NOTIFICATIONS_BUILDERS"] = {
        **NOTIFICATIONS_BUILDERS,
        # Curation request
        **CURATIONS_NOTIFICATIONS_BUILDERS,
    }

    # Setup facets and request policies.
    app.config["REQUESTS_FACETS"] = CURATIONS_FACETS

    # Enable the creation and updating of request comments.
    app.config["CURATIONS_ENABLE_REQUEST_COMMENTS"] = True
    app.config["REQUESTS_REGISTERED_EVENT_TYPES"] = [
        LogEventType(),
        CurationCommentEventType(),
    ]
