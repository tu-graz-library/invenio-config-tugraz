# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

# TODO: This is an example file. Remove it if your package does not use any
# extra configuration variables.

# from invenio_saml.handlers import acs_handler_factory

"""invenio-saml import"""

INVENIO_CONFIG_TUGRAZ_DEFAULT_VALUE = 'foobar'
"""Default value for the application."""

INVENIO_CONFIG_TUGRAZ_BASE_TEMPLATE = 'invenio_config_tugraz/base.html'
"""Default base template for the demo page."""

# Allowed Hosts
APP_ALLOWED_HOSTS = ['0.0.0.0',
                     'localhost',
                     '127.0.0.1',
                     'invenio-dev01.tugraz.at',
                     'invenio-test.tugraz.at'
                     ]

# Allow the statics to build
APP_DEFAULT_SECURE_HEADERS = {
    'content_security_policy': {
        'default-src': [
            "'self'",
            'fonts.googleapis.com',
            '*.gstatic.com',
            'data:',
            "'unsafe-inline'",
            "'unsafe-eval'",
            "blob:",
        ],
    },
    'content_security_policy_report_only': False,
    'content_security_policy_report_uri': None,
    'force_file_save': False,
    'force_https': True,
    'force_https_permanent': False,
    'frame_options': 'sameorigin',
    'frame_options_allow_from': None,
    'session_cookie_http_only': True,
    'session_cookie_secure': True,
    'strict_transport_security': True,
    'strict_transport_security_include_subdomains': True,
    'strict_transport_security_max_age': 31556926,  # One year in seconds
    'strict_transport_security_preload': False,
}

# --------------- Mail server
MAIL_SERVER = '129.27.11.182'
SECURITY_EMAIL_SENDER = 'info@invenio-rdm.tugraz.at'
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to RDM!'
MAIL_SUPPRESS_SEND = False

# --------------- Shibboleth config
# set True if SAML is configured.
INVENIO_CONFIG_TUGRAZ_SHIBBOLETH = 'True'

SSO_SAML_IDPS = {

    'idp': {
        # settings.json or settings.xml
        # Idp
        "settings_file_path": "./saml/idp/idp.json",

        # service provider
        "sp_cert_file": "./saml/idp/cert/sp.crt",

        # service provider private key
        "sp_key_file": "./saml/idp/cert/sp.key",

        # sp settings
        'settings': {
            'sp': {
                'NameIDFormat':
                'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
                'entityId':
                'https://invenio-dev01/shibboleth',
            },
        },
        # mapping
        'mappings': {
            # invenio # origin
            'email': 'urn:oid:0.9.2342.19200300.100.1.3',
            'username': 'urn:oid:2.5.4.42',  # Name
            'full_name': 'urn:oid:2.5.4.4',  # Surname
            'external_id': 'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',

            # Custom
            'org_id': 'urn:oid:CO-ORGUNITID',  # orgunitid
            'org_name': 'urn:oid:CO-ORGUNITNAME',  # orgunitname
            'identifier': 'urn:oid:CO-IDENTNR-C-oid'  # oid:CO-IDENTNR-C-oid
        },
        # 'acs_handler': acs_handler_factory('idp'),
    },

    'onelogin': {
        # settings.json or settings.xml
        # Idp
        "settings_file_path": "./saml/onelogin/onelogin.json",

        # service provider
        "sp_cert_file": "./saml/onelogin/cert/sp.crt",

        # service provider private key
        "sp_key_file": "./saml/onelogin/cert/sp.key",

        # mappings
        "mappings": {

            # invenio  #origin
            "email": "email",
            "username": "username",
            "full_name": "full_name",
            "external_id": "external_id"
        },

        # remove this line
        #'acs_handler': acs_handler_factory('onelogin'),

    },

}

# Blueprint and routes default configuration
SSO_SAML_DEFAULT_BLUEPRINT_PREFIX = '/shibboleth'
"""Base URL for the extensions endpoint."""

SSO_SAML_DEFAULT_METADATA_ROUTE = '/metadata/<idp>'
"""URL route for the metadata request."""
"""This is also SP entityID https://domain/shibboleth/metadata/<idp>"""

SSO_SAML_DEFAULT_SSO_ROUTE = '/login/<idp>'
"""URL route for the SP login."""

SSO_SAML_DEFAULT_ACS_ROUTE = '/authorized/<idp>'
"""URL route to handle the IdP login request."""

SSO_SAML_DEFAULT_SLO_ROUTE = '/slo/<idp>'
"""URL route for the SP logout."""

SSO_SAML_DEFAULT_SLS_ROUTE = '/sls/<idp>'
"""URL route to handle the IdP logout request."""
