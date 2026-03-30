# hr/provision_update.py

from graph_users import update_user
from scim.scim_client import update_scim_user
from scim.scim_mapper import get_scim_id
from logger import log_event


def process_update(record, entra_user):
    """
    Workday → Entra → SCIM update flow.
    Only changed attributes are updated.
    """

    # Unwrap get_user() structured response if needed
    if "user" in entra_user:
        if not entra_user.get("success") or not entra_user["user"]:
            return {"success": False, "error": "Entra user not found"}
        entra_user = entra_user["user"]

    entra_id = entra_user["id"]
    scim_id = get_scim_id(entra_id)

    if not scim_id:
        return {"success": False, "error": "SCIM ID not found for user"}

    # -------------------------
    # Step 1: Determine changes
    # -------------------------
    changes = {}

    if record["department"] != entra_user.get("department"):
        changes["department"] = record["department"]

    if record["jobTitle"] != entra_user.get("jobTitle"):
        changes["jobTitle"] = record["jobTitle"]

    if record["location"] != entra_user.get("officeLocation"):
        changes["officeLocation"] = record["location"]

    if not changes:
        return {"success": True, "message": "No changes detected"}

    # -------------------------
    # Step 2: Update Entra
    # -------------------------
    entra_result = update_user(entra_id, changes)

    # -------------------------
    # Step 3: Update SCIM
    # -------------------------
    scim_changes = {
        "department": record["department"],
        "title": record["jobTitle"],
        "location": record["location"]
    }

    scim_result = update_scim_user(scim_id, scim_changes)

    # -------------------------
    # Step 4: Log event
    # -------------------------
    log_event("UserUpdated", {
        "entra_id": entra_id,
        "scim_id": scim_id,
        "changes": changes
    })

    # -------------------------
    # Step 5: Return summary
    # -------------------------
    return {
        "success": True,
        "entra_update": entra_result,
        "scim_update": scim_result,
        "changes_applied": changes
    }
