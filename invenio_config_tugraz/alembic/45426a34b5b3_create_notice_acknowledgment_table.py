# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Create notice_acknowledgment table."""

import sqlalchemy as sa
from invenio_db import db

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
        sa.Column("created", db.UTCDateTime(), nullable=False),
        sa.Column("updated", db.UTCDateTime(), nullable=False),
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
