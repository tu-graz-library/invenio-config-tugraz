# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# contains code adapted from:
#   TU Wien's CRDM Disco Service (MIT-licensed)
#     https://gitlab.tuwien.ac.at/fairdata/crdm-disco-service/-/blob/main/app.py?ref_type=heads
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Click-based command-line interface for invenio-config-tugraz package."""

import sys
from collections.abc import Iterable
from copy import deepcopy
from itertools import chain

import black
import click
from saml2.config import Config
from saml2.mdstore import MetadataStore


@click.group()
def config_tugraz():
    """CLI-group for "invenio config-tugraz" commands."""


class StringRepresenter:
    """Represents itself exactly as the string passed to init, without quotes around it."""

    def __init__(self, string: str):
        """Init."""
        self.string = string

    def __repr__(self) -> str:
        """Repr."""
        # NOTE: `str.__repr__` would suffix/prefix with `"` here...
        return self.string

    def __str__(self) -> str:
        """Str."""
        return self.string


# when echoed, this represents as the configuration for TU Graz's SSO-IdP
TUGRAZ_IDP_ECHO_DICT = {
    # Basic info
    "title": "TUGRAZ",
    "description": "TUGRAZ shibboleth Authentication Service",
    "icon": "",
    # path to the file i.e. "./saml/sp.crt"
    "sp_cert_file": "./saml/idp/cert/sp.crt",
    "sp_key_file": "./saml/idp/cert/sp.key",
    "settings": {
        # If strict is True, then the Python Toolkit will reject unsigned
        # or unencrypted messages if it expects them to be signed or encrypted.
        # Also it will reject the messages if the SAML standard is not strictly
        # followed. Destination, NameId, Conditions ... are validated too.
        "strict": True,
        # Enable debug mode (outputs errors).
        "debug": True,
        # Service Provider Data that we are deploying.
        "sp": {
            # Specifies the constraints on the name identifier to be used to
            # represent the requested subject.
            # Take a look on https://github.com/onelogin/python-saml/blob/master/src/onelogin/saml2/constants.py
            # to see the NameIdFormat that are supported.
            "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        },
        # Identity Provider Data that we want connected with our SP.
        "idp": {
            # Identifier of the IdP entity  (must be a URI)
            "entityId": "https://auth.tugraz.at/auth/realms/tugraz",
            # SSO endpoint info of the IdP. (Authentication Request protocol)
            "singleSignOnService": {
                # URL Target of the IdP where the Authentication Request Message
                # will be sent.
                "url": "https://auth.tugraz.at/auth/realms/tugraz/protocol/saml",
                # SAML protocol binding to be used when returning the <Response>
                # message. OneLogin Toolkit supports the HTTP-Redirect binding
                # only for this endpoint.
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            # SLO endpoint info of the IdP.
            "singleLogoutService": {
                # URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)
                "url": "https://sso.tugraz.at/slo/Logout",
                # SAML protocol binding to be used when returning the <Response>
                # message. OneLogin Toolkit supports the HTTP-Redirect binding
                # only for this endpoint.
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            # Public X.509 certificate of the IdP
            "x509cert": "MIICmzCCAYMCBgFu/kDRhjANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZ0dWdyYXowHhcNMTkxMjEzMDc1MzExWhcNMjkxMjEzMDc1NDUxWjARMQ8wDQYDVQQDDAZ0dWdyYXowggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDXnaCOxODAXaobWyU0dBxlDSBC0n6YwvYyR1WCaCG57M2DZuA90aILgejhWn4X71al/+CixU5xRegIv7z843+CWBAcXkGQT/O/bfklzF2CvW2XtVftgCUwNOqnOynXA92Ge3YuJbIBxmK3/9XDiAuQ06+tmdZdTOaFyxfLX4TD+agwDd1v5MyK0B3f7yKZ+DEkXVhawj5gAgG+2XJFnM+3kY6tMmSG8af/GdXqnr3bYn1lAWzcRQgSkjasdMUgHpzp3NY2f48uQqoFuZ3frahNT+dl+hrfDC3Ix9D6ePtLBGRrraWBec/BrlcRr9SuaFq1SLGVSRKmkwE3KyyqLCLlAgMBAAEwDQYJKoZIhvcNAQELBQADggEBANMkjmxhXmiNe+uznV4SEWBrMpKEevOkwqrGnSEtx/QSZZ3G0GVHOSRTo+v6G7CukES2zSV1NHSTRbJSbrDK1UmS66N+x9PWfFMLIn0WN1acef5zp516F9qhVgcztjQPmfexIbpe5FYTuYWvptBWs5m4GgbWeBxtjimKS5dOjG5TskFtVH/MEcJk3LRqy8fIksg3Z5eREXQWzbjpvtz/9L/7n4+DzZprVr6VoBjsTn/AJ1d5Q0U9elKOM0o5G3pJWPhT6/gwVpkpqnH6AuGhcXZpxpAS+PGNJghhiJT8odFmoBur24ubYZVPVPDc10/1LKFIJT1vkB8bem/PrhHZDjw=",
        },
        # Security settings
        # more on https://github.com/onelogin/python-saml
        "security": {
            "authnRequestsSigned": False,
            "failOnAuthnContextMismatch": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "metadataCacheDuration": None,
            "metadataValidUntil": None,
            "nameIdEncrypted": False,
            "requestedAuthnContext": False,
            "requestedAuthnContextComparison": "exact",
            "signMetadata": False,
            "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
            "wantAssertionsEncrypted": False,
            "wantAssertionsSigned": False,
            "wantAttributeStatement": False,
            "wantMessagesSigned": False,
            "wantNameId": True,
            "wantNameIdEncrypted": False,
            "digestAlgorithm": "http://www.w3.org/2001/04/xmlenc#sha256",
        },
    },
    # Account Mapping
    # replace `origin_field` to IDP Attributes
    "mappings": {
        "email": "urn:oid:0.9.2342.19200300.100.1.3",
        "name": "urn:oid:2.5.4.42",
        "surname": "urn:oid:2.5.4.4",
        "external_id": "urn:oid:1.3.6.1.4.1.5923.1.1.1.6",
        # Custom - not used
        # 'org_id': 'urn:oid:CO-ORGUNITID',  # orgunitid
        # 'org_name': 'urn:oid:CO-ORGUNITNAME',  # orgunitname
        # 'identifier': 'urn:oid:CO-IDENTNR-C-oid'  # oid:CO-IDENTNR-C-oid
    },
    # Inject your remote_app to handler
    # Note: keep in mind the string should match
    # given name for authentication provider
    "acs_handler": StringRepresenter('acs_handler_factory("idp")'),
    "auto_confirm": True,
}


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


def parse_into_config(mds: MetadataStore, idp_id: str, langpref: str = "en") -> dict:
    """Parse SAML-XML into config compatible with `invenio-saml`."""
    # see invenio-saml for structure of this configuration

    sso_urls: list[str] = mds.single_sign_on_service(
        idp_id, binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    )
    if len(sso_urls) != 1:
        raise ValueError(
            f"{idp_id} has {len(sso_urls)} SSO-URLs for SAML's `Redirect` binding"
        )
    # NOTE: by .xsd, "location"-key must exist here
    sso_url = sso_urls[0]["location"]

    certs: list[tuple[None, str]] = mds.certs(
        idp_id, descriptor="idpsso", use="signing"
    )
    if len(certs) < 1:
        raise ValueError(f"{idp_id} has no signing certificates")
    # there might be multiple signing certificates, by spec they should all work
    x509cert = certs[-1][1]

    # names/titles can be gotten from <md:Organization> or <mdui:DisplayName>
    preferred_display_names = list(
        mds.mdui_uiinfo_display_name(idp_id, langpref=langpref)
    )
    display_names = list(mds.mdui_uiinfo_display_name(idp_id))
    preferred_names = [name] if (name := mds.name(idp_id, langpref=langpref)) else []
    names = [name] if (name := mds.name(idp_id)) else []
    preferred_descriptions = list(
        mds.mdui_uiinfo_description(idp_id, langpref=langpref)
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
        "acs_handler": StringRepresenter(f'acs_handler_factory("{str(idp_id)}")'),
        "auto_confirm": True,  # no need to click confirmation-link in some email
    }


def should_be_parsed(idp_id: str) -> bool:
    """Whether `idp_id` should be parsed."""
    # tugraz config isn't parsed from SAML-XML, but rather custom-configured to use our SSO
    return "tugraz" not in idp_id


@config_tugraz.command()
@click.option(
    "-f", "--file", help="path to SAML-XML file, mutually exclusive with --url"
)
@click.option(
    "-u", "--url", help="url to SAML-XML file, mutually exclusive with --file"
)
def echo_saml_config(file: str | None = None, url: str | None = None):
    """Parse SAML-XML into `invenio-saml`-compatible config, echo that config to stdout.

    Prints configuration to stdout, prints some notes to stderr.

    \b
    examples:
        invenio config-tugraz echo-saml-config --url "https://eduid.at/md/aconet-registered.xml" > output
        invenio config-tugraz echo-saml-config --file "/path/to/eduid.xml" | my-clipboard
    """
    if file and url:
        click.secho(
            "`--file` and `--url` are mutually exclusive", file=sys.stderr, fg="red"
        )
        sys.exit(1)

    # load into parser
    mds = MetadataStore(None, Config())
    if file:
        mds.load("local", file)
    elif url:
        mds.load("remote", url=url)
    else:
        click.secho(
            "must give exactly one of `--file`, `--url`", file=sys.stderr, fg="red"
        )
        sys.exit(1)

    # parse into dict whose `repr` is copyable to config-file
    echo_dict = {
        "idp": deepcopy(TUGRAZ_IDP_ECHO_DICT),
    }
    echo_dict.update(
        {
            idp_id: parse_into_config(mds, idp_id)
            for idp_id in mds.identity_providers()
            if should_be_parsed(idp_id)
        }
    )

    # create to-be-echoed output-string
    output = (
        "from invenio_saml.handlers import default_account_setup, acs_handler_factory\n"
        "from invenio_config_tugraz.utils import tugraz_account_setup_extension\n"
        "\n"
        "def tugraz_account_setup(user, account_info):\n"
        "    default_account_setup(user, account_info)\n"
        "    tugraz_account_setup_extension(user, account_info)\n"
        "\n"
        f"SSO_SAML_IDPS = {echo_dict!r}\n"
    )
    output = black.format_str(output, mode=black.FileMode())
    click.echo(output)

    click.secho(
        "add the stdout-output to your invenio.cfg file\n"
        "\n"
        "NOTE: for this to work correctly:\n"
        "- the role `tugraz_authenticated_user` must exist\n"
        "- `RDM_PERMISSION_POLICY` should be set to `TUGrazRDMRecordPermissionPolicy`",
        file=sys.stderr,
        fg="yellow",
    )
