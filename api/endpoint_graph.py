# api/endpoint_graph.py

from fastapi import APIRouter
from graph_users import get_user, create_user, disable_user
from graph_licenses import assign_license, get_user_licenses
from config import config

router = APIRouter()


@router.get("/users/{user_id}")
async def api_get_user(user_id: str):
    return get_user(user_id)


@router.post("/users/create")
async def api_create_user(payload: dict):
    return create_user(
        first_name=payload["firstName"],
        last_name=payload["lastName"],
        password=payload["password"]
    )


@router.post("/users/{user_id}/disable")
async def api_disable_user(user_id: str):
    return disable_user(user_id)


@router.post("/users/{user_id}/assign-license")
async def api_assign_license(user_id: str, payload: dict):
    sku = payload.get("sku") or config.get("default_license_skus", [None])[0]
    if not sku:
        return {"success": False, "message": "No SKU provided"}
    return assign_license(user_id, sku)
