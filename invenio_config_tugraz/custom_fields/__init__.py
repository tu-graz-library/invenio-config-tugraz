# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Custom fields."""

from invenio_records_resources.services.custom_fields import BooleanCF

ip_network = BooleanCF(name="ip_network")
single_ip = BooleanCF(name="single_ip")
