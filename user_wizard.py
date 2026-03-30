# user_wizard.py

from graph_users import create_user
from graph_groups import add_user_to_group, get_group_id_by_display_name
from graph_licenses import assign_license
from graph_roles import assign_role
from utils import generate_password
from config import config
from logger import log_event


def user_creation_wizard():
    print("\n=== USER CREATION WIZARD ===")

    # -------------------------
    # Step 1: Collect inputs
    # -------------------------
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    department = input("Department: ").strip()
    job_title = input("Job Title: ").strip()
    location = input("Location: ").strip()

    # -------------------------
    # Step 2: Generate password
    # -------------------------
    password = generate_password()

    # -------------------------
    # Step 3: Create user
    # -------------------------
    result = create_user(first, last, password)

    if not result["success"]:
        print("\nUser creation failed.")
        return result

    user = result["user"]
    user_id = user["id"]

    log_event("UserCreatedWizard", {
        "user_id": user_id,
        "first": first,
        "last": last,
        "department": department,
        "job_title": job_title,
        "location": location
    })

    # -------------------------
    # Step 4: Assign default groups
    # -------------------------
    assigned_groups = []
    for group_name in config.get("default_groups", []):
        group_id = get_group_id_by_display_name(group_name)
        if group_id:
            add_user_to_group(user_id, group_id)
            assigned_groups.append(group_name)

    # -------------------------
    # Step 5: Assign default licenses
    # -------------------------
    assigned_licenses = []
    for sku in config.get("default_license_skus", []):
        assign_license(user_id, sku)
        assigned_licenses.append(sku)

    # -------------------------
    # Step 6: Assign default roles
    # -------------------------
    assigned_roles = []
    for role in config.get("default_roles", []):
        assign_role(user_id, role)
        assigned_roles.append(role)

    # -------------------------
    # Step 7: Summary
    # -------------------------
    summary = {
        "user_id": user_id,
        "upn": user["userPrincipalName"],
        "password": password,
        "assigned_groups": assigned_groups,
        "assigned_licenses": assigned_licenses,
        "assigned_roles": assigned_roles
    }

    print("\n=== USER CREATED SUCCESSFULLY ===")
    return summary
