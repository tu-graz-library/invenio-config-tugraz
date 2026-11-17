# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Override specific facets for TU Graz Repo."""

from invenio_curations.services import facets

TUGRAZ_REQUESTS_FACETS = {
    "type": {
        "facet": facets.type,
        "ui": {
            "field": "type",
        },
    },
    "status": {
        "facet": facets.status,
        "ui": {
            "field": "status",
        },
    },
}
"""TU Graz requests facets.

To use: override in invenio.cfg. REQUESTS_FACETS = TUGRAZ_REQUESTS_FACETS.
"""
