import requests
from config import GRAPH_BASE_URL, get_token

def delete_user(user_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    print("User deleted successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    delete_user(user_id)
