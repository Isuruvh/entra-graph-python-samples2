import requests
from auth import get_access_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def graph_headers():
    """Return Graph API headers with fresh token."""
    token = get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# ============================================================
# 1. CREATE GROUP (STATIC OR DYNAMIC)
# ============================================================

def create_group(display_name, description, dynamic_rule=None):
    url = f"{GRAPH_BASE}/groups"

    body = {
        "displayName": display_name,
        "description": description,
        "mailEnabled": False,
        "mailNickname": display_name.replace("-", ""),
        "securityEnabled": True
    }

    if dynamic_rule:
        body["groupTypes"] = ["DynamicMembership"]
        body["membershipRule"] = dynamic_rule
        body["membershipRuleProcessingState"] = "On"

    response = requests.post(url, json=body, headers=graph_headers())

    if response.status_code in (200, 201):
        print(f"[SUCCESS] Created group: {display_name}")
    else:
        print(f"[ERROR] Failed to create group: {display_name}")
        print(response.status_code, response.text)


# ============================================================
# 2. LIST ALL GROUPS
# ============================================================

def list_groups():
    url = f"{GRAPH_BASE}/groups?$select=id,displayName,description"
    response = requests.get(url, headers=graph_headers())

    if response.status_code != 200:
        print("[ERROR] Unable to list groups")
        print(response.status_code, response.text)
        return

    groups = response.json().get("value", [])
    for g in groups:
        print(f"{g['displayName']}  |  {g['id']}")


# ============================================================
# 3. GET GROUP MEMBERS
# ============================================================

def get_group_members(group_id):
    url = f"{GRAPH_BASE}/groups/{group_id}/members?$select=id,displayName,userPrincipalName"
    response = requests.get(url, headers=graph_headers())

    if response.status_code != 200:
        print("[ERROR] Unable to retrieve group members")
        print(response.status_code, response.text)
        return

    members = response.json().get("value", [])
    for m in members:
        print(f"{m['displayName']}  |  {m.get('userPrincipalName', 'N/A')}")


# ============================================================
# 4. ADD USER TO GROUP
# ============================================================

def add_user_to_group(group_id, user_id):
    url = f"{GRAPH_BASE}/groups/{group_id}/members/$ref"
    body = {
        "@odata.id": f"{GRAPH_BASE}/directoryObjects/{user_id}"
    }

    response = requests.post(url, json=body, headers=graph_headers())

    if response.status_code in (200, 204):
        print(f"[SUCCESS] Added user {user_id} to group {group_id}")
    else:
        print("[ERROR] Failed to add user to group")
        print(response.status_code, response.text)


# ============================================================
# 5. REMOVE USER FROM GROUP
# ============================================================

def remove_user_from_group(group_id, user_id):
    url = f"{GRAPH_BASE}/groups/{group_id}/members/{user_id}/$ref"
    response = requests.delete(url, headers=graph_headers())

    if response.status_code in (200, 204):
        print(f"[SUCCESS] Removed user {user_id} from group {group_id}")
    else:
        print("[ERROR] Failed to remove user from group")
        print(response.status_code, response.text)


# ============================================================
# 6. DELETE GROUP
# ============================================================

def delete_group(group_id):
    url = f"{GRAPH_BASE}/groups/{group_id}"
    response = requests.delete(url, headers=graph_headers())

    if response.status_code in (200, 204):
        print(f"[SUCCESS] Deleted group {group_id}")
    else:
        print("[ERROR] Failed to delete group")
        print(response.status_code, response.text)
