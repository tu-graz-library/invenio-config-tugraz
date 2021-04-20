# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""
from flask import Blueprint

from . import config


class InvenioConfigTugraz(object):
    """invenio-config-tugraz extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-config-tugraz"] = self
        self.register_templates(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_CONFIG_TUGRAZ_"):
                app.config.setdefault(k, getattr(config, k))

    def register_templates(self, app):
        """Register this modules templates and rank before security module."""
        blueprint = Blueprint(
            __name__,
            __name__, template_folder='templates')
        app.register_blueprint(blueprint)

        # change blueprint order, if security module was registered before
        blueprints = app._blueprint_order
        our_index = None
        security_index = None

        for index, bp in enumerate(blueprints):
            if bp.name == "security":
                security_index = index
            if bp.name == __name__:
                our_index = index

        if (security_index is not None) and (our_index > security_index):
            temp = blueprints[security_index]
            blueprints[security_index] = blueprints[our_index]
            blueprints[our_index] = temp
