# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for TUGRAZ config."""

from collections.abc import Callable
from functools import wraps

from flask import Blueprint, Flask, g, redirect, render_template, url_for
from flask_login import current_user
from invenio_rdm_records.proxies import current_rdm_records
from invenio_users_resources.proxies import current_user_resources
from werkzeug.wrappers import Response as BaseResponse


def current_identity_is_tugraz_authenticated() -> bool:
    """Check whether the current identity has TU Graz authentication."""
    rdm_service = current_rdm_records.records_service
    return rdm_service.check_permission(g.identity, "tugraz_authenticated")


def require_tugraz_authenticated_else_redirect[**P, R](
    view_func: Callable[P, R],
) -> Callable[P, R]:
    """Redirect unauthenticated users to the uploads page."""

    @wraps(view_func)
    def decorated_view(*args: P.args, **kwargs: P.kwargs) -> R:
        if not current_identity_is_tugraz_authenticated():
            return redirect(url_for("invenio_app_rdm_users.uploads"))
        return view_func(*args, **kwargs)

    return decorated_view


def require_tugraz_authenticated_else_render[**P, R](
    view_func: Callable[P, R],
) -> Callable[P, R]:
    """Render the unlock page for unauthenticated users."""

    @wraps(view_func)
    def decorated_view(*args: P.args, **kwargs: P.kwargs) -> R:
        if not current_identity_is_tugraz_authenticated():
            url = current_user_resources.users_service.links_item_tpl.expand(
                identity=g.identity,
                obj=current_user,
            )["avatar"]
            return render_template(
                "invenio_config_tugraz/not_authenticated.html",
                user_avatar=url,
            )
        return view_func(*args, **kwargs)

    return decorated_view


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
