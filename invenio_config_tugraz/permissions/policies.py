# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2025 Graz University of Technology.
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

from invenio_administration.generators import Administration
from invenio_communities.generators import (
    AllowedMemberTypes,
    CommunityCurators,
    CommunityManagers,
    CommunityManagersForRole,
    CommunityMembers,
    CommunityOwners,
    CommunitySelfMember,
    IfCommunityDeleted,
    IfMemberPolicyClosed,
    IfRecordSubmissionPolicyClosed,
    ReviewPolicy,
)
from invenio_communities.generators import IfRestricted as IfRestrictedCommunity
from invenio_communities.permissions import (
    # at time of writing, BasePermissionPolicy is originally from `invenio_records_permissions`
    # however, this import should trace the base class of `CommunityPermissionPolicy`
    # importing it from invenio-communities better guarantees that
    BasePermissionPolicy,
)
from invenio_rdm_records.services.generators import (
    AccessGrant,
    CommunityInclusionReviewers,
    IfAtLeastOneCommunity,
    IfDeleted,
    IfExternalDOIRecord,
    IfNewRecord,
    IfOneCommunity,
    IfRecordDeleted,
    IfRestricted,
    RecordCommunitiesAction,
    RecordOwners,
    ResourceAccessToken,
    SecretLinks,
    SubmissionReviewer,
)
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    IfConfig,
    SystemProcess,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy
from invenio_records_resources.services.files.generators import IfTransferType
from invenio_records_resources.services.files.transfer import (
    LOCAL_TRANSFER_TYPE,
    MULTIPART_TRANSFER_TYPE,
)
from invenio_users_resources.services.generators import GroupsEnabled
from invenio_users_resources.services.permissions import UserManager

from .generators import (
    AllowedFromIPNetwork,
    RecordSingleIP,
    TUGrazAuthenticatedButNotCommunityMembers,
    TUGrazAuthenticatedUser,
)


class TUGrazRDMRecordPermissionPolicy(RecordPermissionPolicy):
    """Overwrite authenticatedness to mean `tugraz_authenticated` rather than *signed up*."""

    NEED_LABEL_TO_ACTION = {
        "bucket-update": "update_files",
        "bucket-read": "read_files",
        "object-read": "read_files",
    }

    # permission meant for global curators of the instance
    # (for now applies to internal notes field only
    # to be replaced with an adequate permission when it is defined)
    can_manage_internal = [SystemProcess()]

    #
    # General permission-groups, to be used below
    #
    can_manage = [
        RecordOwners(),
        RecordCommunitiesAction("curate"),
        AccessGrant("manage"),
        SystemProcess(),
    ]
    can_curate = can_manage + [AccessGrant("edit"), SecretLinks("edit")]
    can_review = can_curate + [SubmissionReviewer()]
    can_preview = can_curate + [
        AccessGrant("preview"),
        SecretLinks("preview"),
        SubmissionReviewer(),
        UserManager,
    ]
    can_view = can_preview + [
        AccessGrant("view"),
        SecretLinks("view"),
        SubmissionReviewer(),
        CommunityInclusionReviewers(),
        RecordCommunitiesAction("view"),
        AllowedFromIPNetwork(),
        RecordSingleIP(),
    ]

    can_tugraz_authenticated = [TUGrazAuthenticatedUser(), SystemProcess()]
    can_authenticated = can_tugraz_authenticated
    can_all = [
        AnyUser(),
        SystemProcess(),
        AllowedFromIPNetwork(),
        RecordSingleIP(),
    ]

    #
    # Miscellaneous
    #
    # Allow for querying of statistics
    # - This is currently disabled because it's not needed and could potentially
    #   open up surface for denial of service attacks
    can_query_stats = [Disable()]

    #
    # Records - reading and creating
    #
    can_search = can_all
    can_read = [IfRestricted("record", then_=can_view, else_=can_all)]

    can_read_deleted = [
        IfRecordDeleted(then_=[UserManager, SystemProcess()], else_=can_read),
    ]
    can_read_deleted_files = can_read_deleted
    can_media_read_deleted_files = can_read_deleted_files
    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
        ResourceAccessToken("read"),
    ]
    can_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_read_files),
        SystemProcess(),
    ]
    can_create = can_tugraz_authenticated

    can_search_revisions = [Administration()]

    #
    # Drafts
    #
    can_search_drafts = can_tugraz_authenticated
    can_read_draft = can_preview
    can_draft_read_files = can_preview + [ResourceAccessToken("read")]
    can_update_draft = can_review
    can_draft_create_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_review),
        IfTransferType(MULTIPART_TRANSFER_TYPE, can_review),
        SystemProcess(),
    ]
    can_draft_set_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_review),
        IfTransferType(MULTIPART_TRANSFER_TYPE, can_review),
        SystemProcess(),
    ]
    can_draft_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_draft_read_files),
        SystemProcess(),
    ]
    can_draft_commit_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_review),
        IfTransferType(MULTIPART_TRANSFER_TYPE, can_review),
        SystemProcess(),
    ]
    can_draft_update_files = can_review
    can_draft_delete_files = can_review

    can_draft_get_file_transfer_metadata = [SystemProcess()]
    can_draft_update_file_transfer_metadata = [SystemProcess()]

    can_manage_files = [
        IfConfig(
            "RDM_ALLOW_METADATA_ONLY_RECORDS",
            then_=[IfNewRecord(then_=can_tugraz_authenticated, else_=can_review)],
            else_=[],
        ),
    ]
    can_manage_record_access = [
        IfConfig(
            "RDM_ALLOW_RESTRICTED_RECORDS",
            then_=[IfNewRecord(then_=can_tugraz_authenticated, else_=can_review)],
            else_=[],
        ),
    ]

    #
    # PIDs
    #
    can_pid_create = can_review
    can_pid_register = can_review
    can_pid_update = can_review
    can_pid_discard = can_review
    can_pid_delete = can_review
    can_pid_manage = [SystemProcess()]

    #
    # Actions
    #
    can_edit = [IfDeleted(then_=[Disable()], else_=can_curate)]
    can_delete_draft = can_curate
    can_new_version = [
        IfConfig(
            "RDM_ALLOW_EXTERNAL_DOI_VERSIONING",
            then_=can_curate,
            else_=[IfExternalDOIRecord(then_=[Disable()], else_=can_curate)],
        ),
    ]
    can_publish = [
        IfConfig(
            "RDM_COMMUNITY_REQUIRED_TO_PUBLISH",
            then_=[
                IfAtLeastOneCommunity(
                    then_=can_review,
                    else_=[Administration(), SystemProcess()],
                ),
            ],
            else_=can_review,
        ),
    ]
    can_lift_embargo = can_manage

    #
    # Record communities
    #
    can_add_community = can_manage
    can_remove_community_ = [
        RecordOwners(),
        CommunityCurators(),
        SystemProcess(),
    ]
    can_remove_community = [
        IfConfig(
            "RDM_COMMUNITY_REQUIRED_TO_PUBLISH",
            then_=[
                IfOneCommunity(
                    then_=[Administration(), SystemProcess()],
                    else_=can_remove_community_,
                ),
            ],
            else_=can_remove_community_,
        ),
    ]
    can_remove_record = [CommunityCurators(), Administration(), SystemProcess()]
    can_bulk_add = [SystemProcess()]

    #
    # Media files - draft
    #
    can_draft_media_create_files = can_review
    can_draft_media_read_files = can_review
    can_draft_media_set_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_review),
        SystemProcess(),
    ]
    can_draft_media_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_preview),
        SystemProcess(),
    ]
    can_draft_media_commit_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_review),
        SystemProcess(),
    ]
    can_draft_media_delete_files = can_review
    can_draft_media_update_files = can_review

    #
    # Media files - record
    #
    can_media_read_files = [
        IfRestricted("record", then_=can_view, else_=can_all),
        ResourceAccessToken("read"),
    ]
    can_media_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_read),
        SystemProcess(),
    ]
    can_media_create_files = [Disable()]
    can_media_set_content_files = [Disable()]
    can_media_commit_files = [Disable()]
    can_media_update_files = [Disable()]
    can_media_delete_files = [Disable()]

    #
    # Record deletetion
    #
    can_delete = [Administration(), SystemProcess()]
    can_delete_files = [SystemProcess()]
    can_purge = [SystemProcess()]

    #
    # Quotas for records/users
    #
    can_manage_quota = [UserManager, SystemProcess()]

    #
    # Disabled
    #
    # - Records/files are updated/deleted via drafts so we don't support
    #   using below actions.
    can_update = [Disable()]
    can_create_files = [Disable()]
    can_set_content_files = [Disable()]
    can_commit_files = [Disable()]
    can_update_files = [Disable()]

    can_get_file_transfer_metadata = [Disable()]
    can_update_file_transfer_metadata = [Disable()]

    # Used to hide the `parent.is_verified` field. It should be set to
    # correct permissions based on which the field will be exposed only to moderators
    can_moderate = [SystemProcess()]


class TUGrazCommunityPermissionPolicy(BasePermissionPolicy):
    """Have communities respect `tugraz_authenticated` rather than *signed up*."""

    # NOTE: this class's body was copied from invenio_communities.permissions:CommunityPermissionPolicy

    # Community
    can_create = [TUGrazAuthenticatedUser(), SystemProcess()]

    can_read = [
        IfRestrictedCommunity(
            "visibility",
            then_=[CommunityMembers()],
            else_=[AnyUser()],
        ),
        SystemProcess(),
    ]

    # Used for search filtering of deleted records
    # cannot be implemented inside can_read - otherwise permission will
    # kick in before tombstone renders
    can_read_deleted = [
        IfCommunityDeleted(then_=[UserManager, SystemProcess()], else_=can_read),
    ]

    can_update = [CommunityOwners(), SystemProcess()]

    can_delete = [CommunityOwners(), SystemProcess()]

    can_purge = [CommunityOwners(), SystemProcess()]

    can_manage_access = [
        IfConfig("COMMUNITIES_ALLOW_RESTRICTED", then_=can_update, else_=[]),
    ]

    can_create_restricted = [
        IfConfig("COMMUNITIES_ALLOW_RESTRICTED", then_=can_create, else_=[]),
    ]

    can_search = [AnyUser(), SystemProcess()]

    # NOTE: this is deliberately left at `AuthenticatedUser` rather than `TUGrazAuthenticatedUser`
    # requiring `TUGrazAuthenticatedUser` would break *My Communities* part of communites page for
    # users that are authenticated but not tugraz_authenticated
    can_search_user_communities = [AuthenticatedUser(), SystemProcess()]

    can_search_invites = [CommunityManagers(), SystemProcess()]

    can_search_requests = [CommunityManagers(), CommunityCurators(), SystemProcess()]

    can_rename = [CommunityOwners(), SystemProcess()]

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

    # who can include a record directly, without a review
    can_include_directly = [
        ReviewPolicy(
            closed_=[Disable()],
            open_=[CommunityCurators()],
            members_=[CommunityMembers()],
        ),
        SystemProcess(),
    ]

    can_members_add = [
        CommunityManagersForRole(),
        AllowedMemberTypes("group"),
        GroupsEnabled("group"),
        SystemProcess(),
    ]

    can_members_invite = [
        CommunityManagersForRole(),
        AllowedMemberTypes("user", "email"),
        SystemProcess(),
    ]

    can_members_manage = [
        CommunityManagers(),
        SystemProcess(),
    ]

    can_members_search = [
        CommunityMembers(),
        SystemProcess(),
    ]

    can_members_search_public = [
        IfRestrictedCommunity(
            "visibility",
            then_=[CommunityMembers()],
            else_=[
                IfRestrictedCommunity(
                    "members_visibility",
                    then_=[CommunityMembers()],
                    else_=[AnyUser()],
                ),
            ],
        ),
        SystemProcess(),
    ]

    # Ability to use membership update api
    can_members_bulk_update = [
        CommunityMembers(),
        SystemProcess(),
    ]

    can_members_bulk_delete = can_members_bulk_update

    # Ability to update a single membership
    can_members_update = [
        CommunityManagersForRole(),
        CommunitySelfMember(),
        SystemProcess(),
    ]

    # Ability to delete a single membership
    can_members_delete = can_members_update

    can_invite_owners = [CommunityOwners(), SystemProcess()]

    # Abilities for featured communities
    can_featured_search = [AnyUser(), SystemProcess()]
    can_featured_list = [Administration(), SystemProcess()]
    can_featured_create = [Administration(), SystemProcess()]
    can_featured_update = [Administration(), SystemProcess()]
    can_featured_delete = [Administration(), SystemProcess()]

    # Used to hide at the moment the `is_verified` field. It should be set to
    # correct permissions based on which the field will be exposed only to moderators
    can_moderate = [SystemProcess()]

    # Permissions to crud community theming
    can_set_theme = [SystemProcess()]
    can_delete_theme = can_set_theme

    # Permissions to set if communities can have children
    can_manage_children = [SystemProcess()]

    # Permission for assigning a parent community
    can_manage_parent = [Administration(), SystemProcess()]

    # request_membership permission is based on configuration, community settings and
    # identity. Other factors (e.g., previous membership requests) are not under
    # its purview and are dealt with elsewhere.
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
