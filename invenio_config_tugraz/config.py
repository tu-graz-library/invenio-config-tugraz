# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from os.path import abspath, dirname, join

from flask_babelex import gettext as _

INVENIO_CONFIG_TUGRAZ_SHIBBOLETH = False
"""Set True if SAML is configured"""

INVENIO_CONFIG_TUGRAZ_SINGLE_IP = []
"""Allows access to users whose IP address is listed.

INVENIO_CONFIG_TUGRAZ_SINGLE_IP =
    ["127.0.0.1", "127.0.0.2"]
"""

INVENIO_CONFIG_TUGRAZ_IP_RANGES = []
"""Allows access to users whose range of IP address is listed.

INVENIO_CONFIG_TUGRAZ_IP_RANGES =
[["127.0.0.2", "127.0.0.99"], ["127.0.1.3", "127.0.1.5"]]
"""

# Invenio-App
# ===========
# See https://invenio-app.readthedocs.io/en/latest/configuration.html

APP_ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "127.0.0.1",
    "invenio-dev01.tugraz.at",
    "invenio-test.tugraz.at",
    "repository.tugraz.at",
]
"""Allowed Hosts"""

APP_DEFAULT_SECURE_HEADERS = {
    "content_security_policy": {
        "default-src": [
            "'self'",
            "fonts.googleapis.com",
            "*.gstatic.com",
            "data:",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "blob:",
            "ub-support.tugraz.at",  # zammad contact form
            "api.datacite.org/dois",  # datacite
            "api.test.datacite.org/dois",  # datacite test
        ],
    },
    "content_security_policy_report_only": False,
    "content_security_policy_report_uri": None,
    "force_file_save": False,
    "force_https": True,
    "force_https_permanent": False,
    "frame_options": "sameorigin",
    "frame_options_allow_from": None,
    "session_cookie_http_only": True,
    "session_cookie_secure": True,
    "strict_transport_security": True,
    "strict_transport_security_include_subdomains": True,
    "strict_transport_security_max_age": 31556926,  # One year in seconds
    "strict_transport_security_preload": False,
}

# Invenio-Mail
# ===========
# See https://invenio-mail.readthedocs.io/en/latest/configuration.html

MAIL_SERVER = "localhost"
"""Domain ip where mail server is running."""

SECURITY_EMAIL_SENDER = "info@invenio-test.tugraz.at"
"""Email address used as sender of account registration emails."""
"""Domain name should match the domain used in web server."""

SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to TU Graz Repository!")
"""Email subject for account registration emails."""

MAIL_SUPPRESS_SEND = True
"""Enable email sending by default.

Set this to False when sending actual emails.
"""

# CORS - Cross-origin resource sharing
# ===========
# Uncomment to enable the CORS

# CORS_RESOURCES = '*'
# CORS_SEND_WILDCARD = True
# CORS_EXPOSE_HEADERS = [
#    'ETag',
#    'Link',
#    'X-RateLimit-Limit',
#    'X-RateLimit-Remaining',
#    'X-RateLimit-Reset',
#    'Content-Type',
# ]
# REST_ENABLE_CORS = True

# Invenio-userprofiles
# ===========
# See https://invenio-userprofiles.readthedocs.io/en/latest/configuration.html

USERPROFILES_EXTEND_SECURITY_FORMS = False
"""Set True in order to register user_profile.

This also forces user to add username and fullname
when register.
"""

USERPROFILES_EMAIL_ENABLED = False
"""Exclude the user email in the profile form."""

# Invenio-shibboleth
# ===========
# See https://invenio-shibboleth.readthedocs.io/en/latest/configuration.html

SSO_SAML_IDPS = {}
"""Configuration of IDPS. Actual values can be find in to invenio.cfg file"""

SSO_SAML_DEFAULT_BLUEPRINT_PREFIX = "/shibboleth"
"""Base URL for the extensions endpoint."""

SSO_SAML_DEFAULT_METADATA_ROUTE = "/metadata/<idp>"
"""URL route for the metadata request."""
"""This is also SP entityID https://domain/shibboleth/metadata/<idp>"""

SSO_SAML_DEFAULT_SSO_ROUTE = "/login/<idp>"
"""URL route for the SP login."""

SSO_SAML_DEFAULT_ACS_ROUTE = "/authorized/<idp>"
"""URL route to handle the IdP login request."""

SSO_SAML_DEFAULT_SLO_ROUTE = "/slo/<idp>"
"""URL route for the SP logout."""

SSO_SAML_DEFAULT_SLS_ROUTE = "/sls/<idp>"
"""URL route to handle the IdP logout request."""

# Invenio-accounts
# ===========
# See https://invenio-accounts.readthedocs.io/en/latest/configuration.html

SECURITY_CHANGEABLE = False
"""Allow password change by users."""

SECURITY_RECOVERABLE = False
"""Allow password recovery by users."""

SECURITY_REGISTERABLE = False
""""Allow users to register.

With this variable set to "False" users will not be
able to register, or to navigate to /sigup page.
"""

SECURITY_CONFIRMABLE = False
"""Allow user to confirm their email address.

Instead user will get a welcome email.
"""

# Flask-Security
# =============
# See https://pythonhosted.org/Flask-Security/configuration.html
SECURITY_EMAIL_PLAINTEXT = True
"""Render email content as plaintext."""

SECURITY_EMAIL_HTML = False
"""Render email content as HTML."""


ACCOUNTS = True
"""Tells if the templates should use the accounts module.

If False, you won't be able to login via the web UI.

Instead if you have a overriden template somewhere in your config.py:
like this:
SECURITY_LOGIN_USER_TEMPLATE = 'invenio_theme_tugraz/accounts/login.html'
then you can remove this condition from header_login.htm:
{%- if config.ACCOUNTS %}
to render your overriden login.html
"""

# Accounts
# ========
# Actual values can be find in to invenio.cfg file
#: Recaptcha public key (change to enable).
RECAPTCHA_PUBLIC_KEY = None
#: Recaptcha private key (change to enable).
RECAPTCHA_PRIVATE_KEY = None

# invenio-records-permissions
# =======
# See:
# https://invenio-records-permissions.readthedocs.io/en/latest/configuration.html
# Uncomment these to enable overriding RDM permissions
# from .rdm_permissions import TUGRAZRDMRecordServiceConfig
# RDM_RECORDS_BIBLIOGRAPHIC_SERVICE_CONFIG = TUGRAZRDMRecordServiceConfig
"""Access control configuration for records."""

# invenio-rdm-records
# =======
# See:
# https://invenio-rdm-records.readthedocs.io/en/latest/configuration.html
#
RDM_RECORDS_USER_FIXTURE_PASSWORDS = {"info@tugraz.at": None}
"""Overrides for the user fixtures' passwords.
The password set for a user fixture in this dictionary overrides the
password set in the ``users.yaml`` file. This can be used to set custom
passwords for the fixture users (of course, this has to be configured
before the fixtures are installed, e.g. by setting up the services).
If ``None`` or an empty string is configured in this dictionary, then the
password from ``users.yaml`` will be used. If that is also absent, a password
will be generated randomly.
"""

# Custom Access Right
# RDM_RECORDS_CUSTOM_VOCABULARIES = {
#     'access_right': {
#         'path': join(
#             dirname(abspath(__file__)),
#             'restrictions', 'access_right', 'access_right_limit.csv'
#         )
#     }
# }

# Invenio-app-rdm
# =========================
# See https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py
APP_RDM_DEPOSIT_FORM_DEFAULTS = {}
"""Default values for new records in the deposit UI.

The keys denote the dot-separated path, where in the record's metadata
the values should be set (see invenio-records.dictutils).
If the value is callable, its return value will be used for the field
(e.g. lambda/function for dynamic calculation of values).
"""

SQLALCHEMY_ECHO = False
"""Enable to see all SQL queries."""

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": False,
    "pool_recycle": 3600,
    # set a more agressive timeout to ensure http requests don't wait for long
    "pool_timeout": 10,
}
"""SQLAlchemy engine options.

This is used to configure for instance the database connection pool.
Specifically for connection pooling the following options below are relevant.
Note, that the connection pool settings have to be aligned with:

1. your database server's max allowed connections settings, and
2. your application deployment (number of processes/threads)

**Disconnect handling**

Note, it's possible that a connection you get from the connection pool is no
longer open. This happens if e.g. the database server was restarted or the
server has a timeout that closes the connection. In these case you'll see an
error similar to::

    psycopg2.OperationalError: server closed the connection unexpectedly
        This probably means the server terminated abnormally
        before or while processing the request.

The errors can be avoided by using the ``pool_pre_ping`` option, which will
ensure the connection is open first by issuing a ``SELECT 1``. The pre-ping
feature however, comes with a performance penalty, and thus it may be better
to first try adjusting the ``pool_recyle`` to ensure connections are closed and
reopened regularly.

... code-block:: python

    SQLALCHEMY_ENGINE_OPTIONS = dict(
        # enable the connection pool “pre-ping” feature that tests connections
        # for liveness upon each checkout.
        pool_pre_ping=True,

        # the number of connections to allow in connection pool “overflow”,
        # that is connections that can be opened above and beyond the
        # pool_size setting
        max_overflow=10,

        # the number of connections to keep open inside the connection
        pool_size=5,

        # recycle connections after the given number of seconds has passed.
        pool_recycle=3600,

        # number of seconds to wait before giving up on getting a connection
        # from the pool
        pool_timeout=30,

    )

See https://docs.sqlalchemy.org/en/latest/core/engines.html.
"""
