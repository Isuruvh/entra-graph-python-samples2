# main.py

import json

from graph_users import (
    create_user,
    get_user,
    list_users,
    update_user,
    disable_user,
    delete_user
)

from graph_groups import (
    create_group,
    get_group,
    list_groups,
    delete_group,
    add_user_to_group,
    remove_user_from_group,
    get_group_id_by_display_name
)

from graph_licenses import (
    list_skus,
    get_user_licenses,
    assign_license,
    remove_license
)

from graph_roles import (
    list_directory_roles,
    get_role_members,
    assign_role,
    remove_role
)


def pretty_print(data):
    """Clean JSON formatting for consistent CLI output."""
    print(json.dumps(data, indent=4))


def menu():
    print("\n==============================")
    print("     IAM AUTOMATION TOOL")
    print("==============================")
    print("[1] Create User")
    print("[2] Get User")
    print("[3] List Users")
    print("[4] Update User")
    print("[5] Disable User")
    print("[6] Delete User")
    print("------------------------------")
    print("[7] Create Group")
    print("[8] List Groups")
    print("[9] Add User to Group")
    print("[10] Remove User from Group")
    print("[11] Delete Group")
    print("------------------------------")
    print("[12] List License SKUs")
    print("[13] Get User Licenses")
    print("[14] Assign License to User")
    print("[15] Remove License from User")
    print("------------------------------")
    print("[16] List Directory Roles")
    print("[17] Get Role Members")
    print("[18] Assign Role to User")
    print("[19] Remove Role from User")
    print("------------------------------")
    print("[20] User Creation Wizard")
    print("------------------------------")
    print("[0] Exit")
    print("==============================")

    return input("Select an option: ").strip()


def main():
    while True:
        choice = menu()

        # -------------------------
        # USER OPERATIONS
        # -------------------------

        if choice == "1":
            print("\n--- Create User ---")
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            password = input("Temporary password: ").strip()
            pretty_print(create_user(first, last, password))

        elif choice == "2":
            print("\n--- Get User ---")
            upn = input("Enter UPN or Object ID: ").strip()
            pretty_print(get_user(upn))

        elif choice == "3":
            print("\n--- List Users ---")
            top = input("How many users to list (default 25): ").strip()
            top = int(top) if top.isdigit() else 25
            pretty_print(list_users(top))

        elif choice == "4":
            print("\n--- Update User ---")
            upn = input("Enter UPN or Object ID: ").strip()
            field = input("Field to update (e.g., displayName): ").strip()
            value = input("New value: ").strip()
            pretty_print(update_user(upn, {field: value}))

        elif choice == "5":
            print("\n--- Disable User ---")
            upn = input("Enter UPN or Object ID: ").strip()
            pretty_print(disable_user(upn))

        elif choice == "6":
            print("\n--- Delete User ---")
            upn = input("Enter UPN or Object ID: ").strip()
            pretty_print(delete_user(upn))

        # -------------------------
        # GROUP OPERATIONS
        # -------------------------

        elif choice == "7":
            print("\n--- Create Group ---")
            name = input("Group display name: ").strip()
            desc = input("Description (optional): ").strip()
            pretty_print(create_group(name, desc))

        elif choice == "8":
            print("\n--- List Groups ---")
            top = input("How many groups to list (default 25): ").strip()
            top = int(top) if top.isdigit() else 25
            pretty_print(list_groups(top))

        elif choice == "9":
            print("\n--- Add User to Group ---")
            user_id = input("User Object ID: ").strip()
            group_name = input("Group display name: ").strip()

            group_id = get_group_id_by_display_name(group_name)
            if not group_id:
                print(f"\nGroup '{group_name}' not found.")
            else:
                pretty_print(add_user_to_group(user_id, group_id))

        elif choice == "10":
            print("\n--- Remove User from Group ---")
            user_id = input("User Object ID: ").strip()
            group_name = input("Group display name: ").strip()

            group_id = get_group_id_by_display_name(group_name)
            if not group_id:
                print(f"\nGroup '{group_name}' not found.")
            else:
                pretty_print(remove_user_from_group(user_id, group_id))

        elif choice == "11":
            print("\n--- Delete Group ---")
            group_name = input("Group display name: ").strip()

            group_id = get_group_id_by_display_name(group_name)
            if not group_id:
                print(f"\nGroup '{group_name}' not found.")
            else:
                pretty_print(delete_group(group_id))

        # -------------------------
        # LICENSE OPERATIONS
        # -------------------------

        elif choice == "12":
            print("\n--- List License SKUs ---")
            pretty_print(list_skus())

        elif choice == "13":
            print("\n--- Get User Licenses ---")
            user_id = input("User Object ID: ").strip()
            pretty_print(get_user_licenses(user_id))

        elif choice == "14":
            print("\n--- Assign License to User ---")
            user_id = input("User Object ID: ").strip()
            sku_name = input("SKU Name (e.g., AAD_PREMIUM_P1): ").strip()
            pretty_print(assign_license(user_id, sku_name))

        elif choice == "15":
            print("\n--- Remove License from User ---")
            user_id = input("User Object ID: ").strip()
            sku_name = input("SKU Name (e.g., AAD_PREMIUM_P1): ").strip()
            pretty_print(remove_license(user_id, sku_name))

        # -------------------------
        # ROLE OPERATIONS
        # -------------------------

        elif choice == "16":
            print("\n--- List Directory Roles ---")
            pretty_print(list_directory_roles())

        elif choice == "17":
            print("\n--- Get Role Members ---")
            role_name = input("Role name (e.g., Global Reader): ").strip()
            roles = list_directory_roles()
            role_id = roles["roles"].get(role_name)

            if not role_id:
                print(f"\nRole '{role_name}' not found.")
            else:
                pretty_print(get_role_members(role_id))

        elif choice == "18":
            print("\n--- Assign Role to User ---")
            user_id = input("User Object ID: ").strip()
            role_name = input("Role name (e.g., Global Reader): ").strip()
            pretty_print(assign_role(user_id, role_name))

        elif choice == "19":
            print("\n--- Remove Role from User ---")
            user_id = input("User Object ID: ").strip()
            role_name = input("Role name (e.g., Global Reader): ").strip()
            pretty_print(remove_role(user_id, role_name))
        elif choice == "20":
            from user_wizard import user_creation_wizard
            summary = user_creation_wizard()
            pretty_print(summary)

        # -------------------------
        # EXIT
        # -------------------------

        elif choice == "0":
            print("\nExiting IAM Automation Tool. Goodbye.")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
