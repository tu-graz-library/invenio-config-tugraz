# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
