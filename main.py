import sys
import logging

from exports.export_groups import export_groups
from exports.export_group_membership import export_group_membership
from exports.export_user_access import export_user_access

from groups.add_to_group import add_to_group
from groups.list_group_members import list_group_members
from groups.remove_from_group import remove_from_group

from users.delete_user import delete_user
from users.disable_user import disable_user
from users.force_signout import force_signout
from users.update_user import update_user


# ---------- Logging configuration ----------

logging.basicConfig(
    filename="iam_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------- Menu UI ----------

def menu():
    print("\n=== Microsoft Graph IAM Automation Toolkit ===")
    print("1. Export all Groups")
    print("2. Export Group Membership")
    print("3. Export User Access (Groups user belongs to)")
    print("4. Add User to Group")
    print("5. List Group Members")
    print("6. Remove User from Group")
    print("7. Delete User")
    print("8. Disable User")
    print("9. Force User Sign-Out")
    print("10. Update User Display Name")
    print("0. Exit")
    print("===============================================")


# ---------- Main loop ----------

def main():
    logging.info("IAM Automation Toolkit started")

    while True:
        menu()
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                logging.info("Action selected: Export Groups")
                export_groups()
                logging.info("Action completed: Export Groups")

            elif choice == "2":
                group_id = input("Enter Group ID: ").strip()
                logging.info(f"Action selected: Export Group Membership for group {group_id}")
                export_group_membership(group_id)
                logging.info(f"Action completed: Export Group Membership for group {group_id}")

            elif choice == "3":
                user_id = input("Enter User ID: ").strip()
                logging.info(f"Action selected: Export User Access for user {user_id}")
                export_user_access(user_id)
                logging.info(f"Action completed: Export User Access for user {user_id}")

            elif choice == "4":
                user_id = input("Enter User ID: ").strip()
                group_id = input("Enter Group ID: ").strip()
                logging.info(f"Action selected: Add user {user_id} to group {group_id}")
                add_to_group(user_id, group_id)
                logging.info(f"Action completed: Add user {user_id} to group {group_id}")

            elif choice == "5":
                group_id = input("Enter Group ID: ").strip()
                logging.info(f"Action selected: List members of group {group_id}")
                list_group_members(group_id)
                logging.info(f"Action completed: List members of group {group_id}")

            elif choice == "6":
                user_id = input("Enter User ID: ").strip()
                group_id = input("Enter Group ID: ").strip()
                logging.info(f"Action selected: Remove user {user_id} from group {group_id}")
                remove_from_group(user_id, group_id)
                logging.info(f"Action completed: Remove user {user_id} from group {group_id}")

            elif choice == "7":
                user_id = input("Enter User ID: ").strip()
                logging.info(f"Action selected: Delete user {user_id}")
                delete_user(user_id)
                logging.info(f"Action completed: Delete user {user_id}")

            elif choice == "8":
                user_id = input("Enter User ID: ").strip()
                logging.info(f"Action selected: Disable user {user_id}")
                disable_user(user_id)
                logging.info(f"Action completed: Disable user {user_id}")

            elif choice == "9":
                user_id = input("Enter User ID: ").strip()
                logging.info(f"Action selected: Force sign-out for user {user_id}")
                force_signout(user_id)
                logging.info(f"Action completed: Force sign-out for user {user_id}")

            elif choice == "10":
                user_id = input("Enter User ID: ").strip()
                new_name = input("Enter new display name: ").strip()
                logging.info(f"Action selected: Update user {user_id} display name to '{new_name}'")
                update_user(user_id, new_name)
                logging.info(f"Action completed: Update user {user_id} display name")

            elif choice == "0":
                logging.info("Exit selected. Shutting down IAM Automation Toolkit.")
                print("Exiting...")
                sys.exit(0)

            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            logging.error(f"Error occurred during action '{choice}': {e}")
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
