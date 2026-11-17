# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Override requests events configurations based on TU Graz Repo requirements."""

from invenio_curations.services.components import CurationEventsComponent
from invenio_curations.services.events import CurationCommentEventType
from invenio_requests.config import REQUESTS_EVENTS_SERVICE_COMPONENTS
from invenio_requests.customizations import LogEventType

TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES = [
    LogEventType(),
    CurationCommentEventType(),
]
"""TU Graz requests event types.

To use: override in invenio.cfg. REQUESTS_REGISTERED_EVENT_TYPES = TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES
"""

TUGRAZ_REQUESTS_EVENTS_SERVICE_COMPONENTS = REQUESTS_EVENTS_SERVICE_COMPONENTS + [
    CurationEventsComponent,
]
"""TU Graz requests events components.

To use: override in invenio.cfg. REQUESTS_EVENTS_SERVICE_COMPONENTS = TUGRAZ_REQUESTS_EVENTS_SERVICE_COMPONENTS
"""
