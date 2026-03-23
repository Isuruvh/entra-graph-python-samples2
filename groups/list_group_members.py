import requests
from config import GRAPH_BASE_URL, get_token

def list_group_members(group_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/groups/{group_id}/members?$select=id,displayName,userPrincipalName"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    members = response.json().get("value", [])

    for m in members:
        print(f"{m['displayName']} - {m.get('userPrincipalName')}")

if __name__ == "__main__":
    group_id = input("Group ID: ")
    list_group_members(group_id)
