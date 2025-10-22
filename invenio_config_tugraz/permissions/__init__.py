# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permission-policies and roles, based on `flask-principal`."""

from .policies import (
    TUGrazCommunityPermissionPolicy,
    TUGrazRDMRecordPermissionPolicy,
    TUGrazRDMRequestsPermissionPolicy,
)

__all__ = (
    "TUGrazCommunityPermissionPolicy",
    "TUGrazRDMRecordPermissionPolicy",
    "TUGrazRDMRequestsPermissionPolicy",
)
