# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Override specific components for TU Graz Repo."""

from invenio_curations.services.components import CurationComponent
from invenio_rdm_records.services.components import (
    DefaultRecordsComponents as RDMDefaultRecordsComponents,
)

TUGRAZ_RDM_RECORDS_SERVICE_COMPONENTS = RDMDefaultRecordsComponents + [
    CurationComponent,
]
"""TU Graz default RDM record components.

To use: append in invenio.cfg TUGRAZ_RDM_RECORDS_SERVICE_COMPONENTS to other needed components.
"""
