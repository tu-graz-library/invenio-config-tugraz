# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for TUGRAZ config."""

from flask import Blueprint, Flask, redirect
from werkzeug.wrappers import Response as BaseResponse


def ui_blueprint(app: Flask) -> Blueprint:
    """Blueprint for the routes and resources provided by invenio-config-tugraz."""
    routes = app.config.get("CONFIG_TUGRAZ_ROUTES")

    blueprint = Blueprint(
        "invenio_config_tugraz",
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    blueprint.add_url_rule(routes["guide"], view_func=guide)
    blueprint.add_url_rule(routes["terms"], view_func=terms)
    blueprint.add_url_rule(routes["gdpr"], view_func=gdpr)
    blueprint.add_url_rule(routes["accessibility"], view_func=accessibility)
    blueprint.add_url_rule(routes["file-formats"], view_func=file_formats)
    blueprint.add_url_rule(routes["curations"], view_func=curations)

    return blueprint


def guide() -> BaseResponse:
    """TUGraz_Repository_Guide."""
    return redirect("https://doi.org/10.3217/dgpcz-td505")


def terms() -> BaseResponse:
    """Terms_And_Conditions."""
    return redirect("https://doi.org/10.3217/k3dsw-rv326")


def gdpr() -> BaseResponse:
    """General_Data_Protection_Rights."""
    return redirect("https://doi.org/10.3217/xream-wzp39")


def accessibility() -> BaseResponse:
    """Accessibility_Statement."""
    return redirect("https://doi.org/10.3217/psmeb-84429")


def file_formats() -> BaseResponse:
    """File_Formats."""
    return redirect("https://doi.org/10.3217/3c0k5-zqh95")


def curations() -> BaseResponse:
    """Curation_Workflow."""
    return redirect("https://doi.org/10.3217/h1zfa-4fb59")
