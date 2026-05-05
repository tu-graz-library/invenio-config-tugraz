# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils file."""

import warnings

from flask import current_app
from flask_principal import Identity
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts
from invenio_oauthclient.contrib.keycloak import setup_handler
from invenio_oauthclient.contrib.keycloak.handlers import info_serializer_handler
from invenio_oauthclient.contrib.keycloak.helpers import get_user_info


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


def tugraz_setup_handler(remote, token, resp) -> None:  # noqa: ANN001
    """Perform additional setup after the user has been logged in.

    Overrides the handler from invenio_oauthclient.contrib.keycloak by adding the TUG
    specific role to the user.

    To use this, one would need to override the remote app helper in invenio.cfg, e.g.:

    .. code-block:: python
        from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper

        _keycloak_helper = KeycloakSettingsHelper(
          title="Example",
          description="Example",
          base_url="http://127.0.0.1:8087/",
          realm="testrealm",
          app_key="KEYCLOAK_APP_CREDENTIALS",
        )


        _keycloak_helper.remote_app["signup_handler"]["setup"] = "invenio_config_tugraz.config:tugraz_setup_handler"
        OAUTHCLIENT_REMOTE_APPS = {
            "keycloak": _keycloak_helper.remote_app,
        }

    For this to work, the role tugraz_authenticated must have been created
    (e.g. via `invenio roles create tugraz_authenticated`).
    """
    token_user_info, _ = get_user_info(remote, resp, from_token_only=True)

    user_email = token_user_info["email"]
    current_accounts.datastore.add_role_to_user(user_email, "tugraz_authenticated")

    return setup_handler(remote, token, resp)


def tugraz_info_serializer(
    remote,  # noqa: ANN001
    resp,  # noqa: ANN001
    token_user_info,  # noqa: ANN001
    user_info,  # noqa: ANN001
) -> dict:
    """Serialize the account info response object.

    Override the core OAuth serializer to support configuring user information fields
    different than the default implementation.

    For now, 2 fields are of interest: username & external_id.

    To use this override, modify invenio.cfg:
    .. code-block:: python
           _keycloak_helper = KeycloakSettingsHelper(
              title="Example",
              description="Example",
              base_url="http://127.0.0.1:8087/",
              realm="testrealm",
              app_key="KEYCLOAK_APP_CREDENTIALS",
            )
            _keycloak_helper.remote_app["signup_handler"]["info_serializer"] = "invenio_config_tugraz.config:tugraz_info_serializer"

            CONFIG_TUGRAZ_OAUTH_USERNAME_ATTRIBUTE = "sub"
            CONFIG_TUGRAZ_OAUTH_EXTERNAL_ID_ATTRIBUTE = "sub"
    """
    username_attr = current_app.config.get("CONFIG_TUGRAZ_OAUTH_USERNAME_ATTRIBUTE")
    if not username_attr:
        return info_serializer_handler(remote, resp, token_user_info, user_info)

    user_info_tugraz = info_serializer_handler(remote, resp, token_user_info, user_info)
    token_value_username = token_user_info.get(username_attr)

    if not token_value_username:
        msg = f"{username_attr} not present in Keycloak token"
        raise ValueError(msg)

    username_prefix = current_app.config.get("CONFIG_TUGRAZ_OAUTH_USERNAME_PREFIX")
    user_info_tugraz["user"]["profile"]["username"] = (
        f"{username_prefix}-{token_value_username}"
        if username_prefix
        else token_value_username
    )

    external_id_attr = current_app.config.get(
        "CONFIG_TUGRAZ_OAUTH_EXTERNAL_ID_ATTRIBUTE",
    )
    if not external_id_attr:
        return user_info_tugraz

    token_value_externalid = token_user_info.get(external_id_attr)
    if not token_value_externalid:
        msg = f"{external_id_attr} not present in Keycloak token"
        raise ValueError(msg)

    user_info_tugraz["external_id"] = token_value_externalid
    return user_info_tugraz
