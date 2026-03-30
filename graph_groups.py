import csv
import requests
from typing import Optional, Dict, Any, List
from auth import get_access_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def call_graph(
    method: str,
    endpoint: str,
    token: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generic Graph caller returning a structured response."""
    url = f"{GRAPH_BASE}{endpoint}"
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


# ============================================================
# CORE GROUP FUNCTIONS
# ============================================================

def create_group(display_name: str, description: str = "", dynamic_rule: str = None) -> Dict[str, Any]:
    """Create a security group. Idempotent: will not create if already exists."""
    token = get_access_token()

    check = get_group_id_by_display_name(display_name)
    if check:
        return {
            "success": False,
            "reason": "GroupAlreadyExists",
            "message": f"Group '{display_name}' already exists.",
            "group_id": check
        }

    payload = {
        "displayName": display_name,
        "description": description,
        "mailEnabled": False,
        "mailNickname": display_name.replace(" ", "").lower(),
        "securityEnabled": True
    }

    if dynamic_rule:
        payload["groupTypes"] = ["DynamicMembership"]
        payload["membershipRule"] = dynamic_rule
        payload["membershipRuleProcessingState"] = "On"

    result = call_graph("POST", "/groups", token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "group": result["data"] if result["success"] else None,
        "error": result["error"] if not result["success"] else None
    }


def get_group(group_id: str) -> Dict[str, Any]:
    """Get a group by ID."""
    token = get_access_token()
    result = call_graph("GET", f"/groups/{group_id}", token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "group": result["data"] if result["success"] else None,
        "error": result["error"] if not result["success"] else None
    }


def list_groups(top: int = 25) -> Dict[str, Any]:
    """List groups in the tenant."""
    token = get_access_token()
    result = call_graph("GET", "/groups", token, params={"$top": top, "$select": "id,displayName,description"})

    groups: List[Dict[str, Any]] = []
    if result["success"] and result["data"] and "value" in result["data"]:
        groups = result["data"]["value"]

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "groups": groups,
        "error": result["error"] if not result["success"] else None
    }


def delete_group(group_id: str) -> Dict[str, Any]:
    """Delete a group by ID."""
    token = get_access_token()
    result = call_graph("DELETE", f"/groups/{group_id}", token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def get_group_id_by_display_name(display_name: str) -> Optional[str]:
    """Return the group ID for a given displayName, or None if not found."""
    token = get_access_token()
    result = call_graph("GET", "/groups", token, params={"$filter": f"displayName eq '{display_name}'"})

    if result["success"] and result["data"] and result["data"].get("value"):
        return result["data"]["value"][0]["id"]

    return None


# ============================================================
# MEMBERSHIP FUNCTIONS
# ============================================================

def add_user_to_group(user_id: str, group_id: str) -> Dict[str, Any]:
    """Add a user to a group."""
    token = get_access_token()
    payload = {"@odata.id": f"{GRAPH_BASE}/directoryObjects/{user_id}"}
    result = call_graph("POST", f"/groups/{group_id}/members/$ref", token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def remove_user_from_group(user_id: str, group_id: str) -> Dict[str, Any]:
    """Remove a user from a group."""
    token = get_access_token()
    result = call_graph("DELETE", f"/groups/{group_id}/members/{user_id}/$ref", token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def get_group_members(group_id: str) -> Dict[str, Any]:
    """Get members of a group."""
    token = get_access_token()
    result = call_graph("GET", f"/groups/{group_id}/members", token,
                        params={"$select": "id,displayName,userPrincipalName"})

    members: List[Dict[str, Any]] = []
    if result["success"] and result["data"] and "value" in result["data"]:
        members = result["data"]["value"]

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "members": members,
        "error": result["error"] if not result["success"] else None
    }


# ============================================================
# CSV EXPORT FUNCTIONS
# ============================================================

def export_groups():
    token = get_access_token()
    result = call_graph("GET", "/groups", token,
                        params={"$select": "id,displayName,mail,groupTypes"})
    result["data"]["value"] if result["success"] else []
    groups = result["data"].get("value", []) if result["success"] and result["data"] else []

    with open("groups.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "mail", "groupTypes"])
        for g in groups:
            writer.writerow([g["id"], g["displayName"], g.get("mail"), ",".join(g.get("groupTypes", []))])

    print("Export complete: groups.csv")


def export_group_membership(group_id: str):
    result = get_group_members(group_id)
    members = result.get("members", [])

    filename = f"group_{group_id}_members.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "userPrincipalName"])
        for m in members:
            writer.writerow([m["id"], m["displayName"], m.get("userPrincipalName")])

    print(f"Export complete: {filename}")


def export_user_access(user_id: str):
    token = get_access_token()
    result = call_graph("GET", f"/users/{user_id}/memberOf", token,
                        params={"$select": "id,displayName"})
    groups = result["data"].get("value", []) if result["success"] and result["data"] else []

    filename = f"user_{user_id}_access.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName"])
        for g in groups:
            writer.writerow([g["id"], g["displayName"]])

    print(f"Export complete: {filename}")
