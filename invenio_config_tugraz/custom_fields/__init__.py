# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Custom fields."""


from invenio_records_resources.services.custom_fields import BooleanCF

ip_network = BooleanCF(name="ip_network")
single_ip = BooleanCF(name="single_ip")
