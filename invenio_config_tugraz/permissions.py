# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

r"""Permission generators, policies and factories for Invenio records.

Invenio-records-permissions provides a means to fully customize access control
for Invenio records. It does so by defining and providing three layers of
permission constructs that build on each other:
Generators, Policies and Factories. You can extend or override them for maximum
control. Thankfully we provide default ones that cover most cases.

Factories make invenio-records-permissions immediately compatible
with any Invenio module requiring permission factories (e.g.,
`invenio-records-rest <https://invenio-records-rest.readthedocs.io>`_ and
`invenio-files-rest <https://invenio-files-rest.readthedocs.io>`_ ).

Invenio-records-permissions conveniently structures (and relies on)
functionalities from
`invenio-access <https://invenio-access.readthedocs.io>`_ and
`flask-principal <https://pythonhosted.org/Flask-Principal>`_ .


Generators
----------

Generators are the lowest level of abstraction provided by
invenio-records-permissions. A
:py:class:`~invenio_records_permissions.generators.Generator` represents
identities via
`Needs <https://invenio-access.readthedocs.io/en/latest/api.html#needs>`_ that
are allowed or disallowed to act on a kind of object. A Generator does not
specify the action, but it does specify who is allowed and the kind of object
of concern (typically records). Generators *generate* required and forbidden
Needs at the object-of-concern level and *generate* query filters
at the search-for-objects-of-concern level.

A Generator object defines 3 methods in addition to its constructor:

- ``needs(self, **kwargs)``: returns Needs, one of which a provider is
                             required to have to be allowed
- ``excludes(self, **kwargs)``: returns a list of Needs disallowing any
                                provider of a single one
- ``query_filter(self, **kwargs)``: returns a query filter to enable retrieval
                                    of records

The ``needs`` and ``excludes`` methods specify access conditions from
the point-of-view of the object-of-concern; whereas, the ``query_filter``
method specifies those from the actor's point-of-view in search scenarios.

A simple example of a Generator is the provided
:py:class:`~invenio_records_permissions.generators.RecordOwners` Generator:

.. code-block:: python

    from flask_principal import UserNeed


    class RecordOwners(Generator):
        '''Allows record owners.'''

        def needs(self, record=None, **kwargs):
            '''Enabling Needs.'''
            return [UserNeed(owner) for owner in record.get('owners', [])]

        def query_filter(self, record=None, **kwargs):
            '''Filters for current identity as owner.'''
            # NOTE: implementation subject to change until permissions metadata
            #       settled
            provides = g.identity.provides
            for need in provides:
                if need.method == 'id':
                    return Q('term', owners=need.value)
            return []

``RecordOwners`` allows any identity providing a `UserNeed
<https://pythonhosted.org/Flask-Principal/#flask_principal.UserNeed>`_
of value found in the ``owners`` metadata of a record. The
``query_filter(self, **kwargs)``
method outputs a query that returns all owned records of the current user.
Not included in the above, because it doesn't apply to ``RecordOwners``, is
the ``excludes(self, **kwargs)`` method.

.. Note::

    Exclusion has priority over inclusion. If a Need is returned by both
    ``needs`` and ``excludes``, providers of that Need will be **excluded**.

If implementation of Generators seems daunting, fear not! A collection of
them has already been implemented in
:py:mod:`~invenio_records_permissions.generators`
and they cover most cases you may have.

To fully understand how they work, we have to show where Generators are used.
That is in the Policies.


Policies
--------

Classes inheriting from
:py:class:`~invenio_records_permissions.policies.base.BasePermissionPolicy` are
referred to as Policies. They list **what actions** can be done **by whom**
over an implied category of objects (typically records). A Policy is
instantiated on a per action basis and is a descendant of `Permission
<https://invenio-access.readthedocs.io/en/latest/api.html
#invenio_access.permissions.Permission>`_ in
`invenio-access <https://invenio-access.readthedocs.io>`_ .
Generators are used to provide the "by whom" part and the implied category of
object.

Here is an example of a custom record Policy:

.. code-block:: python

    from invenio_records_permissions.generators import AnyUser, RecordOwners, \
        SuperUser
    from invenio_records_permissions.policies.base import BasePermissionPolicy

    class ExampleRecordPermissionPolicy(BasePermissionPolicy):
        can_create = [AnyUser()]
        can_search = [AnyUser()]
        can_read = [AnyUser()]
        can_update = [RecordOwners()]
        can_foo_bar = [SuperUser()]

The actions are class variables of the form: ``can_<action>`` and the
corresponding (dis-)allowed identities are a list of Generator instances.
One can define any action as long as it follows that pattern and
is verified at the moment it is undertaken.

In the example above, any user can create, list and read records, but only
a record's owner can edit it and only super users can perform the "foo_bar"
action.

We recommend you extend the provided
:py:class:`invenio_records_permissions.policies.records.RecordPermissionPolicy`
to customize record permissions for your instance.
This way you benefit from sane defaults.

After you have defined your own Policy, set it in your configuration:

.. code-block:: python

    RECORDS_PERMISSIONS_RECORD_POLICY = (
        'module.to.ExampleRecordPermissionPolicy'
    )

The succinct encoding of the permissions for your instance gives you
    - one central location where your permissions are defined
    - exact control
    - great flexibility by defining your own actions, generators and policies

In turn, to fully understand how Policies fit in an Invenio project, we have to
show where *they* are used. And *that* is in the Factories.


Factories
---------

Most authorization is enforced through permission factories in Invenio:
simple functions that return a `Permission
<https://invenio-access.readthedocs.io/en/latest/api.html
#invenio_access.permissions.Permission>`_ object. Thankfully, Policies are
just that kind of object.

Invenio-records-permissions provides you with pre-made configurable record
permission factories here:
:py:mod:`invenio_records_permissions.factories.records` . You can follow the
pattern there to create other factories you may need.

Pre-made factories
~~~~~~~~~~~~~~~~~~

By setting the following configuration in your instance:

.. code-block:: python

    RECORDS_PERMISSIONS_RECORD_POLICY = (
        'module.to.ExampleRecordPermissionPolicy'
    )
    RECORDS_REST_ENDPOINTS = {
        "recid": {
            # ...
            # We only display key-value pairs relevant to this explanation
            'read_permission_factory_imp': 'invenio_records_permissions.factories.record_read_permission_factory',  # noqa
            'list_permission_factory_imp': 'invenio_records_permissions.factories.record_search_permission_factory',  # noqa
            'create_permission_factory_imp': 'invenio_records_permissions.factories.record_create_permission_factory',  # noqa
            'update_permission_factory_imp': 'invenio_records_permissions.factories.record_update_permission_factory',  # noqa
            'delete_permission_factory_imp': 'invenio_records_permissions.factories.record_delete_permission_factory'  # noqa
        }
    }

you will be using the pre-made factories that know to look for their associated
action in ``module.to.ExampleRecordPermissionPolicy``.

Custom factories
~~~~~~~~~~~~~~~~

To implement your own factories, create a factory with the required signature
and return an instance of your custom PermissionPolicy object with the
appropriate action. For example:

.. code-block:: python

    def license_delete_permission_factory(license=None):
        '''Delete permission factory for license records.'''
        return LicensePermissionPolicy(action='delete', license=license)


With that, we covered all you need to know to fully specify access control in
your instance: combine and use permission Generators, Policies and Factories.

Custom Generators.
"""
from elasticsearch_dsl.query import Q
from invenio_records_permissions.generators import Generator


class RecordIp(Generator):
    """Allowed any user with accessing with the IP."""

    # TODO: Implement
    def needs(self, **kwargs):
        """Enabling Needs."""
        return []

    def excludes(self, **kwargs):
        """Preventing Needs."""
        return []

    def query_filter(self, **kwargs):
        """Elasticsearch filters."""
        return Q('match_all')
