# graph_roles.py

import requests
from typing import Dict, Any, Optional, List

from auth import get_access_token

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def call_graph(
    method: str,
    endpoint: str,
    token: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generic Graph caller."""
    url = f"{GRAPH_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.request(method, url, headers=headers, params=params, json=json)

    try:
        data = response.json() if response.content else None
    except ValueError:
        data = None

    return {
        "success": response.ok,
        "status_code": response.status_code,
        "data": data,
        "error": None if response.ok else data
    }


# ---------------------------------------------------------
# ROLE FUNCTIONS
# ---------------------------------------------------------

def list_directory_roles() -> Dict[str, Any]:
    """List all active directory roles in the tenant."""
    token = get_access_token()
    result = call_graph("GET", "/directoryRoles", token)

    if not result["success"]:
        return result

    roles = result["data"].get("value", [])

    # Build friendly-name mapping
    friendly = {}
    for role in roles:
        name = role.get("displayName")
        role_id = role.get("id")
        friendly[name] = role_id

    return {
        "success": True,
        "roles": friendly,
        "raw": roles
    }


def get_role_id_by_name(role_name: str) -> Optional[str]:
    """Return the role ID for a friendly role name."""
    roles = list_directory_roles()
    if not roles["success"]:
        return None

    return roles["roles"].get(role_name)


def get_role_members(role_id: str) -> Dict[str, Any]:
    """Return all members of a directory role."""
    token = get_access_token()
    endpoint = f"/directoryRoles/{role_id}/members"

    result = call_graph("GET", endpoint, token)

    if not result["success"]:
        return result

    members = result["data"].get("value", [])

    return {
        "success": True,
        "members": members
    }


def user_has_role(user_id: str, role_id: str) -> bool:
    """Check if a user already has a specific directory role."""
    members = get_role_members(role_id)
    if not members["success"]:
        return False

    for m in members["members"]:
        if m.get("id") == user_id:
            return True

    return False


# ---------------------------------------------------------
# ROLE ASSIGNMENT
# ---------------------------------------------------------

def assign_role(user_id: str, role_name: str) -> Dict[str, Any]:
    """
    Assign a directory role to a user using friendly role name.
    Idempotent: will not assign if already present.
    """
    role_id = get_role_id_by_name(role_name)
    if not role_id:
        return {
            "success": False,
            "reason": "RoleNotFound",
            "message": f"Role '{role_name}' not found in tenant."
        }

    if user_has_role(user_id, role_id):
        return {
            "success": False,
            "reason": "AlreadyAssigned",
            "message": f"User already has role '{role_name}'."
        }

    token = get_access_token()
    endpoint = f"/directoryRoles/{role_id}/members/$ref"

    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
    }

    result = call_graph("POST", endpoint, token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def remove_role(user_id: str, role_name: str) -> Dict[str, Any]:
    """
    Remove a directory role from a user using friendly role name.
    Idempotent: will not fail if user doesn't have it.
    """
    role_id = get_role_id_by_name(role_name)
    if not role_id:
        return {
            "success": False,
            "reason": "RoleNotFound",
            "message": f"Role '{role_name}' not found in tenant."
        }

    if not user_has_role(user_id, role_id):
        return {
            "success": False,
            "reason": "NotAssigned",
            "message": f"User does not have role '{role_name}'."
        }

    token = get_access_token()
    endpoint = f"/directoryRoles/{role_id}/members/{user_id}/$ref"

    result = call_graph("DELETE", endpoint, token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


if __name__ == "__main__":
    print("graph_roles module loaded. Use from main.py for menu-driven flows.")
