# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom TU Graz datastreams."""

from typing import Any

from flask import current_app
from invenio_vocabularies.contrib.funders.datastreams import FundersRORTransformer
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.errors import TransformerError


class TuGrazRORTransformer(FundersRORTransformer):
    """Custom TU Graz ROR Datastream transformer."""

    def apply(
        self,
        stream_entry: StreamEntry,
        **kwargs: Any,  # noqa: ANN401
    ) -> StreamEntry:
        """Apply the transformation to the stream entry.

        Apply the default transformation then filter based on TU Graz repository
        requirements. Current requirements:
        - funder must be an Austrian funder
        - funder must be an EU funder
        """
        stream_entry = super().apply(stream_entry, **kwargs)
        ror = stream_entry.entry

        if not (
            ror["country"] == "AT"
            or ror["country_name"] == "Austria"
            or any(
                funder_partial_name in ror["name"].lower()
                for funder_partial_name in current_app.config.get(
                    "CONFIG_TUGRAZ_ROR_FUNDERS_NAME_CONTAINS",
                )
            )
        ):
            msg = "ROR Entry not needed for TU Graz Repository."
            raise TransformerError(msg)

        return stream_entry
