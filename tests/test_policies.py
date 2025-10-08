# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tests for permissions-policy."""

from collections.abc import Iterable

from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_permissions.policies import BasePermissionPolicy

from invenio_config_tugraz.permissions.policies import (
    TUGrazCommunityPermissionPolicy,
    TUGrazRDMRecordPermissionPolicy,
)

ALLOWED_DIFFERENCES_COMMUNITY = {
    "can_create",
    "can_request_membership",
    "can_submit_record",
}

ALLOWED_DIFFERENCES_RDM = {
    "can_authenticated",
    "can_create",
    "can_search",
    "can_view",
    "can_all",
    "can_search_drafts",
    "can_tugraz_authenticated",
}


def ensure_need_labels_synced(
    tugraz_policy: type[BasePermissionPolicy],
    invenio_policy: type[BasePermissionPolicy],
    allowed_differences: Iterable,
) -> None:
    """Ensure given policies' "NEED_LABEL_TO_ACTION" attribute matches."""
    tugraz_has_need_label = hasattr(tugraz_policy, "NEED_LABEL_TO_ACTION")
    invenio_has_need_label = hasattr(invenio_policy, "NEED_LABEL_TO_ACTION")
    if not tugraz_has_need_label and not invenio_has_need_label:
        # policies are allowed to not have .NEED_LABEL_TO_ACTION
        # if neither policy has it, the policies are considered synced in that regard
        return

    if not tugraz_has_need_label:
        msg = f"{invenio_policy} has `NEED_LABEL_TO_ACTION`, but {tugraz_policy} hasn't"
        raise AttributeError(msg)
    if not invenio_has_need_label:
        msg = f"{tugraz_policy} has `NEED_LABEL_TO_ACTION`, but {invenio_policy} hasn't"
        raise AttributeError(msg)

    tugraz_label_to_action = tugraz_policy.NEED_LABEL_TO_ACTION
    invenio_label_to_action = invenio_policy.NEED_LABEL_TO_ACTION

    for label in tugraz_label_to_action.keys() & invenio_label_to_action.keys():
        if label in allowed_differences:
            continue

        if tugraz_label_to_action.get(label) != invenio_label_to_action.get(label):
            msg = f"""
            invenio's NEED_LABEL_TO_ACTION differs from TU Graz's in {label}
            if this is intentional, add to corresponding ALLOWED_DIFFERENCES_... in test-file
            otherwise fix .NEED_LABEL_TO_ACTION of {tugraz_policy}
            """
            raise ValueError(msg)


def ensure_policies_synced(
    tugraz_policy: type[BasePermissionPolicy],
    invenio_policy: type[BasePermissionPolicy],
    allowed_differences: Iterable,
) -> None:
    """Ensure given policies match, except for given allowed differences."""
    allowed_differences = set(allowed_differences)

    tugraz_cans = {
        name: getattr(tugraz_policy, name)
        for name in dir(tugraz_policy)
        if name.startswith("can_")
    }
    invenio_cans = {
        name: getattr(invenio_policy, name)
        for name in dir(invenio_policy)
        if name.startswith("can_")
    }

    # check whether same set of `can_<action>`s are covered by the two policies
    if extras := set(tugraz_cans) - set(invenio_cans) - allowed_differences:
        msg = f"""
        TU Graz's permission-policy has additional fields over invenio's: {sorted(extras)}
        if this is intentional, add to corresponding ALLOWED_DIFFERENCES_... in test-file
        otherwise remove extraneous fields from {tugraz_policy}
        """
        raise KeyError(msg)

    if missing := set(invenio_cans) - set(tugraz_cans):
        msg = f"""
        invenio-rdm's permission-policy has fields unhandled by TU Graz's: {missing}
        if this is intentional, add to corresponding ALLOWED_DIFFERENCES_... in test-file
        otherwise set the corresponding fields in {tugraz_policy}
        """
        raise KeyError(msg)

    # check whether same permission-generators used for same `can_<action>`
    for can_name in invenio_cans.keys() & tugraz_cans.keys():
        if can_name in allowed_differences:
            continue

        tugraz_can = tugraz_cans[can_name]
        invenio_can = invenio_cans[can_name]

        # permission-Generators don't implement equality checks for their instances
        # we can however compare which types (classes) of Generators are used...
        if {type(gen) for gen in tugraz_can} != {type(gen) for gen in invenio_can}:
            msg = f"""
            permission-policy for `{can_name}` differs between TU-Graz and invenio
            if this is intentional, add to corresponding ALLOWED_DIFFERENCES_... in test-file
            otherwise fix {tugraz_policy}
            """
            raise ValueError(msg)

    # check whether same `NEED_LABEL_TO_ACTION`
    ensure_need_labels_synced(tugraz_policy, invenio_policy, allowed_differences)


def test_community_policies_synced() -> None:
    """Make sure our community permission-policy stays synced with invenio's."""
    ensure_policies_synced(
        TUGrazCommunityPermissionPolicy,
        CommunityPermissionPolicy,
        ALLOWED_DIFFERENCES_COMMUNITY,
    )


def test_rdm_policies_synced() -> None:
    """Make sure our RDM permission-policy stays synced with invenio's."""
    ensure_policies_synced(
        TUGrazRDMRecordPermissionPolicy,
        RDMRecordPermissionPolicy,
        ALLOWED_DIFFERENCES_RDM,
    )
