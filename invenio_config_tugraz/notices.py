# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""User notices, filtered by who they are shown to, role and per item."""

from flask import Blueprint, Flask, current_app, g, jsonify
from flask_login import current_user, login_required
from invenio_db import db
from werkzeug.wrappers import Response as BaseResponse

from .models import NoticeAcknowledgment


def current_roles() -> set[str]:
    """Role names held by the current identity."""
    return {need.value for need in g.identity.provides if need.method == "role"}


def is_shown_to(notice: dict, *, authenticated: bool) -> bool:
    """Check whether the notice should be shown to this visitor."""
    show_to = notice.get("show_to", "users")
    if show_to == "guests":
        return not authenticated
    if show_to == "users":
        return authenticated
    return True


def roles_match(roles: list | None, held: set[str]) -> bool:
    """Check whether the visitor holds one of the required roles."""
    return not roles or any(role in held for role in roles)


def visible_items(notice: dict, roles: set[str]) -> list[str]:
    """Return the item texts the visitor is allowed to see."""
    result = []
    for item in notice["items"]:
        if not isinstance(item, dict):
            result.append(str(item))
            continue
        if not roles_match(item.get("roles"), roles):
            continue
        check = item.get("visible")
        if check and not check():
            continue
        result.append(str(item["text"]))
    return result


def pending_notices() -> list[dict]:
    """Return the notices to show the current visitor."""
    authenticated = current_user.is_authenticated
    roles = current_roles() if authenticated else set()
    seen = set()
    if authenticated:
        seen = {
            ack.notice_key
            for ack in NoticeAcknowledgment.query.filter_by(user_id=current_user.id)
        }
    notices = []
    for notice in current_app.config.get("CONFIG_TUGRAZ_NOTICES", []):
        if not is_shown_to(notice, authenticated=authenticated):
            continue
        if authenticated and not roles_match(notice.get("roles"), roles):
            continue
        if notice["key"] in seen:
            continue
        notices.append(
            {
                "key": notice["key"],
                "title": str(notice["title"]),
                "intro": str(notice["intro"]),
                "items": visible_items(notice, roles),
                "outro": str(notice["outro"]) if notice.get("outro") else "",
                "accent": bool(notice.get("accent")),
            },
        )
    return notices


def api_blueprint(_app: Flask) -> Blueprint:
    """Blueprint for the notices API."""
    blueprint = Blueprint("tugraz_notices", __name__, url_prefix="/notices")

    @blueprint.route("/<key>/acknowledge", methods=["POST"])
    @login_required
    def acknowledge(key: str) -> BaseResponse:
        """Record that the current user acknowledged a notice."""
        already = NoticeAcknowledgment.query.filter_by(
            user_id=current_user.id,
            notice_key=key,
        ).count()
        if not already:
            db.session.add(
                NoticeAcknowledgment(user_id=current_user.id, notice_key=key),
            )
            db.session.commit()
        return jsonify({"acknowledged": key})

    return blueprint
