import requests
from config import GRAPH_BASE_URL, get_token

def disable_user(user_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {"accountEnabled": False}

    response = requests.patch(url, headers=headers, json=body)
    response.raise_for_status()
    print("User disabled successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    disable_user(user_id)
