import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = PROJECT_ROOT / "config" / "security_policy.json"


class AccessControl:

    def __init__(self, policy_path=None):
        path = Path(policy_path or POLICY_PATH)

        with open(path, "r", encoding="utf-8-sig") as file:
            self.policy = json.load(file)

        self.roles = self.policy.get("roles", {})

    def has_permission(self, role, permission):
        if not isinstance(role, str) or not isinstance(permission, str):
            return False

        permissions = self.roles.get(role.lower(), [])
        return permission in permissions

    def require_permission(self, role, permission):
        if not self.has_permission(role, permission):
            raise PermissionError(
                f"Role '{role}' is not authorized for '{permission}'."
            )

    def get_permissions(self, role):
        if not isinstance(role, str):
            return []

        return list(self.roles.get(role.lower(), []))
