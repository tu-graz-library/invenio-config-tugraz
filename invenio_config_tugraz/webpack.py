# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""JS/CSS Webpack bundles for invenio-config-tugraz."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "invenio-config-tugraz-unlock": "./js/invenio_config_tugraz/unlock.js",
                "invenio-config-tugraz-contact": "./js/invenio_config_tugraz/contact.js",
                # notices bundle name; extract to invenio-notices later
                "invenio-config-tugraz-notices": "./js/invenio_config_tugraz/notices.js",
            },
            "dependencies": {
                "jquery": "^3.2.1",
                "react": "^16.13.0",
                "react-dom": "^16.13.0",
                "react-invenio-forms": "^4.11.0",
            },
        },
    },
)
