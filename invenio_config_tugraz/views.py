# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
#
# invenio-theme-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for TUGRAZ config."""

from os import environ
from typing import Dict

from elasticsearch_dsl.utils import AttrDict
from flask import Blueprint, current_app


def ui_blueprint(app):
    """Blueprint for the routes and resources provided by invenio-config-tugraz."""
    blueprint = Blueprint(
        "invenio_config_tugraz",
        __name__,
        template_folder="templates",
    )

    @blueprint.before_app_first_request
    def rank_higher():
        """Rank this modules blueprint higher than blueprint of security module."""
        blueprints = current_app._blueprint_order
        our_index = None
        security_index = None

        for index, bp in enumerate(blueprints):
            print(bp.name)
            if bp.name == "security":
                security_index = index
            if bp.name == "invenio_config_tugraz":
                our_index = index

        if (security_index is not None) and (our_index > security_index):
            temp = blueprints[security_index]
            blueprints[security_index] = blueprints[our_index]
            blueprints[our_index] = temp

    @blueprint.app_template_filter("make_dict_like")
    def make_dict_like(value: str, key: str) -> Dict[str, str]:
        """Convert the value to a dict like structure.

        in the form of a key -> value pair.
        """
        return {key: value}

    @blueprint.app_template_filter("cast_to_dict")
    def cast_to_dict(attr_dict):
        """Return the dict structure of AttrDict variable."""
        return AttrDict.to_dict(attr_dict)

    return blueprint
