# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Override notifications builders based on TU Graz Repo requirements."""

from invenio_app_rdm.config import NOTIFICATIONS_BUILDERS
from invenio_curations.config import CURATIONS_NOTIFICATIONS_BUILDERS

TUGRAZ_NOTIFICATIONS_BUILDERS = {
    **NOTIFICATIONS_BUILDERS,
    **CURATIONS_NOTIFICATIONS_BUILDERS,
}
"""TU Graz notification builders.

Extended the default invenio-app-rdm with curations specific notifications.
"""
