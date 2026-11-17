# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Tests for permissions-policy."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from flask import Flask
from flask_principal import AnonymousIdentity, Identity
from invenio_curations.services.generators import (
    CurationModerators,
    IfCurationRecordBasedExists,
)
from invenio_pidstore.models import PersistentIdentifier

import invenio_config_tugraz.permissions.generators as generators_mod
from invenio_config_tugraz.permissions.policies import (
    TUGrazCommunityPermissionPolicy,
    TUGrazRDMRecordPermissionPolicy,
)


class MockRecord(dict):
    """Mock record behaving as a dict while providing Invenio attribute access."""

    def __init__(self, custom_fields: dict | None = None) -> None:
        """Construct."""
        super().__init__(custom_fields=custom_fields or {})
        self.parent = MagicMock()
        self.parent.access.owner.owner_id = 10000
        self.pid = PersistentIdentifier(
            pid_type="recid",
            pid_value="12345",
        )
        self.parent.access.grants.needs.return_value = []
        self.parent.access.links.needs.return_value = []
        self.parent.communities.ids = []
        self.access = MagicMock()

    def get_review(self) -> None:
        """Get review."""
        return


@pytest.mark.parametrize("action", ["create", "search_drafts", "authenticated"])
def test_tugraz_authentication_actions(  # noqa: PLR0913, PLR0917
    base_app: Flask,
    action: str,
    identity_anon: AnonymousIdentity,
    identity_generic_authenticated: Identity,
    identity_tugraz_authenticated: Identity,
    identity_system: Identity,
) -> None:
    """Test tugraz_authenticated policies."""
    with base_app.app_context():
        policy = TUGrazRDMRecordPermissionPolicy(action)
        assert not policy.allows(identity_anon)
        assert not policy.allows(identity_generic_authenticated)
        assert policy.allows(identity_tugraz_authenticated)
        assert policy.allows(identity_system)


@pytest.mark.parametrize(
    ("single_ip", "result"),
    [("192.168.1.100", False), ("192.168.1.50", True)],
)
def test_can_view_and_can_all_ip_restrictions(
    base_app: Flask,
    identity_anon: AnonymousIdentity,
    single_ip: str,
    result: bool,  # noqa: FBT001
) -> None:
    """Test custom network policies."""
    record_with_single_ip = MockRecord({"single_ip": True})
    record_with_network_ip = MockRecord({"ip_network": True})
    record_regular = MockRecord()

    with base_app.test_request_context(environ_base={"REMOTE_ADDR": "192.168.1.50"}):
        # Configure allowed IPs
        base_app.config["CONFIG_TUGRAZ_SINGLE_IPS"] = [single_ip]
        base_app.config["CONFIG_TUGRAZ_IP_NETWORK"] = "10.0.0.0/8"
        policy_view = TUGrazRDMRecordPermissionPolicy(
            "view",
            record=record_with_single_ip,
        )
        assert policy_view.allows(identity_anon) is result
        policy_all = TUGrazRDMRecordPermissionPolicy(
            "all",
            record=record_with_network_ip,
        )
        assert not policy_all.allows(identity_anon)

        # Regular record without IP custom field is accessible via can_all
        policy_regular = TUGrazRDMRecordPermissionPolicy(
            "all",
            record=record_regular,
        )
        assert policy_regular.allows(identity_anon)


def test_can_preview_curation_moderator(
    base_app: Flask,
    monkeypatch: pytest.MonkeyPatch,
    identity_anon: AnonymousIdentity,
    identity_curation_moderator: Identity,
) -> None:
    """Test custom curations policies."""
    role_name = "administration-rdm-records-curation"

    mock_curations_service = MagicMock(
        moderation_role_name=role_name,
        get_review=lambda self, identity, topic, **kwargs: None,  # noqa: ARG005
    )
    monkeypatch.setattr(
        CurationModerators,
        "_curations_service",
        mock_curations_service,
    )
    with base_app.app_context():
        # Case 1: Curation request exists
        monkeypatch.setattr(
            IfCurationRecordBasedExists,
            "_condition",
            lambda self, record=None, **kwargs: True,  # noqa: ARG005
        )
        policy = TUGrazRDMRecordPermissionPolicy("preview", record=MockRecord())
        assert policy.allows(identity_curation_moderator)
        assert not policy.allows(identity_anon)

        # Case 2: No curation request exists
        monkeypatch.setattr(
            IfCurationRecordBasedExists,
            "_condition",
            lambda self, record=None, **kwargs: False,  # noqa: ARG005
        )
        policy_no_curation = TUGrazRDMRecordPermissionPolicy(
            "preview",
            record=MockRecord(),
        )
        assert not policy_no_curation.allows(identity_curation_moderator)
        assert not policy_no_curation.allows(identity_anon)


@pytest.mark.parametrize(
    ("action", "requires_community"),
    [
        ("create", False),
        ("submit_record", True),
        ("request_membership", True),
    ],
)
def test_community_tugraz_authentication_actions(  # noqa: PLR0913, PLR0917
    base_app: Flask,
    action: str,
    requires_community: bool,  # noqa: FBT001
    mock_community_open: SimpleNamespace,
    identity_anon: AnonymousIdentity,
    identity_generic_authenticated: Identity,
    identity_tugraz_authenticated: Identity,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test custom community policies."""
    monkeypatch.setattr(
        generators_mod,
        "current_roles",
        [SimpleNamespace(name="member"), SimpleNamespace(name="owner")],
    )
    with base_app.app_context():
        base_app.config["COMMUNITIES_ALLOW_MEMBERSHIP_REQUESTS"] = True
        kwargs = {"record": mock_community_open} if requires_community else {}
        policy = TUGrazCommunityPermissionPolicy(action, **kwargs)
        # Anonymous -> denied
        assert not policy.allows(identity_anon)
        # Generic authenticated user (non-TU Graz) -> denied
        assert not policy.allows(identity_generic_authenticated)
        # TU Graz-authenticated user -> granted
        assert policy.allows(identity_tugraz_authenticated)
