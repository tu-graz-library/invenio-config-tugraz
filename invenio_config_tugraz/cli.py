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

import pathlib
import sys
from collections.abc import Iterable
from functools import partial
from importlib import resources
from importlib.abc import Traversable
from itertools import chain

import black
import click
from jinja2 import Environment, loaders
from saml2.config import Config
from saml2.mdstore import MetadataStore


@click.group()
def config_tugraz() -> None:
    """CLI-group for "invenio config-tugraz" commands."""


class StringRepresenter:
    """Represents itself exactly as the string passed to init, without quotes around it."""

    def __init__(self, string: str) -> None:
        """Init."""
        self.string = string

    def __repr__(self) -> str:
        """Repr."""
        # NOTE: `str.__repr__` would suffix/prefix with `"` here...
        return self.string

    def __str__(self) -> str:
        """Str."""
        return self.string


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
        "acs_handler": StringRepresenter(f'acs_handler_factory("{idp_id}")'),
        "auto_confirm": True,  # no need to click confirmation-link in some email
    }


def exclude_item_if_includes(input_dict: dict, *exclusions: str) -> dict:
    """Jinja-filter for excluding items from a dict."""
    return {k: v for k, v in input_dict.items() if all(e not in k for e in exclusions)}


@config_tugraz.command()
@click.option(
    "-f",
    "--file",
    help="path to SAML-XML file, mutually exclusive with --url",
)
@click.option(
    "-u",
    "--url",
    help="url to SAML-XML file, mutually exclusive with --file",
)
@click.option(
    "-t",
    "--template-path",
    help="path to jinja-template for formatting output",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
)
def echo_saml_config(
    file: str | None = None,
    url: str | None = None,
    template_path: pathlib.Path | None = None,
) -> None:
    """Parse SAML-XML into `invenio-saml`-compatible config, echo that config to stdout.

    Prints configuration to stdout, prints some notes to stderr.

    \b
    examples:
        invenio config-tugraz echo-saml-config --url "https://eduid.at/md/aconet-registered.xml" > output
        invenio config-tugraz echo-saml-config --file "/path/to/eduid.xml" | my-clipboard
    """  # noqa: D301  # allow backspace `\b`, which prevents click from wrapping newlines
    if template_path is None:
        template_path: Traversable = resources.files(__package__).joinpath(
            "config_templates",
            "tugraz",
            "saml.cfg.jinja",
        )

    jinja_env = Environment(loader=loaders.BaseLoader())  # noqa: S701
    jinja_env.globals["format_str"] = partial(black.format_str, mode=black.FileMode())
    jinja_env.globals["repr"] = repr
    jinja_env.filters["exclude_item_if_includes"] = exclude_item_if_includes
    template = jinja_env.from_string(template_path.read_text())

    if file and url:
        click.secho(
            "`--file` and `--url` are mutually exclusive",
            file=sys.stderr,
            fg="red",
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
            "must give exactly one of `--file`, `--url`",
            file=sys.stderr,
            fg="red",
        )
        sys.exit(1)

    # parse into dict whose `repr` is copyable to config-file
    echo_dict = {
        idp_id: parse_into_config(mds, idp_id) for idp_id in mds.identity_providers()
    }

    # create to-be-echoed output-string
    output = template.render(echo_dict=echo_dict)
    click.echo(output)

    # output notes to stderr
    notes_path = template_path.parent.joinpath("notes.jinja")
    notes = "add the stdout-output to your invenio.cfg file"
    if notes_path.exists():
        notes_template = jinja_env.from_string(notes_path.read_text())
        notes = notes_template.render()
    click.secho(
        notes,
        file=sys.stderr,
        fg="yellow",
    )
