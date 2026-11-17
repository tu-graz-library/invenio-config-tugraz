# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""TU Graz permission-policy for invenio services.

To use, set these config-variables:
  `RDM_PERMISSION_POLICY` to `TUGrazRDMRecordPermissionPolicy`
  `COMMUNITIES_PERMISSION_POLICY` to `TUGrazCommunityPermissionPolicy`

Policies list **what actions** can be done **by whom**
over an implied category of objects (typically records). A Policy is
instantiated on a per action basis and is a descendant of `Permission
<https://invenio-access.readthedocs.io/en/latest/api.html
#invenio_access.permissions.Permission>`_ in
`invenio-access <https://invenio-access.readthedocs.io>`_ .
Generators are used to provide the "by whom" part and the implied category of
object.

Actions are class variables of the form: ``can_<action>`` and the
corresponding (dis-)allowed identities are a list of Generator instances.
One can define any action as long as it follows that pattern and
is verified at the moment it is undertaken.
"""

from invenio_communities.generators import (
    CommunityMembers,
    IfRecordSubmissionPolicyClosed,
)
from invenio_communities.generators import IfRestricted as IfRestrictedCommunity
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_curations.services.generators import (
    CurationModerators,
    IfCurationRecordBasedExists,
)
from invenio_rdm_records.services.permissions import (
    RDMRecordPermissionPolicy,
)
from invenio_records_permissions.generators import (
    IfConfig,
    SameAs,
    SystemProcess,
)

from .generators import (
    AllowedFromIPNetwork,
    IfMemberPolicyClosed,
    RecordSingleIP,
    TUGrazAuthenticatedButNotCommunityMembers,
    TUGrazAuthenticatedUser,
)


class TUGrazRDMRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Overwrite authenticatedness to mean `tugraz_authenticated` rather than *signed up*."""

    can_preview = RDMRecordPermissionPolicy.can_preview + [
        IfCurationRecordBasedExists(then_=[CurationModerators()], else_=[]),
    ]
    can_view = RDMRecordPermissionPolicy.can_view + [
        AllowedFromIPNetwork(),
        RecordSingleIP(),
    ]

    can_tugraz_authenticated = [TUGrazAuthenticatedUser(), SystemProcess()]
    can_authenticated = SameAs("can_tugraz_authenticated")
    can_all = RDMRecordPermissionPolicy.can_all + [
        AllowedFromIPNetwork(),
        RecordSingleIP(),
    ]


class TUGrazCommunityPermissionPolicy(CommunityPermissionPolicy):
    """Have communities respect `tugraz_authenticated` rather than *signed up*."""

    can_create = [TUGrazAuthenticatedUser(), SystemProcess()]

    can_request_membership = [
        IfConfig(
            "COMMUNITIES_ALLOW_MEMBERSHIP_REQUESTS",
            then_=[
                IfMemberPolicyClosed(
                    then_=[SystemProcess()],
                    else_=[TUGrazAuthenticatedButNotCommunityMembers()],
                ),
            ],
            else_=[SystemProcess()],
        ),
    ]

    can_submit_record = [
        IfRecordSubmissionPolicyClosed(
            then_=[CommunityMembers()],
            else_=[
                IfRestrictedCommunity(
                    "visibility",
                    then_=[CommunityMembers()],
                    else_=[TUGrazAuthenticatedUser()],
                ),
            ],
        ),
        SystemProcess(),
    ]
