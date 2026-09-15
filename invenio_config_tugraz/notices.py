# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Notices shown once to logged-in users and acknowledged per user."""

from flask import Blueprint, Flask, current_app, jsonify
from flask_login import current_user, login_required
from invenio_db import db

from .models import NoticeAcknowledgment


def pending_notices():
    """Return the notices the current user has not acknowledged yet."""
    if not current_user.is_authenticated:
        return []
    seen = {
        ack.notice_key
        for ack in NoticeAcknowledgment.query.filter_by(user_id=current_user.id)
    }
    return [
        {
            "key": notice["key"],
            "title": str(notice["title"]),
            "intro": str(notice["intro"]),
            "items": [str(item) for item in notice["items"]],
        }
        for notice in current_app.config.get("CONFIG_TUGRAZ_NOTICES", [])
        if notice["key"] not in seen
    ]


def api_blueprint(app: Flask) -> Blueprint:
    """Blueprint for the notices REST API."""
    blueprint = Blueprint("tugraz_notices", __name__, url_prefix="/notices")

    @blueprint.route("/<key>/acknowledge", methods=["POST"])
    @login_required
    def acknowledge(key: str):
        already = NoticeAcknowledgment.query.filter_by(
            user_id=current_user.id, notice_key=key
        ).count()
        if not already:
            db.session.add(
                NoticeAcknowledgment(user_id=current_user.id, notice_key=key)
            )
            db.session.commit()
        return jsonify({"acknowledged": key})

    return blueprint
