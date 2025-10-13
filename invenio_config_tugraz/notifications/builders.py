# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
