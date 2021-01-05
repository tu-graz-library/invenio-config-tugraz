# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology.
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

How to override default policies for rdm-records.

Using Custom Generator for a policy:

.. code-block:: python

    from invenio_rdm_records.services import (
    BibliographicRecordServiceConfig,
    RDMRecordPermissionPolicy,
    )

    from invenio_config_tugraz.generators import RecordIp

    class TUGRAZPermissionPolicy(RDMRecordPermissionPolicy):

    # Create access given to SuperUser only.

    can_create = [SuperUser()]

    RDM_RECORDS_BIBLIOGRAPHIC_SERVICE_CONFIG  = TUGRAZBibliographicRecordServiceConfig


Permissions for Invenio (RDM) Records.
"""

from invenio_rdm_records.services import (
    BibliographicRecordServiceConfig,
    RDMRecordPermissionPolicy,
)
from invenio_records_permissions.generators import (
    Admin,
    AnyUser,
    RecordOwners,
    SuperUser,
)

from .generators import AuthenticatedUser, RecordIp


class TUGRAZPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for rdm records.

    This overrides the origin:
    https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/permissions.py.

    """

    # Read access given to:
    # TODO:
    # AnyUserIfPublic : grant access if record is public
    # RecordIp: grant access for single_ip
    # RecordOwners: owner of records, enable once the deposit is allowed only for loged-in users.
    # CURRENT:
    # RecordIp: grant access for single_ip
    can_read = [RecordIp()]  # RecordOwners()

    # Search access given to:
    # AnyUser : grant access anyUser
    # RecordIp: grant access for single_ip
    can_search = [AnyUser(), RecordIp()]

    # Update access given to record owners.
    can_update = [RecordOwners()]

    # Delete access given to admins only.
    can_delete = [Admin()]

    # Create action given to AuthenticatedUser
    # UI - if user is loged in
    # API - if user has Access token (Bearer API-TOKEN)
    can_create = [AuthenticatedUser()]

    # Associated files permissions (which are really bucket permissions)
    # can_read_files = [AnyUserIfPublic(), RecordOwners()]
    # can_update_files = [RecordOwners()]


class TUGRAZBibliographicRecordServiceConfig(BibliographicRecordServiceConfig):
    """Overriding BibliographicRecordServiceConfig."""

    permission_policy_cls = TUGRAZPermissionPolicy
