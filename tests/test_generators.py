# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test Generators."""

from invenio_config_tugraz.generators import RecordIp


def test_recordip():
    """Test Generator RecordIp."""
    generator = RecordIp()

    assert generator.needs() == []
    assert generator.excludes() == []
    assert generator.query_filter().to_dict() == {"match_all": {}}
