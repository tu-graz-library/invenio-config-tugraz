# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from .ext import InvenioConfigTugraz
from .generators import RecordIp
from .utils import get_identity_from_user_by_email

__version__ = "0.12.0"

__all__ = (
    "__version__",
    "InvenioConfigTugraz",
    "RecordIp",
    "get_identity_from_user_by_email",
)
