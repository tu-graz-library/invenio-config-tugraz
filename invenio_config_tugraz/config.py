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

from invenio_saml.handlers import acs_handler_factory

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
        'settings': {
            'debug': True,
            'idp': {
                'entityId': 'https://sso.tugraz.at/idp/shibboleth',
                'singleLogoutService': {
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
                    'url': 'https://sso.tugraz.at/slo/Logout'
                },

                'singleSignOnService': {
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
                    'url': 'https://sso.tugraz.at/idp/profile/SAML2/Redirect/SSO'
                },

                'x509cert': 'MIIDHzCCAgegAwIBAgIUG6ra0BvXswfyErcCDmzw3AV+uI0wDQYJKoZIhvcNAQEFBQAwGDEWMBQGA1UEAxMNc3NvLnR1Z3Jhei5hdDAeFw0xMDAzMjkxNzEzMTZaFw0zMDAzMjkxODEzMTZaMBgxFjAUBgNVBAMTDXNzby50dWdyYXouYXQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCEyQxHIM1zxbBnXn60Ksg7B7HcPLPcN7bXLrLPOFXtkZxm0YkHY5Rxignm7wHD7C81U09DFS2eT8qRCcVtVz+kuwdgS54fC/alg9oLxXk4CgKjhtZZ2ECLdTHfUXOA5uOLlpoN1LY6VpIjSYe3UEX3HxfhXx/fPeE8VInGCKnml8Too22G30htB/EU44A2yqrR3LUngJIaq //N0QbeMYitNh02o6xB5+bp6k6noM7DH6S9phe0kCEibaiLaCf7k9LpNnAz9bPtQVth0gdJqoUry/iK1QBTFTEXvvJynFEp0+5Wz/XFmEcFhsaK8OcHd0R9FfpX5Z2fewA2Q0SLKz+bAgMBAAGjYTBfMD4GA1UdEQQ3MDWCDXNzby50dWdyYXouYXSGJGh0dHBzOi8vc3NvLnR1Z3Jhei5hdC9pZHAvc2hpYmJvbGV0aDAdBgNVHQ4EFgQUXd76PcSiXR6wFna5qQi+S0W/9Y0wDQYJKoZIhvcNAQEFBQADggEBACgkQqxBtYY1OcuoAUP/P+ukJW7XyofK89qs2dkGClx7s0hR/1zImWgljgfguLJOSfC/CWE1wfNK9bTi4Fu9809PmOoaCxkNmniFRAyaOiBoUz5XIpJniW7wBo+YBpBlXZXi5PmU2DOsfZxo7fs4se32dHO1WqgJodqkK2Wa4HDiigh42trZ9i3uS73uHSSCeIJYQNj84BMJ+ifgj3Zi/TgLS+IX7Ayy2bkDzIzIRnj7ULQ/MgfacGXQXJPHyp+w+YvydQalPAWc43+5DkNacN34K8cE3XjHq1kx/BgYOtQ7M2Xa1oApLzPoHO4D2kaf6FCgGR8Mx7GVAz0aQVxfB8I='
            },

            'sp': {
                'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',

                'entityId': 'https://invenio-dev01/shibboleth',
                'privateKey': 'MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIHxNp8P2PsV8CAggAMBQGCCqGSIb3DQMHBAjOyik6fsEC3gSCAoC4tFsYAl4GexyXESiRKpOQzHQNFtQtwDEevT1IKgsafSNjOMJZLKrnoejNoxEQUPPPXgGEd83Fmp2cSHm+YVksH06zcsA+RKf5ab6t0bsgcyljGzkHEDQtMRPcaXNlVMbU9VEDOX26MgmlU/pd+GGfE99IbEFc6qN1e7qOnmKSw93Q3o05ubO3wEI76JhOioGGXB3pEn8f4XLDwck0thzYD6H2vdF+kyIdM8w1BgyLdeP0aDkfG1V3rLGhE8246rwVUzRSZv6BCNBZFk7YO1d7j0+BDxnbHFS631zdCgMcd/XS8u6acc3IYr/bQLH4a1y0X3Z+8ks8arEgUtXqYx9wMlp5lajlsr9JDIU5OnuZ2XY+4sqDQsTZPjBpxK8oMjvJNNatnTf+18htkTdovpInlP7xpEjp1L7H74iKY25UsAZ9e+gqHZwILnk418mQ1E4JYU6JRUZspJSFfqwn9FL6DnvhzPIhtzwhr3eL4f4RXWxxe2xCzvWg+GaWuMfZdj77SV4pMOi7vb3HlYY6luShVlYKdSaw+jf6XVy4ZMTWT5wcE1mc3tAJqF18Mi8amOetpZhz16ISOKnO0rKrfmxteNPQn2AB8QquGGn050PTW4m8zFXDBiyg2xvcRLAW/8ych3k+pkEZi4tVCkLcHM56J/XUEKMCxiSok+vbzxfVf1D2vYFFS7Lw1nP5RnLKFdn8XdHQ+lu2diod18wYBQP4eoU+XjjP2zjlpULiWHt7PpCERqGg7H2Z2amIL5rTeqQuyXczw1/xG/VBNn9qe3DXFodvoV6OZb3efNT/eJgOyaPLi2FmB7Kpdp4JIdJgLnaBCwNBXkpGSwb732O/cug8',

                'x509cert': 'MIICjjCCAfegAwIBAgIBADANBgkqhkiG9w0BAQ0FADBkMQswCQYDVQQGEwJhdDENMAsGA1UECAwER3JhejEPMA0GA1UECgwGVFVHUkFaMRAwDgYDVQQDDAdpbnZlbmlvMSMwIQYJKoZIhvcNAQkBFhRtb2ppYi53YWxpQHR1Z3Jhei5hdDAeFw0yMDAxMTAyMDIwMTlaFw0yMTAxMDkyMDIwMTlaMGQxCzAJBgNVBAYTAmF0MQ0wCwYDVQQIDARHcmF6MQ8wDQYDVQQKDAZUVUdSQVoxEDAOBgNVBAMMB2ludmVuaW8xIzAhBgkqhkiG9w0BCQEWFG1vamliLndhbGlAdHVncmF6LmF0MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5ZrPhRhyDyLTe93rpgqN9MMfnCsg+2QBW4EOuQnMXJzF1dqrFEsexot1FRW83IjqbY+680PmGABQtxUpS4Kinr/pLYbPhQ2WPQRad7mtOn/dD40VVwfG0GfcLrnKe5F4QLfNjervjl8jH/AKPCYwwfSeuw1LNoRjy1uDwkp9cRQIDAQABo1AwTjAdBgNVHQ4EFgQUPv2+wS1RuagCOed7w1FzouBmpP4wHwYDVR0jBBgwFoAUPv2+wS1RuagCOed7w1FzouBmpP4wDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQ0FAAOBgQA4qvU7gbgE/MoljUW68qMPs8z8Q2Ngttp6F1KOMNO9rgrYWAJh4u6BMt11mlBgBlLLJzG67wXpBr0l78IcOXun4w955te0VRp7aZ0b1uOPt0aUoDOXuBAhZURLZfbsogpWiE6bdB8N0nHTwk2WG2PPIC5Z99UdDivcP5ZeSPAkUw=='

            },
            'security': {
                'authnRequestsSigned': False,
                'failOnAuthnContextMismatch': False,
                'logoutRequestSigned': False,
                'logoutResponseSigned': False,
                'metadataCacheDuration': None,
                'metadataValidUntil': None,
                'nameIdEncrypted': False,
                'requestedAuthnContext': False,
                'requestedAuthnContextComparison': 'exact',
                'signMetadata': False,
                'signatureAlgorithm':
                    'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
                'wantAssertionsEncrypted': False,
                'wantAssertionsSigned': False,
                'wantAttributeStatement': False,
                'wantMessagesSigned': False,
                'wantNameId': True,
                'wantNameIdEncrypted': False,
                'digestAlgorithm':
                    'http://www.w3.org/2001/04/xmlenc#sha256'
            },

        },
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
    # onelogin
    'onelogin': {
        'settings': {
            'debug': True,
            'idp': {
                'entityId': 'https://app.onelogin.com/saml/metadata/01661574-91ed-4735-a3b9-f4ddebb2cbb8',
                'singleLogoutService': {
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
                    'url': 'https://tugraz-dev.onelogin.com/trust/saml2/http-redirect/slo/1070112'
                },

                'singleSignOnService': {
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
                    'url': 'https://tugraz-dev.onelogin.com/trust/saml2/http-post/sso/01661574-91ed-4735-a3b9-f4ddebb2cbb8'
                },

                'x509cert': 'MIID2DCCAsCgAwIBAgIUWRGl84DFd+GbLYt0BmwyI+FCKVIwDQYJKoZIhvcNAQEFBQAwRDEPMA0GA1UECgwGVFVHUkFaMRUwEwYDVQQLDAxPbmVMb2dpbiBJZFAxGjAYBgNVBAMMEU9uZUxvZ2luIEFjY291bnQgMB4XDTIwMDEyODEwNDI1M1oXDTI1MDEyODEwNDI1M1owRDEPMA0GA1UECgwGVFVHUkFaMRUwEwYDVQQLDAxPbmVMb2dpbiBJZFAxGjAYBgNVBAMMEU9uZUxvZ2luIEFjY291bnQgMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAve5a++I/VHC22fMk5v8GwCvdIyiziOwGjq0XXyjTg9TyhHJZbfDXa7S0NjK7dK4+d3iaB3MvCpnr+7H2J2Cohracgy2BQz9Z4BqsjDat016zkAPoID9R6osliqocw1jESnyL59OJWftAiA4rFmQs6v/b56vgre8EP6qKbykq6mWvepGyBbfjRsYbFoIDmnW8kJoZtLMDQfTBvEF2veHDt9EbsWP+hyedMYTWCfsbTHhFKNrhRKr3m3k+w6Zsca2zp3A8xiFv0fcl6PglEwEZz2Iwb0ySifaf4ZLDVjSekpCLf29doBJYUeE5TUP8oHfATOcWW+m5D3MXVcMUax+AFwIDAQABo4HBMIG+MAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFK4GHoSfnMQKb8RjP2HrGzJ4ICiDMH8GA1UdIwR4MHaAFK4GHoSfnMQKb8RjP2HrGzJ4ICiDoUikRjBEMQ8wDQYDVQQKDAZUVUdSQVoxFTATBgNVBAsMDE9uZUxvZ2luIElkUDEaMBgGA1UEAwwRT25lTG9naW4gQWNjb3VudCCCFFkRpfOAxXfhmy2LdAZsMiPhQilSMA4GA1UdDwEB/wQEAwIHgDANBgkqhkiG9w0BAQUFAAOCAQEAUg7UHFju0QA7ubcSLBuvEMUQL9jxtzDi0ndSi8qqtLJSjBalcfll0X/gI+sAMGMd0MW7P3abOVVfGBSlZN01KCPC2WHKRwzyO3sOCatkPrn2SYthQWHD/W7psyFgoDt5lQNijLyZdpvZbRIotxcWpoaTcBzaArd/0MNe1VaGlLK5GeqtbwL+dQD+O3mtSUfF918qeiOHEwI7nfPo7vjUyRT8Ov1loqP5+A0/R1CyL0Dh/tVdIkOHx6EjrIXsb/K6xXPknYZqPApPkZq514ZCEPhAILFU+5R/cQMZMZEacCdKuQ9XMkR8bqnh8xu620SCYiSVPXtVW4bpXKs0nJazBQ=='
            },

            'sp': {

                'privateKey': 'MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIHxNp8P2PsV8CAggAMBQGCCqGSIb3DQMHBAjOyik6fsEC3gSCAoC4tFsYAl4GexyXESiRKpOQzHQNFtQtwDEevT1IKgsafSNjOMJZLKrnoejNoxEQUPPPXgGEd83Fmp2cSHm+YVksH06zcsA+RKf5ab6t0bsgcyljGzkHEDQtMRPcaXNlVMbU9VEDOX26MgmlU/pd+GGfE99IbEFc6qN1e7qOnmKSw93Q3o05ubO3wEI76JhOioGGXB3pEn8f4XLDwck0thzYD6H2vdF+kyIdM8w1BgyLdeP0aDkfG1V3rLGhE8246rwVUzRSZv6BCNBZFk7YO1d7j0+BDxnbHFS631zdCgMcd/XS8u6acc3IYr/bQLH4a1y0X3Z+8ks8arEgUtXqYx9wMlp5lajlsr9JDIU5OnuZ2XY+4sqDQsTZPjBpxK8oMjvJNNatnTf+18htkTdovpInlP7xpEjp1L7H74iKY25UsAZ9e+gqHZwILnk418mQ1E4JYU6JRUZspJSFfqwn9FL6DnvhzPIhtzwhr3eL4f4RXWxxe2xCzvWg+GaWuMfZdj77SV4pMOi7vb3HlYY6luShVlYKdSaw+jf6XVy4ZMTWT5wcE1mc3tAJqF18Mi8amOetpZhz16ISOKnO0rKrfmxteNPQn2AB8QquGGn050PTW4m8zFXDBiyg2xvcRLAW/8ych3k+pkEZi4tVCkLcHM56J/XUEKMCxiSok+vbzxfVf1D2vYFFS7Lw1nP5RnLKFdn8XdHQ+lu2diod18wYBQP4eoU+XjjP2zjlpULiWHt7PpCERqGg7H2Z2amIL5rTeqQuyXczw1/xG/VBNn9qe3DXFodvoV6OZb3efNT/eJgOyaPLi2FmB7Kpdp4JIdJgLnaBCwNBXkpGSwb732O/cug8',

                'x509cert': 'MIICjjCCAfegAwIBAgIBADANBgkqhkiG9w0BAQ0FADBkMQswCQYDVQQGEwJhdDENMAsGA1UECAwER3JhejEPMA0GA1UECgwGVFVHUkFaMRAwDgYDVQQDDAdpbnZlbmlvMSMwIQYJKoZIhvcNAQkBFhRtb2ppYi53YWxpQHR1Z3Jhei5hdDAeFw0yMDAxMTAyMDIwMTlaFw0yMTAxMDkyMDIwMTlaMGQxCzAJBgNVBAYTAmF0MQ0wCwYDVQQIDARHcmF6MQ8wDQYDVQQKDAZUVUdSQVoxEDAOBgNVBAMMB2ludmVuaW8xIzAhBgkqhkiG9w0BCQEWFG1vamliLndhbGlAdHVncmF6LmF0MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5ZrPhRhyDyLTe93rpgqN9MMfnCsg+2QBW4EOuQnMXJzF1dqrFEsexot1FRW83IjqbY+680PmGABQtxUpS4Kinr/pLYbPhQ2WPQRad7mtOn/dD40VVwfG0GfcLrnKe5F4QLfNjervjl8jH/AKPCYwwfSeuw1LNoRjy1uDwkp9cRQIDAQABo1AwTjAdBgNVHQ4EFgQUPv2+wS1RuagCOed7w1FzouBmpP4wHwYDVR0jBBgwFoAUPv2+wS1RuagCOed7w1FzouBmpP4wDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQ0FAAOBgQA4qvU7gbgE/MoljUW68qMPs8z8Q2Ngttp6F1KOMNO9rgrYWAJh4u6BMt11mlBgBlLLJzG67wXpBr0l78IcOXun4w955te0VRp7aZ0b1uOPt0aUoDOXuBAhZURLZfbsogpWiE6bdB8N0nHTwk2WG2PPIC5Z99UdDivcP5ZeSPAkUw=='

            },
            'security': {
                'authnRequestsSigned': False,
                'failOnAuthnContextMismatch': False,
                'logoutRequestSigned': False,
                'logoutResponseSigned': False,
                'metadataCacheDuration': None,
                'metadataValidUntil': None,
                'nameIdEncrypted': False,
                'requestedAuthnContext': False,
                'requestedAuthnContextComparison': 'exact',
                'signMetadata': False,
                'signatureAlgorithm':
                    'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
                'wantAssertionsEncrypted': False,
                'wantAssertionsSigned': False,
                'wantAttributeStatement': False,
                'wantMessagesSigned': False,
                'wantNameId': True,
                'wantNameIdEncrypted': False,
                'digestAlgorithm':
                    'http://www.w3.org/2001/04/xmlenc#sha256'
            },

        },

        # mappings
        "mappings": {

            # invenio  #origin
            "email": "email",
            "username": "username",
            "full_name": "full_name",
            "external_id": "external_id"
        },

        # remove this line
         'acs_handler': acs_handler_factory('onelogin'),

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
