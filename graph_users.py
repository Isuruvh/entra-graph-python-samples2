# graph_users.py
from logger import log_event
import requests
from typing import Optional, Dict, Any, List

from auth import get_access_token

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
DEFAULT_DOMAIN = "isurutrader.onmicrosoft.com"


def call_graph(
    method: str,
    endpoint: str,
    token: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generic Graph caller returning a structured response.
    """
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

    success = response.ok

    return {
        "success": success,
        "status_code": response.status_code,
        "data": data,
        "error": None if success else data
    }


def generate_upn(first_name: str, last_name: str, domain: str = DEFAULT_DOMAIN) -> str:
    """
    Build a UPN from first and last name.
    """
    base = f"{first_name}.{last_name}".replace(" ", "").lower()
    return f"{base}@{domain}"


def generate_mail_nickname(first_name: str, last_name: str) -> str:
    """
    Build a mailNickname (alias) from first and last name.
    """
    return f"{first_name}{last_name}".replace(" ", "").lower()


def build_password_profile(password: str, force_change: bool = True) -> Dict[str, Any]:
    """
    Build a passwordProfile object for user creation.
    """
    return {
        "forceChangePasswordNextSignIn": force_change,
        "password": password
    }


def user_exists(upn: str) -> Dict[str, Any]:
    """
    Check if a user exists by UPN.
    """
    token = get_access_token()
    endpoint = f"/users/{upn}"

    result = call_graph("GET", endpoint, token)

    if result["success"]:
        return {
            "exists": True,
            "user": result["data"]
        }

    if result["status_code"] == 404:
        return {
            "exists": False,
            "user": None
        }

    return {
        "exists": False,
        "user": None,
        "error": result["error"],
        "status_code": result["status_code"]
    }


def create_user(
    first_name: str,
    last_name: str,
    password: str,
    domain: str = DEFAULT_DOMAIN
) -> Dict[str, Any]:
    """
    Create a new user with generated UPN and mailNickname.
    Idempotent: will not create if user already exists.
    """
    token = get_access_token()

    upn = generate_upn(first_name, last_name, domain)
    mail_nickname = generate_mail_nickname(first_name, last_name)

    exists_result = user_exists(upn)
    if exists_result.get("exists"):
        return {
            "success": False,
            "reason": "UserAlreadyExists",
            "message": f"User with UPN {upn} already exists.",
            "user": exists_result.get("user")
        }

    user_payload = {
        "accountEnabled": True,
        "displayName": f"{first_name} {last_name}",
        "mailNickname": mail_nickname,
        "userPrincipalName": upn,
        "passwordProfile": build_password_profile(password)
    }

    result = call_graph("POST", "/users", token, json=user_payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "user": result["data"] if result["success"] else None,
        "error": result["error"] if not result["success"] else None
    }


def get_user(upn_or_id: str) -> Dict[str, Any]:
    """
    Get a user by UPN or objectId.
    """
    token = get_access_token()
    endpoint = f"/users/{upn_or_id}"

    result = call_graph("GET", endpoint, token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "user": result["data"] if result["success"] else None,
        "error": result["error"] if not result["success"] else None
    }


def list_users(top: int = 25) -> Dict[str, Any]:
    """
    List users in the tenant.
    """
    token = get_access_token()
    params = {
        "$top": top
    }

    result = call_graph("GET", "/users", token, params=params)

    users: List[Dict[str, Any]] = []
    if result["success"] and "value" in result["data"]:
        users = result["data"]["value"]

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "users": users if result["success"] else [],
        "error": result["error"] if not result["success"] else None
    }


def update_user(
    upn_or_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a user with a partial payload (PATCH).
    Example updates: {"displayName": "New Name"}
    """
    token = get_access_token()
    endpoint = f"/users/{upn_or_id}"

    result = call_graph("PATCH", endpoint, token, json=updates)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def disable_user(upn_or_id: str) -> Dict[str, Any]:
    """
    Disable a user (accountEnabled = False).
    """
    return update_user(upn_or_id, {"accountEnabled": False})


def delete_user(upn_or_id: str) -> Dict[str, Any]:
    """
    Delete a user by UPN or objectId.
    """
    token = get_access_token()
    endpoint = f"/users/{upn_or_id}"

    result = call_graph("DELETE", endpoint, token)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


if __name__ == "__main__":
    # Simple manual smoke test hooks (optional)
    print("graph_users module loaded. Use from main.py for menu-driven flows.")
