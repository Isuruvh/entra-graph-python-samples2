# graph_licenses.py

import requests
from typing import Optional, Dict, Any, List

from auth import get_access_token

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def call_graph(
    method: str,
    endpoint: str,
    token: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generic Graph caller returning a structured response."""
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


def _resolve_sku_id(sku_name: str, token: str) -> Optional[str]:
    """Resolve a SKU display name or part number to its skuId."""
    result = call_graph("GET", "/subscribedSkus", token)
    if not result["success"] or not result["data"]:
        return None

    for sku in result["data"].get("value", []):
        if sku.get("skuPartNumber", "").upper() == sku_name.upper():
            return sku["skuId"]

    return None


# ============================================================
# LIST AVAILABLE LICENSE SKUs
# ============================================================

def list_skus() -> Dict[str, Any]:
    """List all subscribed license SKUs in the tenant."""
    token = get_access_token()
    result = call_graph("GET", "/subscribedSkus", token)

    skus: List[Dict[str, Any]] = []
    if result["success"] and result["data"]:
        skus = [
            {
                "skuId": s["skuId"],
                "skuPartNumber": s["skuPartNumber"],
                "consumed": s.get("consumedUnits"),
                "enabled": s.get("prepaidUnits", {}).get("enabled")
            }
            for s in result["data"].get("value", [])
        ]

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "skus": skus,
        "error": result["error"] if not result["success"] else None
    }


# ============================================================
# GET USER LICENSES
# ============================================================

def get_user_licenses(user_id: str) -> Dict[str, Any]:
    """Get licenses assigned to a user."""
    token = get_access_token()
    result = call_graph("GET", f"/users/{user_id}/licenseDetails", token)

    licenses: List[Dict[str, Any]] = []
    if result["success"] and result["data"]:
        licenses = [
            {
                "skuId": l["skuId"],
                "skuPartNumber": l["skuPartNumber"]
            }
            for l in result["data"].get("value", [])
        ]

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "licenses": licenses,
        "error": result["error"] if not result["success"] else None
    }


# ============================================================
# ASSIGN LICENSE
# ============================================================

def assign_license(user_id: str, sku_name: str) -> Dict[str, Any]:
    """Assign a license to a user by SKU part number (e.g., AAD_PREMIUM_P1)."""
    token = get_access_token()

    sku_id = _resolve_sku_id(sku_name, token)
    if not sku_id:
        return {
            "success": False,
            "reason": "SKUNotFound",
            "message": f"SKU '{sku_name}' not found in subscribed SKUs."
        }

    payload = {
        "addLicenses": [{"skuId": sku_id}],
        "removeLicenses": []
    }

    result = call_graph("POST", f"/users/{user_id}/assignLicense", token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


# ============================================================
# REMOVE LICENSE
# ============================================================

def remove_license(user_id: str, sku_name: str) -> Dict[str, Any]:
    """Remove a license from a user by SKU part number (e.g., AAD_PREMIUM_P1)."""
    token = get_access_token()

    sku_id = _resolve_sku_id(sku_name, token)
    if not sku_id:
        return {
            "success": False,
            "reason": "SKUNotFound",
            "message": f"SKU '{sku_name}' not found in subscribed SKUs."
        }

    payload = {
        "addLicenses": [],
        "removeLicenses": [sku_id]
    }

    result = call_graph("POST", f"/users/{user_id}/assignLicense", token, json=payload)

    return {
        "success": result["success"],
        "status_code": result["status_code"],
        "error": result["error"] if not result["success"] else None
    }


if __name__ == "__main__":
    print("graph_licenses module loaded. Use from main.py for menu-driven flows.")
