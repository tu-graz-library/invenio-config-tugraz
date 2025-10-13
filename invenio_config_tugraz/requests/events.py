# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Override requests events configurations based on TU Graz Repo requirements."""

from invenio_curations.services.events import CurationCommentEventType
from invenio_requests.customizations import LogEventType

TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES = [
    LogEventType(),
    CurationCommentEventType(),
]
"""TU Graz requests event types.

To use: override in invenio.cfg. REQUESTS_REGISTERED_EVENT_TYPES = TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES
"""
