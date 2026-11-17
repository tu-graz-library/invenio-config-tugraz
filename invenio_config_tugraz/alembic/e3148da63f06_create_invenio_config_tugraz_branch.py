# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Create invenio-config-tugraz branch."""

# revision identifiers
revision = "e3148da63f06"
down_revision = None
branch_labels = ("invenio_config_tugraz",)
depends_on = "dbdbc1b19cf2"


def upgrade() -> None:
    """Upgrade database."""


def downgrade() -> None:
    """Downgrade database."""
