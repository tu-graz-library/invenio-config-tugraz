# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from collections.abc import Callable
from types import SimpleNamespace

import pytest
from flask import Flask
from flask_principal import AnonymousIdentity, Identity, RoleNeed
from invenio_access.permissions import (
    _P,
    Permission,
    any_user,
    authenticated_user,
    system_process,
)
from invenio_curations.services.generators import IfCurationRecordBasedExists

from invenio_config_tugraz import InvenioConfigTugraz
from invenio_config_tugraz.permissions.roles import tugraz_authenticated_user


@pytest.fixture(scope="module")
def create_app(instance_path: str) -> Callable[..., Flask]:
    """Application factory fixture."""

    def factory(**config: str) -> Flask:
        app = Flask("testapp", instance_path=instance_path)
        app.config.update(**config)
        InvenioConfigTugraz(app)
        return app

    return factory


@pytest.fixture
def identity_anon() -> AnonymousIdentity:
    """Anonymous identity."""
    id_ = AnonymousIdentity()
    id_.provides.add(any_user)
    return id_


@pytest.fixture
def identity_generic_authenticated() -> Identity:
    """Base Invenio Authenticated user."""  # noqa: D401
    id_ = Identity(1)
    id_.provides.update({any_user, authenticated_user})
    return id_


@pytest.fixture
def identity_tugraz_authenticated() -> Identity:
    """TU Graz-authenticated user."""
    id_ = Identity(2)
    id_.provides.update({any_user, authenticated_user, tugraz_authenticated_user})
    return id_


@pytest.fixture
def identity_system() -> Identity:
    """System process identity."""
    id_ = Identity(3)
    id_.provides.update({any_user, system_process})
    return id_


@pytest.fixture
def identity_curation_moderator() -> Identity:
    """Identity with curation moderation role."""
    id_ = Identity(4)
    # Default curation role name in Invenio is "administration-rdm-records-curation"
    id_.provides.update(
        {
            any_user,
            authenticated_user,
            RoleNeed("administration-rdm-records-curation"),
        },
    )
    return id_


@pytest.fixture
def mock_community_open() -> SimpleNamespace:
    """Mock community."""
    return SimpleNamespace(
        id="test-community-1",
        access=SimpleNamespace(
            record_submission_policy="open",
            visibility="public",
            member_policy="open",
        ),
    )


@pytest.fixture(autouse=True)
def mock_permission_db_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    """Bypass database and invenio-access lookups in Permission._load_permissions."""

    def mock_load(self: Permission) -> None:
        self._permissions = _P(
            needs=set(self.explicit_needs),
            excludes=set(self.explicit_excludes),
        )

    monkeypatch.setattr(Permission, "_load_permissions", mock_load)


@pytest.fixture(autouse=True)
def mock_default_curation_condition(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default IfCurationRecordBasedExists condition to False to bypass invenio-curations lookup."""
    monkeypatch.setattr(
        IfCurationRecordBasedExists,
        "_condition",
        lambda self, record=None, **kwargs: False,  # noqa: ARG005
    )
