# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Override specific OAI-PMH functions & configs for TUGRAZ usecase.

    In order to expose all records present in the repository to the OAI-Server,
we make use of the global-search data model and "redirect" the fetched record
to its corresponding serializer, which should be located in the respective data
model package (rdm-records, lom, marc21).
    This approach leads to the need of overriding most of the OAISERVER_ configurations
in invenio.cfg with the functions and classes defined in this file.

Example invenio.cfg:

OAISERVER_METADATA_FORMATS = {
    "oai_dc": {
        "serializer": "invenio_config_tugraz.oai:gs_oai_dc_etree",
        "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    },
    'lom':{
        'serializer': 'invenio_config_tugraz.oai:gs_lom_etree',
        'schema':'https://w3id.org/oerbase/profiles/lomuibk/latest/lom-uibk.xsd',
        'namespace': 'https://w3id.org/oerbase/profiles/lomuibk/latest/'
    },
    "marc21": {
        "serializer": "invenio_config_tugraz.oai:gs_marc21_etree",
        "schema": "https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd",
        "namespace": "https://www.loc.gov/standards/marcxml/",
    },
}

OAISERVER_GETRECORD_FETCHER = "invenio_config_tugraz.oai:getrecord_fetcher"
OAISERVER_RECORD_INDEX='global-search-records-record-v1.0.0'
OAISERVER_ID_FETCHER="invenio_config_tugraz.oai:oaiid_fetcher"

from invenio_config_tugraz.oai import TUGRAZOAIRecordSearch
OAISERVER_SEARCH_CLS=TUGRAZOAIRecordSearch
"""

from flask import current_app
from invenio_db import db
from invenio_pidstore.errors import PersistentIdentifierError
from invenio_pidstore.fetchers import FetchedPID
from invenio_pidstore.models import PersistentIdentifier
from invenio_rdm_records.oai import dublincore_etree
from invenio_rdm_records.oai import getrecord_fetcher as rdm_getrecord_fetcher
from invenio_rdm_records.records.api import RDMRecord
from invenio_rdm_records.services.pids.providers.oai import OAIPIDProvider
from invenio_records_lom.oai import getrecord_fetcher as lom_getrecord_fetcher
from invenio_records_lom.oai import lom_dc_etree, lom_etree
from invenio_records_lom.records.api import LOMRecord
from invenio_records_marc21.oai import getrecord_fetcher as marc21_getrecord_fetcher
from invenio_records_marc21.oai import marc21_dc_etree, marc21_etree
from invenio_records_marc21.records.api import Marc21Record
from invenio_search import RecordsSearch, current_search_client
from invenio_search.engine import dsl


def getrecord_fetcher(record_uuid: str) -> str:
    """OAISERVER_GETRECORD_FETCHER override.

    Redirect the record_uuid to its specific data model record fetcher.
    """
    pids = (
        db.session.query(PersistentIdentifier)
        .filter_by(object_uuid=record_uuid, object_type="rec")
        .all()
    )
    for pid in pids:
        if pid.pid_type == "recid":
            return rdm_getrecord_fetcher(record_uuid)
        if pid.pid_type == "lomid":
            return lom_getrecord_fetcher(record_uuid)
        if pid.pid_type == "marcid":
            return marc21_getrecord_fetcher(record_uuid)
    msg = "Unknown PID"
    raise PersistentIdentifierError(msg)


def gs_lom_etree(
    pid: str,
    record: dict,
) -> dict:
    """GS-to-LOM adapter for lom metadata format."""
    if "original" not in record["_source"]:
        return lom_etree(pid, record)

    original = record["_source"]["original"]
    pid_value = original["pid"]
    lom_record_idx_view = current_search_client.search(
        index=f"{LOMRecord.index._name}",  # noqa: SLF001
        body={"query": {"term": {"id": pid_value}}},
    )
    hits = lom_record_idx_view["hits"]["hits"]
    if len(hits) > 0:
        return lom_etree(pid, hits[0])
    return lom_etree(pid, record)


def gs_marc21_etree(
    pid: str,
    record: dict,
) -> dict:
    """GS-to-MARC21 adapter for marc21 metadata format."""
    if "original" not in record["_source"]:
        return marc21_etree(pid, record)

    original = record["_source"]["original"]
    pid_value = original["pid"]
    marc21_record_idx_view = current_search_client.search(
        index=f"{Marc21Record.index._name}",  # noqa: SLF001
        body={"query": {"term": {"id": pid_value}}},
    )
    hits = marc21_record_idx_view["hits"]["hits"]
    if len(hits) > 0:
        return marc21_etree(pid, hits[0])
    return marc21_etree(pid, record)


def gs_oai_dc_etree(
    pid: str,
    record: dict,
) -> dict:
    """GS-to-OAI_DC adapter for oai_dc metadata format.

    From the fetched global-search record, search the original record
    and direct it to its dublincore serializer.

    Because this method is intended to be placed as the serializer of
    oai_dc metadata format, it will be called also for GetRecord. Therefore
    in that case the record is the "original" from the start, there is
    no need for an extra query, just redirect to the existing dc serializers
    based on the PID Type.

    TODO: instead of an extra search query, consider adding the whole
        record in the "original" field of the gs-schema.
    """
    if "original" not in record["_source"]:
        # record not coming from global-search
        pid = (
            db.session.query(PersistentIdentifier)
            .filter_by(pid_value=record["_source"]["id"], object_type="rec")
            .first()
        )
        if pid.pid_type == "lomid":
            return lom_dc_etree(pid, record)
        if pid.pid_type == "marcid":
            return marc21_dc_etree(pid, record)

        return dublincore_etree(pid, record)

    original = record["_source"]["original"]
    pid_value = original["pid"]

    match original["schema"]:
        case "marc21":
            marc21_record_idx_view = current_search_client.search(
                index=f"{Marc21Record.index._name}",  # noqa: SLF001
                body={"query": {"term": {"id": pid_value}}},
            )
            hits = marc21_record_idx_view["hits"]["hits"]
            return marc21_dc_etree(pid, hits[0])

        case "rdm":
            rdm_record_idx_view = current_search_client.search(
                index=f"{RDMRecord.index._name}",  # noqa: SLF001
                body={"query": {"term": {"id": pid_value}}},
            )
            hits = rdm_record_idx_view["hits"]["hits"]
            return dublincore_etree(pid, hits[0])

        case "lom":
            lom_record_idx_view = current_search_client.search(
                index=f"{LOMRecord.index._name}",  # noqa: SLF001
                body={"query": {"term": {"id": pid_value}}},
            )
            hits = lom_record_idx_view["hits"]["hits"]
            return lom_dc_etree(pid, hits[0])


def generate_id(pid_value: str) -> str:
    """Copy-paste the ID generation from https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/pids/providers/oai.py.

    Used to add it to the global-search original PID which does not have the OAI-ID.

    TODO: maybe this "trick" won't be needed once "original" contains the complete record
    """
    prefix = current_app.config.get("OAISERVER_ID_PREFIX", "")
    return f"oai:{prefix}:{pid_value}"


def oaiid_fetcher(record_uuid: str, data: dict) -> FetchedPID:  # noqa: ARG001
    """OAISERVER_OAIID_FETCHER override based on global search schema.

    "Original" PID updated with generated OAI-ID.
    """
    pid_value = data.get("original", {}).get("pid")

    if pid_value is None:
        raise PersistentIdentifierError

    oai_pid = generate_id(pid_value)
    return FetchedPID(
        provider=OAIPIDProvider,
        pid_type="oai",
        pid_value=oai_pid,
    )


class TUGRAZOAIRecordSearch(RecordsSearch):
    """
    OAISERVER_SEARCH_CLS override.

    Override default_filter to match global-search schema.
    """

    class Meta:
        """Configuration for OAI server search."""

        default_filter = [
            dsl.Q("exists", field="original.pid"),
        ]
