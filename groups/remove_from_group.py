import requests
from config import GRAPH_BASE_URL, get_token

def remove_from_group(user_id, group_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/groups/{group_id}/members/{user_id}/$ref"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    print("User removed from group successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    group_id = input("Group ID: ")
    remove_from_group(user_id, group_id)
