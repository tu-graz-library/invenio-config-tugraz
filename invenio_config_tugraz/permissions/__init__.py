# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
