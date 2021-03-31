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

from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.config import RDMRecordServiceConfig
from invenio_rdm_records.services.generators import IfDraft, IfRestricted, RecordOwners
from invenio_records_permissions.generators import (
    Admin,
    AnyUser,
    AuthenticatedUser,
    Disable,
    SuperUser,
    SystemProcess,
)


class TUGRAZPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for rdm records.

    This overrides the origin:
    https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/permissions.py.
    Access control configuration for records.
    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.
    - Create action given to everyone for now.
    - Read access given to everyone if public record and given to owners
      always. (inherited)
    - Update access given to record owners. (inherited)
    - Delete access given to admins only. (inherited)
    """


class TUGRAZRDMRecordServiceConfig(RDMRecordServiceConfig):
    """Overriding BibliographicRecordServiceConfig."""
