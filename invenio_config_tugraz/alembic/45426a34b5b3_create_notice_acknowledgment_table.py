# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Create notice_acknowledgment table."""

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "45426a34b5b3"
down_revision = "e3148da63f06"
branch_labels = ()
depends_on = "9848d0149abd"


def upgrade() -> None:
    """Upgrade database."""
    op.create_table(
        "notice_acknowledgment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("notice_key", sa.String(length=128), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["accounts_user.id"],
            name=op.f("fk_notice_acknowledgment_user_id_accounts_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notice_acknowledgment")),
        sa.UniqueConstraint(
            "user_id",
            "notice_key",
            name=op.f("uq_notice_acknowledgment_user_id"),
        ),
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("notice_acknowledgment")
