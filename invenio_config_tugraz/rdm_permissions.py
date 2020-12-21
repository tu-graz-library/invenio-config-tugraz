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
    AnyUserIfPublic,
    RecordOwners,
    SuperUser,
)

from .generators import RecordIp


class TUGRAZPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for records.

    This overrides the /api/records endpoint.

    """

    # Create action given to no one (Not even superusers) bc Deposits should
    # be used.
    can_create = [SuperUser()]


class TUGRAZBibliographicRecordServiceConfig(BibliographicRecordServiceConfig):
    """Overriding BibliographicRecordServiceConfig."""

    permission_policy_cls = TUGRAZPermissionPolicy
