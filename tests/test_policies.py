# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tests for permissions-policy."""

from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy

from invenio_config_tugraz.permissions.policies import TUGrazRDMRecordPermissionPolicy

ALLOWED_DIFFERENCES = {
    "can_authenticated",
    "can_create",
    "can_search_drafts",
    "can_tugraz_authenticated",
}


def test_policies_synced():
    """Make sure our permission-policy stays synced with invenio's."""
    tugraz_cans = {
        name: getattr(TUGrazRDMRecordPermissionPolicy, name)
        for name in dir(TUGrazRDMRecordPermissionPolicy)
        if name.startswith("can_")
    }
    rdm_cans = {
        name: getattr(RDMRecordPermissionPolicy, name)
        for name in dir(RDMRecordPermissionPolicy)
        if name.startswith("can_")
    }

    # check whether same set of `can_<action>`s`
    if extras := set(tugraz_cans) - set(rdm_cans) - ALLOWED_DIFFERENCES:
        raise KeyError(
            f"TU Graz's permission-policy has additional fields over invenio-rdm's:{extras}\n"
            "if this is intentional, add to ALLOWED_DIFFERENCES in test-file\n"
            "otherwise remove extraneous fields from TUGrazRDMRecordPermissionPolicy"
        )
    if missing := set(rdm_cans) - set(tugraz_cans):
        raise KeyError(
            f"invenio-rdm's permission-policy has fields unhandled by TU Graz's: {missing}\n"
            "if this is intentional, add to ALLOWED_DIFFERENCES\n"
            "otherwise set the corresponding fields in TUGrazRDMRecordPermissionPolicy"
        )

    # check whether same permission-generators used for same `can_<action>`
    for can_name in rdm_cans.keys() & tugraz_cans.keys():
        if can_name in ALLOWED_DIFFERENCES:
            continue

        tugraz_can = tugraz_cans[can_name]
        rdm_can = rdm_cans[can_name]

        # permission-Generators don't implement equality checks for their instances
        # we can however compare which types (classes) of Generators are used...
        if {type(gen) for gen in tugraz_can} != {type(gen) for gen in rdm_can}:
            raise ValueError(
                f"permission-policy for `{can_name}` differs between TU-Graz and invenio-rdm\n"
                "if this is intentional, add to ALLOWED_DIFFERENCES in test-file\n"
                "otherwise fix TUGrazRDMRecordPermissionPolicy"
            )

    # check whether same `NEED_LABEL_TO_ACTION`
    tugraz_label_to_action = TUGrazRDMRecordPermissionPolicy.NEED_LABEL_TO_ACTION
    rdm_label_to_action = RDMRecordPermissionPolicy.NEED_LABEL_TO_ACTION
    for label in tugraz_label_to_action.keys() & rdm_label_to_action.keys():
        if label in ALLOWED_DIFFERENCES:
            continue
        if tugraz_label_to_action.get(label) != rdm_label_to_action.get(label):
            raise ValueError(
                f"invenio-rdm's NEED_LABEL_TO_ACTION differs from TU Graz's in {label}\n"
                "if this is intentional, add to ALLOWED_DIFFERENCES in test-file\n"
                "otherwise fix TUGrazRDMRecordPermissionPolicy.NEED_LABEL_TO_ACTION"
            )
