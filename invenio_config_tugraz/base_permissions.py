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

# from invenio_records_permissions.generators import (
#     Admin,
#     AnyUser,
#     AnyUserIfPublic,
#     RecordOwners,
# )
# from invenio_records_permissions.policies.base import BasePermissionPolicy

# from .generators import RecordIp


# class TUGRAZPermissionPolicy(BasePermissionPolicy):
#     """Access control configuration for records.

#     This overrides the /api/records endpoint.

#     """

#     # Read access to API given to everyone.
#     can_search = [AnyUser(), RecordIp()]

#     # Read access given to everyone if public record/files and owners always.
#     can_read = [AnyUserIfPublic(), RecordOwners(), RecordIp()]

#     # Create action given to no one (Not even superusers) bc Deposits should
#     # be used.
#     can_create = [AnyUser()]

#     # Update access given to record owners.
#     can_update = [RecordOwners()]

#     # Delete access given to admins only.
#     can_delete = [Admin()]

#     # Associated files permissions (which are really bucket permissions)
#     can_read_files = [AnyUserIfPublic(), RecordOwners()]
#     can_update_files = [RecordOwners()]
