# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""invenio module that adds tugraz configs."""

from .ext import InvenioConfigTugraz
from .utils import get_identity_from_user_by_email

__version__ = "0.14.10"

__all__ = (
    "InvenioConfigTugraz",
    "__version__",
    "get_identity_from_user_by_email",
)
