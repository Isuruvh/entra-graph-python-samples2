import requests
from config import GRAPH_BASE_URL, get_token

def update_user(user_id, new_display_name):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {"displayName": new_display_name}

    response = requests.patch(url, headers=headers, json=body)
    response.raise_for_status()
    print("User updated successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    new_name = input("New Display Name: ")
    update_user(user_id, new_name)
