# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

r"""Permission generators for permission policies.

invenio's permissions build on
`flask-principal <https://pythonhosted.org/Flask-Principal>`_ .

In `flask-principal`, an action's `Need`s are checked
against current user's `Need`s to determine permissions.

For example, the action of deleting a record is only
permitted to users with `Need(method='role', value='admin')`.

Not all `Need`s can be known before the app is running.
For example, permissions for reading a record depend on whether
the record is public/private, so the set of `Need`s necessary
for reading a record must be computed dynamically at runtime.
This is the use case for
invenio's :py:class:`~invenio_records_permissions.generators.Generator`:
it generates `Need`s necessary for an action at runtime.

A `Generator` object defines 3 methods in addition to its constructor:

- ``needs(self, **kwargs)``: returns `Need`s, one of which a provider is
                             required to have to be allowed
- ``excludes(self, **kwargs)``: returns a list of `Need`s disallowing any
                                provider of a single one
- ``query_filter(self, **kwargs)``: returns a query filter to enable retrieval
                                    of records

The ``needs`` and ``excludes`` methods specify access conditions from
the point-of-view of the object-of-concern; whereas, the ``query_filter``
method specifies those from the actor's point-of-view in search scenarios.

.. Note::

    Exclusion has priority over inclusion. If a `Need` is returned by both
    ``needs`` and ``excludes``, providers of that `Need` will be **excluded**.

"""

from flask import current_app, request
from invenio_access.permissions import any_user
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl

from .roles import tugraz_authenticated_user


class RecordIp(Generator):
    """Allowed any user with accessing with the IP."""

    def needs(self, record=None, **kwargs):
        """Enabling Needs, Set of Needs granting permission."""
        if record is None:
            return []

        # check if singleip is in the records restriction
        is_single_ip = record.get("access", {}).get("access_right") == "singleip"

        # check if the user ip is on list
        visible = self.check_permission()

        if not is_single_ip:
            # if record does not have singleip - return any_user
            return [any_user]
            # if record has singleip, then check the ip of user - if ip user is on list - return any_user
        elif visible:
            return [any_user]
        else:
            # non of the above - return empty
            return []

    def excludes(self, **kwargs):
        """Preventing Needs, Set of Needs denying permission.

        If ANY of the Needs are matched, permission is revoked.

        .. note::

            ``_load_permissions()`` method from `Permission
            <https://invenio-access.readthedocs.io/en/latest/api.html
            #invenio_access.permissions.Permission>`_ adds by default the
            ``superuser_access`` Need (if tied to a User or Role) for us.

            It also expands ActionNeeds into the Users/Roles that
            provide them.

        If the same Need is returned by `needs` and `excludes`, then that
        Need provider is disallowed.
        """
        return []

    def query_filter(self, *args, **kwargs):
        """Filters for singleip records."""
        # check if the user ip is on list
        visible = self.check_permission()

        if not visible:
            # If user ip is not on the list, and If the record contains 'singleip' will not be seen
            return ~dsl.Q("match", **{"access.access_right": "singleip"})

        # Lists all records
        return dsl.Q("match_all")

    def check_permission(self):
        """Check for User IP address in config variable."""
        # Get user IP
        user_ip = request.remote_addr
        # Checks if the user IP is among single IPs
        if user_ip in current_app.config["INVENIO_CONFIG_TUGRAZ_SINGLE_IP"]:
            return True
        return False


class TUGrazAuthenticatedUser(Generator):
    """Generates the `tugraz_authenticated_user` role-need."""

    def needs(self, **__):
        """Generate needs to be checked against current user identity."""
        return [tugraz_authenticated_user]
