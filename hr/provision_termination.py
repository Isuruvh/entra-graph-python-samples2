# hr/provision_termination.py

from graph_users import disable_user
from scim.scim_client import update_scim_user
from scim.scim_mapper import get_scim_id
from logger import log_event


def process_termination(record):
    """
    Workday → Entra → SCIM termination flow.
    """

    entra_id = record["employeeId"]
    scim_id = get_scim_id(entra_id)

    # -------------------------
    # Step 1: Disable in Entra
    # -------------------------
    entra_result = disable_user(entra_id)

    # -------------------------
    # Step 2: Deactivate SCIM user
    # -------------------------
    scim_result = None
    if scim_id:
        scim_result = update_scim_user(scim_id, {"active": False})

    # -------------------------
    # Step 3: Log event
    # -------------------------
    log_event("UserTerminated", {
        "entra_id": entra_id,
        "scim_id": scim_id,
        "entra_result": entra_result,
        "scim_result": scim_result
    })

    return {
        "success": True,
        "entra_result": entra_result,
        "scim_result": scim_result
    }
