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

from typing import Final

from invenio_communities.generators import (
    CommunityMembers,
    IfRecordSubmissionPolicyClosed,
)
from invenio_communities.generators import IfRestricted as IfRestrictedCommunity
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_curations.requests.curation import CurationRequest
from invenio_curations.services.generators import (
    CurationModerators,
    IfCurationRecordBasedExists,
    IfCurationRequestAccepted,
    IfCurationRequestBasedExists,
    IfRequestTypes,
    TopicPermission,
)
from invenio_rdm_records.requests import CommunitySubmission
from invenio_rdm_records.services.permissions import (
    RDMRecordPermissionPolicy,
    RDMRequestsPermissionPolicy,
)
from invenio_records_permissions.generators import (
    IfConfig,
    SameAs,
    SystemProcess,
)
from invenio_requests.services.generators import Creator, Receiver

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


class TUGrazRDMRequestsPermissionPolicy(RDMRequestsPermissionPolicy):
    """Customized requests permission policy for TU Graz repository's needs.

    Note: For now it is 100% percent copied from invenio-curations.
    """

    curation_request_record_review = IfRequestTypes(
        [CurationRequest],
        then_=[TopicPermission(permission_name="can_review")],
        else_=[],
    )

    # Only allow community-submission requests to be accepted after the rdm-curation request has been accepted
    # (if curation request exists).
    _can_communities_curation_accept: Final = [
        IfCurationRequestBasedExists(
            then_=[
                IfCurationRequestAccepted(
                    then_=RDMRequestsPermissionPolicy.can_action_accept,
                    else_=[],
                ),
            ],
            else_=RDMRequestsPermissionPolicy.can_action_accept,
        ),
    ]

    can_action_accept: Final = [
        IfRequestTypes(
            request_types=[CommunitySubmission],
            then_=_can_communities_curation_accept,
            else_=RDMRequestsPermissionPolicy.can_action_accept,
        ),
    ]

    # Update can read and can comment with new states
    can_read: Final = [
        # Have to explicitly check the request type and circumvent using status, as creator/receiver will add a query filter where one entity must be the user.
        IfRequestTypes(
            [CurationRequest],
            then_=[
                Creator(),
                Receiver(),
                TopicPermission(permission_name="can_review"),
                SystemProcess(),
            ],
            else_=RDMRequestsPermissionPolicy.can_read,
        ),
    ]
    can_create_comment = SameAs("can_read")
    can_reply_comment = SameAs("can_create_comment")

    # Update submit to also allow record reviewers/managers for curation requests
    can_action_submit = RDMRequestsPermissionPolicy.can_action_submit + [
        curation_request_record_review,
    ]

    # Add new actions
    can_action_review = RDMRequestsPermissionPolicy.can_action_accept
    can_action_critique = RDMRequestsPermissionPolicy.can_action_accept
    can_action_resubmit = SameAs("can_action_submit")
    can_action_pending_resubmission = SameAs("can_action_resubmit")
