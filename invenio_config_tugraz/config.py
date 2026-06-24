# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from invenio_app_rdm.config import (
    CELERY_BEAT_SCHEDULE,
    STATS_AGGREGATIONS,
    STATS_EVENTS,
    STATS_QUERIES,
)
from invenio_global_search.oai import OAIGlobalSearch
from invenio_i18n import gettext as _
from invenio_records_lom.config import (
    LOM_STATS_AGGREGATIONS,
    LOM_STATS_CELERY_TASKS,
    LOM_STATS_EVENTS,
    LOM_STATS_QUERIES,
)
from invenio_records_marc21.config import (
    MARC21_STATS_AGGREGATIONS,
    MARC21_STATS_CELERY_TASKS,
    MARC21_STATS_EVENTS,
    MARC21_STATS_QUERIES,
)

from .facets import TUGRAZ_REQUESTS_FACETS
from .notifications import TUGRAZ_NOTIFICATIONS_BUILDERS
from .permissions import (
    TUGrazRDMRecordPermissionPolicy,
    TUGrazRDMRequestsPermissionPolicy,
)
from .requests import TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES
from .requests.events import TUGRAZ_REQUESTS_EVENTS_SERVICE_COMPONENTS

# Config-Tugraz
# =============

CONFIG_TUGRAZ_IP_NETWORK = ""
"""Allows access to users who are in the IP network."""

CONFIG_TUGRAZ_IP_RANGES = []
"""Allows access to users whose range of IP address is listed.

INVENIO_CONFIG_TUGRAZ_IP_RANGES =
[["127.0.0.2", "127.0.0.99"], ["127.0.1.3", "127.0.1.5"]]
"""

CONFIG_TUGRAZ_ROUTES = {
    "guide": "/guide",
    "terms": "/terms",
    "gdpr": "/gdpr",
    "accessibility": "/accessibility",
    "file-formats": "/file-formats",
    "curations": "/curations",
}
"""Defined routes for TUG."""

CONFIG_TUGRAZ_SHIBBOLETH = False
"""Set True if SAML is configured"""

CONFIG_TUGRAZ_SINGLE_IPS = []
"""Allows access to users whose IP address is listed.

INVENIO_CONFIG_TUGRAZ_SINGLE_IPS =
    ["127.0.0.1", "127.0.0.2"]
"""

# Invenio-App
# ===========
# See https://invenio-app.readthedocs.io/en/latest/configuration.html

APP_DEFAULT_SECURE_HEADERS = {
    "content_security_policy": {
        "default-src": [
            "'self'",
            "data:",
            "'unsafe-inline'",
            "blob:",
            "ub-support.tugraz.at",  # zammad contact form
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

# Invenio-I18N
# ============
# See https://invenio-i18n.readthedocs.io/en/latest/configuration.html

BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "Europe/Vienna"
I18N_LANGUAGES = [("de", _("German"))]

# Invenio-Mail
# ============
# See https://invenio-mail.readthedocs.io/en/latest/configuration.html

SECURITY_EMAIL_SENDER = "info@invenio-test.tugraz.at"
SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to TU Graz Repository!")

# Invenio-Userprofiles
# ====================
# See https://invenio-userprofiles.readthedocs.io/en/latest/configuration.html

USERPROFILES_EMAIL_ENABLED = True
USERPROFILES_EXTEND_SECURITY_FORMS = True
USERPROFILES_READ_ONLY = True

# Invenio-SAML
# ============
# See https://invenio-saml.readthedocs.io/en/latest/configuration.html

SSO_SAML_DEFAULT_ACS_ROUTE = "/authorized/<idp>"
SSO_SAML_DEFAULT_BLUEPRINT_PREFIX = "/shibboleth"
SSO_SAML_DEFAULT_METADATA_ROUTE = "/metadata/<idp>"
SSO_SAML_DEFAULT_SLO_ROUTE = "/slo/<idp>"
SSO_SAML_DEFAULT_SLS_ROUTE = "/sls/<idp>"
SSO_SAML_DEFAULT_SSO_ROUTE = "/login/<idp>"
SSO_SAML_IDPS = {}

# Invenio-Accounts
# ================
# See https://invenio-accounts.readthedocs.io/en/latest/configuration.html

ACCOUNTS_LOCAL_LOGIN_ENABLED = True
RECAPTCHA_PRIVATE_KEY = None
RECAPTCHA_PUBLIC_KEY = None
SECURITY_CHANGEABLE = False
SECURITY_CONFIRMABLE = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
SECURITY_PASSWORD_SINGLE_HASH = ["pbkdf2_sha512"]

# Invenio-RDM-Records
# ===================
# See https://invenio-rdm-records.readthedocs.io/en/latest/configuration.html

APP_RDM_DEPOSIT_FORM_AUTOCOMPLETE_NAMES = "off"
APP_RDM_DEPOSIT_FORM_DEFAULTS = {
    "publisher": "Graz University of Technology",
}
APP_RDM_DEPOSIT_FORM_QUOTA = {
    "maxFiles": 100,
    "maxStorage": 10**9 * 10,
}
APP_RDM_SUBCOMMUNITIES_LABEL = "Projects"
DATACITE_DATACENTER_SYMBOL = ""
DATACITE_FORMAT = "{prefix}/{id}"
RDM_RECORDS_USER_FIXTURE_PASSWORDS = {"info@tugraz.at": None}

# SQLAlchemy
# ==========

SQLALCHEMY_ECHO = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": False,
    "pool_recycle": 3600,
    "pool_timeout": 10,
}

# Redis (cache)
# =============

RATELIMIT_AUTHENTICATED_USER = "25000 per hour;1000 per minute"
RATELIMIT_GUEST_USER = "5000 per hour;500 per minute"
SESSION_COOKIE_SAMESITE = "Strict"

# OAI-PMH
# =======
# See https://github.com/inveniosoftware/invenio-oaiserver

OAISERVER_ADMIN_EMAILS = [
    "oai@repository.tugraz.at",
]
# Same prefix on every instance; ideally per-environment (e.g. test should
# advertise invenio-test.tugraz.at). Override per env via
# INVENIO_OAISERVER_ID_PREFIX or per-env invenio.cfg.
OAISERVER_ID_PREFIX = "repository.tugraz.at"

# Invenio-Curations
# =================
# See https://github.com/tu-graz-library/invenio-curations

CURATIONS_ENABLE_REQUEST_COMMENTS = True
CURATIONS_PRIVILEGED_ROLES = ["administration", "bypass-curation"]

# Invenio-Override
# ================
# See https://github.com/tu-graz-library/invenio-override

OVERRIDE_CONTACT_FORM = True
OVERRIDE_CONTACT_FORM_BUNDLE = "invenio-config-tugraz-contact.js"
OVERRIDE_DOC_REDIRECTS = {
    "/guide": "https://doi.org/10.3217/dgpcz-td505",
    "/terms": "https://doi.org/10.3217/k3dsw-rv326",
    "/gdpr": "https://doi.org/10.3217/xream-wzp39",
    "/accessibility": "https://doi.org/10.3217/psmeb-84429",
    "/file-formats": "https://doi.org/10.3217/3c0k5-zqh95",
    "/curations": "https://doi.org/10.3217/h1zfa-4fb59",
}
OVERRIDE_FAVICON = "tug.ico"
OVERRIDE_FOOTER_BACKGROUND = "#4a4a4a"
OVERRIDE_FOOTER_DIVIDER_COLOR = "rgba(255,255,255,0.1)"
OVERRIDE_FOOTER_FG_COLOR = "#ffffff"
OVERRIDE_FOOTER_LINKS = {
    "Repository": [
        {
            "label": "Documentation",
            "url": "https://tu-graz-library.github.io/docs-repository",
            "external": True,
        },
        {"label": "Reference Guide", "url": "/guide", "external": True},
        {"label": "Search Guide", "url": "/help/search"},
        {"label": "Data Protection", "url": "/gdpr", "external": True},
        {"label": "Terms and Conditions", "url": "/terms", "external": True},
        {"label": "Accessibility Statement", "url": "/accessibility", "external": True},
        {
            "label": "List of preferred file formats",
            "url": "/file-formats",
            "external": True,
        },
        {"label": "Curation Workflow", "url": "/curations", "external": True},
    ],
    "Features": [
        {"label": "Scalability"},
        {"label": "Institutional integration"},
        {"label": "Next Generation Repository"},
        {"label": "Repository Profiles"},
        {"label": "Resilient"},
    ],
    "Connected Services": [
        {"label": "PURE", "url": "https://pure.tugraz.at", "external": True},
        {
            "label": "CampusOnline",
            "url": "http://campusonline.tugraz.at",
            "external": True,
        },
        {
            "label": "Research Data Management",
            "url": "https://rdm.tugraz.at",
            "external": True,
        },
    ],
    "Accessibility": [
        {"label": "Tipp:"},
        {"label": "Use Ctrl + and Ctrl -"},
        {"label": "to change the font size."},
    ],
}
OVERRIDE_FOOTER_LOGO_FILTER = "brightness(0) invert(1)"
OVERRIDE_FRONTPAGE_FEATURES = [
    {"icon": "check circle", "text": "FAIR Data"},
    {"icon": "quote left", "text": "Citable with DOI"},
    {"icon": "lock open", "text": "Open Access"},
    {"icon": "shield alternate", "text": "Long-term Preservation"},
]
OVERRIDE_FRONTPAGE_RIGHT = False
OVERRIDE_FRONTPAGE_SHOW_RECENT_UPLOADS = True
OVERRIDE_FRONTPAGE_SUBTITLE = (
    "Publish and share your research data — citable, visible, and FAIR."
)
OVERRIDE_HEADER_CLAIM_WORDS = ["SCIENCE", "TECHNOLOGY", "PASSION"]
OVERRIDE_HEADER_LOGO_LEFT = "images/library_logo.png"
OVERRIDE_HEADER_LOGO_LINK = "https://www.tugraz.at"
OVERRIDE_HEADER_LOGO_SVG = "images/tu_graz_logo.svg"
OVERRIDE_HEADER_TEXT_LINE1 = "TU GRAZ"
OVERRIDE_HEADER_TEXT_LINE2 = "REPOSITORY"
OVERRIDE_HEADER_TEXT_LINE3 = "LIBRARY & ARCHIVES"
OVERRIDE_ICON = "images/icon_use.png"
OVERRIDE_LOGO = "images/TUG.png"
OVERRIDE_INSTANCE_TYPE = "production"
OVERRIDE_PRODUCTION = True
OVERRIDE_REASONS_BG = None
OVERRIDE_REASONS_PARTNER = "TU Graz & CERN"
OVERRIDE_RESOURCE_OVERVIEW = False
OVERRIDE_SHIBBOLETH = False
OVERRIDE_SHOW_CONTACT = True
OVERRIDE_SHOW_EDUCATIONAL_RESOURCES = True
OVERRIDE_SHOW_EDUCATIONAL_RESOURCES_CARD = True
OVERRIDE_SHOW_PUBLICATIONS_CARD = True
OVERRIDE_SHOW_PUBLICATIONS_SEARCH = True
OVERRIDE_SHOW_RDM_SEARCH = True
THEME_FOOTER_TEMPLATE = "invenio_override/footer.html"
THEME_FRONTPAGE_TITLE = "TUGraz Repository"
THEME_SITENAME = "TU Graz Repository"

# Invenio-App-RDM
# ===============
# See https://github.com/inveniosoftware/invenio-app-rdm

AUDIT_LOGS_ENABLED = True
COMMUNITIES_ADMINISTRATION_DISABLED = False
COMMUNITIES_SHOW_BROWSE_MENU_ENTRY = True
JOBS_ADMINISTRATION_ENABLED = True
RDM_SEARCH_SORT_BY_VERIFIED = True
RDM_USER_MODERATION_ENABLED = True
THEME_SHOW_FRONTPAGE_INTRO_SECTION = False
USERS_RESOURCES_ADMINISTRATION_ENABLED = True

# Invenio-Global-Search
# =====================
# See https://github.com/tu-graz-library/invenio-global-search

GLOBAL_SEARCH_ORIGINAL_SCHEMAS = {
    "lom": {
        "schema": "lom",
        "name_l10n": _("OER"),
    },
    "rdm": {
        "schema": "rdm",
        "name_l10n": _("Research Result"),
    },
    "marc21": {
        "schema": "marc21",
        "name_l10n": _("Publication"),
    },
}
GLOBAL_SEARCH_SCHEMAS = {
    "rdm": {
        "schema": "rdm",
        "name_l10n": "Research Result",
    },
    "marc21": {
        "schema": "marc21",
        "name_l10n": "Publication",
    },
    "lom": {
        "schema": "lom",
        "name_l10n": "OER",
    },
}

# Invenio-Records-Marc21
# ======================
# See https://github.com/tu-graz-library/invenio-records-marc21

MARC21_DATACITE_DEFAULT_PUBLISHER = "Graz University of Technology"
MARC21_RECORD_LANDING_PAGE_TEMPLATE = (
    "invenio_catalogue_marc21/landing_page/record.html"
)
MARC21_SEARCH_NAV_TEMPLATE = "invenio_override/search_nav.html"
LOM_SEARCH_NAV_TEMPLATE = "invenio_override/search_nav.html"
GLOBAL_SEARCH_NAV_TEMPLATE = "invenio_override/search_nav.html"
MARC21_UPLOADS_TEMPLATE = "invenio_override/datamodels/marc21_uploads.html"
LOM_UPLOADS_TEMPLATE = "invenio_override/datamodels/lom_uploads.html"

# Invenio-Curations — permissions and requests
# =============================================
# See https://github.com/tu-graz-library/invenio-curations

NOTIFICATIONS_BUILDERS = TUGRAZ_NOTIFICATIONS_BUILDERS
RDM_PERMISSION_POLICY = TUGrazRDMRecordPermissionPolicy
REQUESTS_EVENTS_SERVICE_COMPONENTS = TUGRAZ_REQUESTS_EVENTS_SERVICE_COMPONENTS
REQUESTS_FACETS = TUGRAZ_REQUESTS_FACETS
REQUESTS_PERMISSION_POLICY = TUGrazRDMRequestsPermissionPolicy
REQUESTS_REGISTERED_EVENT_TYPES = TUGRAZ_REQUESTS_REGISTERED_EVENT_TYPES

# Stats — LOM and Marc21
# ======================

CELERY_BEAT_SCHEDULE.update(LOM_STATS_CELERY_TASKS)
CELERY_BEAT_SCHEDULE.update(MARC21_STATS_CELERY_TASKS)

STATS_AGGREGATIONS.update(LOM_STATS_AGGREGATIONS)
STATS_AGGREGATIONS.update(MARC21_STATS_AGGREGATIONS)

STATS_EVENTS.update(LOM_STATS_EVENTS)
STATS_EVENTS.update(MARC21_STATS_EVENTS)

STATS_QUERIES.update(LOM_STATS_QUERIES)
STATS_QUERIES.update(MARC21_STATS_QUERIES)

CONFIG_TUGRAZ_OAUTH_USERNAME_ATTRIBUTE = ""
"""Set this config to choose a custom attribute from the OAuth provider token for the username."""

CONFIG_TUGRAZ_OAUTH_EXTERNAL_ID_ATTRIBUTE = ""
"""Set this config to choose a custom attribute from the OAuth provider token for the external id."""

CONFIG_TUGRAZ_OAUTH_USERNAME_PREFIX = "idp"
"""Prefix the username with this value if CONFIG_TUGRAZ_OAUTH_USERNAME_ATTRIBUTE is set."""

OAISERVER_METADATA_FORMATS = {
    "oai_dc": {
        "serializer": "invenio_global_search.oai:gs_oai_dc_etree",
        "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    },
    "lom": {
        "serializer": "invenio_global_search.oai:gs_lom_etree",
        "schema": "https://w3id.org/oerbase/profiles/lomuibk/latest/lom-uibk.xsd",
        "namespace": "https://w3id.org/oerbase/profiles/lomuibk/latest/",
    },
    "marc21": {
        "serializer": "invenio_global_search.oai:gs_marc21_etree",
        "schema": "https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd",
        "namespace": "https://www.loc.gov/standards/marcxml/",
    },
}
"""TU Graz supported OAI metadata formats with their serializer, schema and namespace."""

OAISERVER_GETRECORD_FETCHER = "invenio_global_search.oai:getrecord_fetcher"
"""Record fetcher based on global-search for OAI serialization."""

OAISERVER_RECORD_SETS_FETCHER = "invenio_global_search.oai:getrecord_sets_fetcher"
"""Record sets fetcher based on global-search for OAI serialization."""

OAISERVER_RECORD_INDEX = "global-search-records-record-v1.0.0"
"""Configured index to retrieve the records for OAI functions like ListRecords."""

OAISERVER_ID_FETCHER = "invenio_global_search.oai:oaiid_fetcher"
"""TU Graz custom OAI ID fetcher."""

OAISERVER_SEARCH_CLS = OAIGlobalSearch
"""TU Graz custom search class for OAI records retrieval based on global-search."""
