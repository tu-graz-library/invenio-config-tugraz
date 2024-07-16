# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from . import config
from .custom_fields import ip_network, single_ip


class InvenioConfigTugraz(object):
    """invenio-config-tugraz extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.add_custom_fields(app)
        app.extensions["invenio-config-tugraz"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_CONFIG_TUGRAZ_"):
                app.config.setdefault(k, getattr(config, k))

    def add_custom_fields(self, app):
        """Add custom fields."""
        app.config.setdefault("RDM_CUSTOM_FIELDS", [])
        app.config["RDM_CUSTOM_FIELDS"].append(ip_network)
        app.config["RDM_CUSTOM_FIELDS"].append(single_ip)


def finalize_app(app):
    """Finalize app."""
    rank_blueprint_higher(app)


def rank_blueprint_higher(app):
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
