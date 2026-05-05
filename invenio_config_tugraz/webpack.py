# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
            },
            "dependencies": {
                "jquery": "^3.2.1",
            },
        },
    },
)
