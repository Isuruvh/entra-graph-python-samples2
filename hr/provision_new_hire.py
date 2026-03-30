# hr/provision_new_hire.py

from graph_users import create_user, update_user
from graph_groups import add_user_to_group, get_group_id_by_display_name
from graph_licenses import assign_license
from graph_roles import assign_role
from scim.scim_client import create_scim_user
from scim.scim_mapper import store_scim_id
from utils import generate_password
from config import config
from logger import log_event


def process_new_hire(record):
    """
    Full Workday → Entra → SCIM provisioning flow for a new hire.
    """

    first = record["firstName"]
    last = record["lastName"]
    department = record.get("department", "")
    job_title = record.get("jobTitle", "")
    location = record.get("location", "")

    # -------------------------
    # Step 1: Generate password
    # -------------------------
    password = generate_password()

    # -------------------------
    # Step 2: Create user in Entra
    # -------------------------
    result = create_user(first, last, password)

    if not result["success"]:
        log_event("NewHire_Failed", {"record": record, "error": result})
        return {"success": False, "error": "Failed to create user in Entra"}

    user = result["user"]
    user_id = user["id"]

    # Update department, job title, location
    update_user(user_id, {
        "department": department,
        "jobTitle": job_title,
        "officeLocation": location
    })

    # -------------------------
    # Step 3: Assign default groups
    # -------------------------
    assigned_groups = []
    for group_name in config.get("default_groups", []):
        group_id = get_group_id_by_display_name(group_name)
        if group_id:
            add_user_to_group(user_id, group_id)
            assigned_groups.append(group_name)

    # -------------------------
    # Step 4: Assign default licenses
    # -------------------------
    assigned_licenses = []
    for sku in config.get("default_license_skus", []):
        assign_license(user_id, sku)
        assigned_licenses.append(sku)

    # -------------------------
    # Step 5: Assign default roles
    # -------------------------
    assigned_roles = []
    for role in config.get("default_roles", []):
        assign_role(user_id, role)
        assigned_roles.append(role)

    # -------------------------
    # Step 6: Provision user into SCIM SaaS app
    # -------------------------
    scim_payload = {
        "userName": user["userPrincipalName"],
        "name": {
            "givenName": first,
            "familyName": last
        },
        "active": True,
        "department": department,
        "title": job_title
    }

    scim_user = create_scim_user(scim_payload)
    scim_id = scim_user.get("id")

    store_scim_id(user_id, scim_id)

    # -------------------------
    # Step 7: Log everything
    # -------------------------
    log_event("NewHire_Provisioned", {
        "entra_user_id": user_id,
        "scim_user_id": scim_id,
        "groups": assigned_groups,
        "licenses": assigned_licenses,
        "roles": assigned_roles
    })

    # -------------------------
    # Step 8: Return summary
    # -------------------------
    return {
        "success": True,
        "entra_user_id": user_id,
        "scim_user_id": scim_id,
        "upn": user["userPrincipalName"],
        "password": password,
        "assigned_groups": assigned_groups,
        "assigned_licenses": assigned_licenses,
        "assigned_roles": assigned_roles
    }
