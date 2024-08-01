# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils file."""

import warnings
from collections.abc import Iterable
from itertools import chain
from typing import Iterator

from flask import current_app
from flask_principal import Identity
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts
from invenio_saml.handlers import acs_handler_factory

# these are from package `pysaml2` (import-name differs from package-name for some reason):
from saml2.config import Config
from saml2.mdstore import MetadataStore


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


def pick_squarest_logo(logo_dicts: Iterable[dict], default: str = "") -> str:
    """Pick from logo_dicts a logo whose width/height-ratio is closest to 1."""
    pick = default
    best_ratio = float("inf")
    for logo_dict in logo_dicts:
        text = logo_dict["text"]
        width = int(logo_dict["width"])
        height = int(logo_dict["height"])

        ratio = max(width, height) / min(width, height)
        if ratio < best_ratio:
            pick = text
            best_ratio = ratio

    return pick


def parse_into_saml_config(
    mds: MetadataStore,
    idp_id: str,
    langpref: str = "en",
) -> dict:
    """Parse SAML-XML into config compatible with `invenio-saml`.

    See invenio-saml's SSO_SAML_IDPS for structure of this function's output.
    """
    sso_urls: list[str] = mds.single_sign_on_service(
        idp_id,
        binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
    )
    if len(sso_urls) != 1:
        msg = f"{idp_id} has {len(sso_urls)} SSO-URLs for SAML's `Redirect` binding"
        raise ValueError(msg)
    # NOTE: by .xsd, "location"-key must exist here
    sso_url = sso_urls[0]["location"]

    certs: list[tuple[None, str]] = mds.certs(
        idp_id,
        descriptor="idpsso",
        use="signing",
    )
    if len(certs) < 1:
        msg = f"{idp_id} has no signing certificates"
        raise ValueError(msg)
    # there might be multiple signing certificates, by spec they should all work
    x509cert = certs[-1][1]

    # names/titles can be gotten from <md:Organization> or <mdui:DisplayName>
    preferred_display_names = list(
        mds.mdui_uiinfo_display_name(idp_id, langpref=langpref),
    )
    display_names = list(mds.mdui_uiinfo_display_name(idp_id))
    preferred_names = [name] if (name := mds.name(idp_id, langpref=langpref)) else []
    names = [name] if (name := mds.name(idp_id)) else []
    preferred_descriptions = list(
        mds.mdui_uiinfo_description(idp_id, langpref=langpref),
    )
    descriptions = list(mds.mdui_uiinfo_description(idp_id))

    # for title, prefer name in <md:Organization>
    title_iterator = chain(
        preferred_names,
        preferred_display_names,
        names,
        display_names,
    )
    title = next(title_iterator)

    # description
    desc_iterator = chain(
        preferred_descriptions,
        descriptions,
        preferred_display_names,
        preferred_names,
        display_names,
        names,
    )
    description = next(desc_iterator)

    icon = pick_squarest_logo(mds.mdui_uiinfo_logo(idp_id))

    return {
        "title": title,
        "description": description,
        "icon": icon,
        "sp_cert_file": "./saml/idp/cert/sp.crt",
        "sp_key_file": "./saml/idp/cert/sp.key",
        "settings": {
            "sp": {
                "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
            },
            "idp": {
                "singleSignOnService": {
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                    "url": sso_url,
                },
                "singleLougoutService": {},
                "x509cert": x509cert,
            },
            "security": {},  # leave at defaults
        },
        "mappings": {},
        "acs_handler": acs_handler_factory(idp_id),
        "auto_confirm": True,  # no need to click confirmation-link in some email
    }


def update_saml_idp_config(url) -> None:
    """Update SAML IdP config from url."""
    mds = MetadataStore(None, Config())
    # NOTE: http_client_timeout is in seconds
    mds.load("remote", url=url, http_client_timeout=5 * 60)

    idp_configs = {
        idp_id: parse_into_saml_config(mds, idp_id)
        for idp_id in mds.identity_providers()
    }
    # TODO: write `idp_configs` to db or redis or something...

