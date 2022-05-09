# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mojib Wali.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module that adds tugraz configs."""

from .ext import InvenioConfigTugraz
from .generators import RecordIp

__version__ = "0.8.4"

__all__ = ("__version__", "InvenioConfigTugraz", "RecordIp")
