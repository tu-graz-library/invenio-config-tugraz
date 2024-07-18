# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils file."""

import warnings

from flask_principal import Identity
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts


def get_identity_from_user_by_email(email: str | None = None) -> Identity:
    """Get the user specified via email or ID."""
    warnings.warn("deprecated", DeprecationWarning, stacklevel=2)

    if email is None:
        msg = "the email has to be set to get a identity"
        raise ValueError(msg)

    user = current_accounts.datastore.get_user(email)

    if user is None:
        msg = f"user with {email} not found"
        raise LookupError(msg)

    identity = get_identity(user)

    # TODO: this is a temporary solution. this should be done with data from the db
    identity.provides.add(any_user)

    return identity


def tugraz_account_setup_extension(user, account_info) -> None:  # noqa: ANN001, ARG001
    """Add tugraz_authenticated role to user after SAML-login was acknowledged.

    To use, have `acs_handler_factory` call invenio_saml's `default_account_setup` first,
    then this function second.

    .. code-block:: python

        # invenio.cfg
        from invenio_saml.handlers import default_account_setup, acs_handler_factory

        def tugraz_account_setup(user, account_info):
            # links external `account_info` with our database's `user` for future logins
            default_account_setup(user, account_info)
            tugraz_account_setup_extension(user, account_info)

        SSO_SAML_IDPS = {
            "my-tugraz-idp": {
                ...
                "acs_handler": acs_handler_factory(
                    "my-tugraz-idp", account_setup=tugraz_account_setup
                )
            }
        }

    For this to work, the role tugraz_authenticated must have been created
    (e.g. via `invenio roles create tugraz_authenticated`).
    """
    user_email = account_info["user"]["email"]

    # NOTE: `datastore.commit`ing will be done by acs_handler that calls this func
    # NOTE: this is a No-Op when user_email already has role tugraz_authenticated
    current_accounts.datastore.add_role_to_user(user_email, "tugraz_authenticated")
