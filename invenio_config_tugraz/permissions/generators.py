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

from ipaddress import ip_address, ip_network
from typing import Any

from flask import current_app, request
from flask_principal import Need
from invenio_access.permissions import any_user
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl

from .roles import tugraz_authenticated_user


class RecordSingleIP(Generator):
    """Allowed any user with accessing with the IP."""

    def needs(self, record: dict | None = None, **__: dict) -> list[Need]:
        """Set of Needs granting permission. Enabling Needs."""
        if record is None:
            return []

        # if record has singleip, and the ip of the user matches the allowed ip
        if (
            record.get("custom_fields", {}).get("single_ip", False)
            and self.check_permission()
        ):
            return [any_user]

        # non of the above - return empty
        return []

    def excludes(self, **kwargs: dict) -> list[Need]:
        """Set of Needs denying permission. Preventing Needs.

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
        try:
            if (
                kwargs["record"]["custom_fields"]["single_ip"]
                and not self.check_permission()
            ):
                return [any_user]

        except KeyError:
            return []
        else:
            return []

    def query_filter(self, *_: dict, **__: dict) -> Any:  # noqa: ANN401
        """Filter for singleip records."""
        if not self.check_permission():
            # If user ip is not on the list, and If the record contains 'singleip' will not be seen
            return ~dsl.Q("match", **{"custom_fields.single_ip": True})

        # Lists all records
        return dsl.Q("match_all")

    def check_permission(self) -> bool:
        """Check for User IP address in config variable.

        If the user ip is in the configured list return True.
        """
        try:
            user_ip = request.remote_addr
        except RuntimeError:
            return False

        single_ips = current_app.config["CONFIG_TUGRAZ_SINGLE_IPS"]

        return user_ip in single_ips


class AllowedFromIPNetwork(Generator):
    """Allowed from ip range."""

    def needs(self, record: dict | None = None, **__: dict) -> list[Need]:
        """Set of Needs granting permission. Enabling Needs."""
        if record is None:
            return []

        # if the record has set the ip_range allowance and is in the range
        if (
            record.get("custom_fields", {}).get("ip_network", False)
            and self.check_permission()
        ):
            return [any_user]

        # non of the above - return empty
        return []

    def excludes(self, **kwargs: dict) -> Need:
        """Set of Needs denying permission. Preventing Needs.

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
        try:
            if (
                kwargs["record"]["custom_fields"]["ip_network"]
                and not self.check_permission()
            ):
                return [any_user]

        except KeyError:
            return []
        else:
            return []

    def query_filter(self, *_: dict, **__: dict) -> Any:  # noqa: ANN401
        """Filter for ip range records."""
        if not self.check_permission():
            return ~dsl.Q("match", **{"custom_fields.ip_network": True})

        return dsl.Q("match_all")

    def check_permission(self) -> bool:
        """Check for User IP address in the configured network."""
        try:
            user_ip = request.remote_addr
        except RuntimeError:
            return False

        network = current_app.config["CONFIG_TUGRAZ_IP_NETWORK"]

        try:
            return ip_address(user_ip) in ip_network(network)
        except ValueError:
            return False


class TUGrazAuthenticatedUser(Generator):
    """Generates the `tugraz_authenticated_user` role-need."""

    def needs(self, **__: dict) -> list[Need]:
        """Generate needs to be checked against current user identity."""
        return [tugraz_authenticated_user]
