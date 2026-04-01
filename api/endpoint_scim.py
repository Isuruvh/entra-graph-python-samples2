# api/endpoint_scim.py

from fastapi import APIRouter
from scim.scim_client import create_scim_user, update_scim_user, delete_scim_user

router = APIRouter()


@router.post("/provision")
async def scim_provision(payload: dict):
    return create_scim_user(payload)


@router.patch("/update/{user_id}")
async def scim_update(user_id: str, payload: dict):
    return update_scim_user(user_id, payload)


@router.delete("/delete/{user_id}")
async def scim_delete(user_id: str):
    return delete_scim_user(user_id)
