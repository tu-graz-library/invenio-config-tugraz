# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
