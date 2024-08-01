# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Celery tasks for `invenio_config_tugraz`."""

from celery import shared_task
from flask import current_app

from . import utils


@shared_task(ignore_result=True)
def update_saml_idp_config() -> None:
    """Celery task for updating SSO_SAML_IDPS."""
    url = current_app.config["CONFIG_TUGRAZ_SAML_UPDATE_URL"]
    utils.update_saml_idp_config(url)
