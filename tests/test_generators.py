# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test Generators."""

from invenio_access.permissions import any_user

from invenio_config_tugraz.generators import RecordIp


def test_recordip(create_app, open_record, singleip_record):
    """Test Generator RecordIp."""
    generator = RecordIp()
    open_record = open_record
    singleiprec = singleip_record

    assert generator.needs(record=None) == []
    assert generator.needs(record=open_record) == [any_user]
    assert generator.needs(record=singleiprec) == []

    assert generator.excludes(record=open_record) == []
    assert generator.excludes(record=open_record) == []

    assert generator.query_filter().to_dict() == {'bool': {'must_not': [{'match': {'access.access_right': 'singleip'}}]}}
