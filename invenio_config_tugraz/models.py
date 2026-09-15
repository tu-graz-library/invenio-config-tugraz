# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Database models for invenio-config-tugraz."""

from invenio_accounts.models import User
from invenio_db import db


class NoticeAcknowledgment(db.Model, db.Timestamp):
    """Records that a user acknowledged a notice."""

    __tablename__ = "tugraz_notice_acknowledgment"
    __table_args__ = (db.UniqueConstraint("user_id", "notice_key"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    notice_key = db.Column(db.String(128), nullable=False)
