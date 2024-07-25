# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""`RoleNeed`s for permission policies.

To use these roles, add them to the database via:
    `$ invenio roles create tugraz_authenticated --description "..."`
then add roles to users via:
    `$ invenio roles add user@email.com tugraz_authenticated`
"""

from flask_principal import RoleNeed

# using `flask_principal.RoleNeed`` instead of `invenio_access.SystemRoleNeed`,
# because these roles are assigned by an admin rather than automatically by the system
tugraz_authenticated_user = RoleNeed("tugraz_authenticated")
