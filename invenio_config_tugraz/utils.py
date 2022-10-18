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
