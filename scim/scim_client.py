# scim/scim_client.py

import requests
from logger import log_event

SCIM_BASE = "http://localhost:8000"

def create_scim_user(user_obj):
    r = requests.post(f"{SCIM_BASE}/Users", json=user_obj)
    log_event("SCIM_CreateUser", {"payload": user_obj, "status": r.status_code})
    return r.json()

def update_scim_user(scim_id, changes):
    payload = {"Operations": [{"op": "replace", "value": changes}]}
    r = requests.patch(f"{SCIM_BASE}/Users/{scim_id}", json=payload)
    log_event("SCIM_UpdateUser", {"id": scim_id, "changes": changes, "status": r.status_code})
    return r.json()

def delete_scim_user(scim_id):
    r = requests.delete(f"{SCIM_BASE}/Users/{scim_id}")
    log_event("SCIM_DeleteUser", {"id": scim_id, "status": r.status_code})
    return r.json()
