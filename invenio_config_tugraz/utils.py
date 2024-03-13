# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils file."""

from flask_principal import Identity
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts
from invenio_saml.handlers import default_account_setup


def get_identity_from_user_by_email(email: str = None) -> Identity:
    """Get the user specified via email or ID."""
    if email is None:
        raise ValueError("the email has to be set to get a identity")

    user = current_accounts.datastore.get_user(email)

    if user is None:
        raise LookupError(f"user with {email} not found")

    identity = get_identity(user)

    # TODO: this is a temporary solution. this should be done with data from the db
    identity.provides.add(any_user)

    return identity


def tugraz_account_setup(user, account_info):
    """Add tugraz_authenticated role to user after SAML-login was acknowledged.

    Use as `account_setup`-argument to `invenio_saml.handlers.acs_handler_factory`.
    For this to work, the role tugraz_authenticated must have been created
    (e.g. via `invenio roles create tugraz_authenticated`).
    """
    # links external `account_info` with our database's `user` for future logins
    default_account_setup(user, account_info)

    user_email = account_info["user"]["email"]

    # NOTE: `datastore.commit`ing will be done by acs_handler that calls this func
    # NOTE: this is a No-Op when user_email already has role tugraz_authenticated
    current_accounts.datastore.add_role_to_user(user_email, "tugraz_authenticated")
