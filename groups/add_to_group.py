import requests
from config import GRAPH_BASE_URL, get_token

def add_to_group(user_id, group_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/groups/{group_id}/members/$ref"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "@odata.id": f"{GRAPH_BASE_URL}/directoryObjects/{user_id}"
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    print("User added to group successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    group_id = input("Group ID: ")
    add_to_group(user_id, group_id)
