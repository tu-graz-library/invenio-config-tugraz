# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2026 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from .ext import InvenioConfigTugraz
from .utils import get_identity_from_user_by_email

__version__ = "0.14.0"

__all__ = (
    "InvenioConfigTugraz",
    "__version__",
    "get_identity_from_user_by_email",
)
