# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Database models for invenio-config-tugraz."""

from invenio_accounts.models import User
from invenio_db import db


class NoticeAcknowledgment(db.Model, db.Timestamp):
    """Records that a user acknowledged a notice."""

    __tablename__ = "notice_acknowledgment"
    __table_args__ = (db.UniqueConstraint("user_id", "notice_key"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
    )
    notice_key = db.Column(db.String(128), nullable=False)
