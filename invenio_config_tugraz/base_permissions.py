# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""
Records permission policies.

Default policies for records:

.. code-block:: python

    # Read access given to everyone.
    can_search = [AnyUser()]
    # Create action given to no one (Not even superusers) bc Deposits should
    # be used.
    can_create = [Disable()]
    # Read access given to everyone if public record/files and owners always.
    can_read = [AnyUserIfPublic(), RecordOwners()]
    # Update access given to record owners.
    can_update = [RecordOwners()]
    # Delete access given to admins only.
    can_delete = [Admin()]
    # Associated files permissions (which are really bucket permissions)
    can_read_files = [AnyUserIfPublic(), RecordOwners()]
    can_update_files = [RecordOwners()]

How to override default policies for records.

Using Custom Generator for a policy:

.. code-block:: python

    from invenio_rdm_records.permissions import RDMRecordPermissionPolicy
    from invenio_config_tugraz.generators import RecordIp

    class TUGRAZPermissionPolicy(RDMRecordPermissionPolicy):

    # Delete access given to RecordIp only.

    can_delete = [RecordIp()]

    RECORDS_PERMISSIONS_RECORD_POLICY = TUGRAZPermissionPolicy


Permissions for Invenio records.
"""


from invenio_rdm_records.services.generators import (
    IfRestricted,
    RecordOwners,
    SecretLinks,
)
from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    SystemProcess,
)

from .generators import TUGrazCurators


class TUGrazPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for records.

    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.
    """

    NEED_LABEL_TO_ACTION = {
        'bucket-update': 'update_files',
        'bucket-read': 'read_files',
        'object-read': 'read_files',
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [RecordOwners(), TUGrazCurators(), SystemProcess()]
    can_curate = can_manage + [SecretLinks("edit")]
    can_preview = can_manage + [SecretLinks("preview")]
    can_view = can_manage + [SecretLinks("view")]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess()]

    #
    #  Records
    #
    # Allow searching of records
    can_search = can_all
    # Allow reading metadata of a record
    can_read = [IfRestricted('record', then_=can_view, else_=can_all)]
    # Allow reading the files of a record
    can_read_files = [IfRestricted('files', then_=can_view, else_=can_all)]
    # Allow submitting new record
    can_create = can_authenticated

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate

    #
    # PIDs
    #
    can_pid_reserve = can_curate
    can_pid_delete = can_curate

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_curate
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage

    #
    # Disabled actions (these should not be used or changed)
    #
    # - Records/files are updated/deleted via drafts so we don't support
    #   using below actions.
    can_update = [Disable()]
    can_delete = [Disable()]
    can_create_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]
