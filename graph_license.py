# graph_licenses.py

import requests
from typing import Dict, Any, Optional, List

from graph_auth import get_access_token

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
# SKU FUNCTIONS
# ---------------------------------------------------------

def list_skus() -> Dict[str, Any]:
    """List all available license SKUs in the tenant."""
    token = get_access_token()
    result = call_graph("GET", "/subscribedSkus", token)

    if not result["success"]:
        return result

    skus = result["data"].get("value", [])

    # Build friendly-name mapping
    friendly = {}
    for sku in skus:
        name = sku.get("skuPartNumber")
        sku_id = sku.get("skuId")
        friendly[name] = sku_id

    return {
        "success": True,
        "skus": friendly,
        "raw": skus
    }


def get_sku_id_by_name(sku_name: str) -> Optional[str]:
    """Return SKU ID for a friendly SKU name."""
    skus = list_skus()
    if not skus["success"]:
        return None

    return skus["skus"].get(sku_name)


# ---------------------------------------------------------
# USER LICENSE FUNCTIONS
# ---------------------------------------------------------

def get_user_licenses(user_id: str) -> Dict[str, Any]:
    """Return all licenses assigned to a user."""
    token = get_access_token()
    endpoint = f"/users/{user_id}/licenseDetails"

    result = call_graph("GET", endpoint, token)

    if not result["success"]:
        return result

    assigned = result["data"].get("value", [])

    # Extract SKU IDs
    sku_ids = [lic.get("skuId") for lic in assigned]

    return {
        "success": True,
        "assigned_skus": sku_ids,
        "raw": assigned
    }


def user_has_license(user_id: str, sku_id: str) -> bool:
    """Check if a user already has a specific license."""
    licenses = get_user_licenses(user_id)
    if not licenses["success"]:
        return False

    return sku_id in licenses["assigned_skus"]


# ---------------------------------------------------------
# LICENSE ASSIGNMENT
# ---------------------------------------------------------

def assign_license(user_id: str, sku_name: str) -> Dict[str, Any]:
    """
    Assign a license to a user using friendly SKU name.
    Idempotent: will not assign if already present.
    """
    sku_id = get_sku_id_by_name(sku_name)
    if not sku_id:
        return {
            "success": False,
            "reason": "SkuNotFound",
            "message": f"SKU '{sku_name}' not found in tenant."
        }

    if user_has_license(user_id, sku_id):
        return {
            "success": False,
            "reason": "AlreadyLicensed",
            "message": f"User already has license '{sku_name}'."
        }

    token = get_access_token()
    endpoint = f"/users/{user_id}/assignLicense"

    payload = {
        "addLicenses": [{"skuId": sku_id}],
        "removeLicenses": []
    }

    result = call_graph("POST", endpoint, token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


def remove_license(user_id: str, sku_name: str) -> Dict[str, Any]:
    """
    Remove a license from a user using friendly SKU name.
    Idempotent: will not fail if user doesn't have it.
    """
    sku_id = get_sku_id_by_name(sku_name)
    if not sku_id:
        return {
            "success": False,
            "reason": "SkuNotFound",
            "message": f"SKU '{sku_name}' not found in tenant."
        }

    if not user_has_license(user_id, sku_id):
        return {
            "success": False,
            "reason": "NotLicensed",
            "message": f"User does not have license '{sku_name}'."
        }

    token = get_access_token()
    endpoint = f"/users/{user_id}/assignLicense"

    payload = {
        "addLicenses": [],
        "removeLicenses": [sku_id]
    }

    result = call_graph("POST", endpoint, token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


if __name__ == "__main__":
    print("graph_licenses module loaded. Use from main.py for menu-driven flows.")
