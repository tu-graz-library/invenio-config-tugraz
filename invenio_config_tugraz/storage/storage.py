# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom storage for TUGraz needs."""

import mimetypes
from typing import Any

from flask import current_app, make_response, Response
from invenio_files_rest.helpers import sanitize_mimetype
from invenio_files_rest.storage import PyFSFileStorage


class TUGrazStorage(PyFSFileStorage):
    """Overrides the class from invenio_files_rest with custom logic for TUGraz needs."""

    def send_file(self, filename: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send file custom implementation.

        Build a redirect response for the nginx container so that it will
        directly serve the requested file and free up the flask workers.

        FILES_REST_XSENDFILE_ENABLED has to be enabled for this to work, otherwise
        flask will download the files.
        """
        if current_app.config["FILES_REST_XSENDFILE_ENABLED"]:
            response = make_response()
            redirect_url_base = current_app.config["CONFIG_TUGRAZ_NGINX_URL_BASE"]
            storage_root = current_app.config["CONFIG_TUGRAZ_STORAGE_ROOT"]

            redirect_url_key = self.fileurl.removeprefix(storage_root)

            response.headers["X-Accel-Redirect"] = (
                f"{redirect_url_base}{redirect_url_key}"
            )
            response.headers["X-Accel-Buffering"] = "yes"
            response.headers["X-Accel-Limit-Rate"] = "off"

            mimetype = mimetypes.guess_type(filename)[0]
            if mimetype is not None:
                mimetype = sanitize_mimetype(mimetype, filename=filename)

            if mimetype is None:
                mimetype = "application/octet-stream"

            response.mimetype = mimetype

            # make the browser use the file download dialogue for the file
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )

            # set some security-related headers for the download
            response.headers["Content-Security-Policy"] = "default-src 'none';"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Download-Options"] = "noopen"
            response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
            response.headers["X-Frame-Options"] = "deny"
            response.headers["X-XSS-Protection"] = "1; mode=block"

            return response
        return super().send_file(filename, **kwargs)
