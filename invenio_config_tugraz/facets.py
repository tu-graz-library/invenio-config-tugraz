# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
