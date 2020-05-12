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

# Mail server
MAIL_SERVER = '129.27.11.182'
SECURITY_EMAIL_SENDER = 'info@invenio-rdm.tugraz.at'
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to RDM!'
MAIL_SUPPRESS_SEND = False

# Shibboleth config
# set True if SAML is configured.
SHIBBOLETH_ISACTIVE = 'False'
