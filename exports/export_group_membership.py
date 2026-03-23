import requests
import csv
from config import GRAPH_BASE_URL, get_token

def export_group_membership(group_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/groups/{group_id}/members?$select=id,displayName,userPrincipalName"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    members = response.json().get("value", [])

    filename = f"group_{group_id}_members.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "userPrincipalName"])
        for m in members:
            writer.writerow([m["id"], m["displayName"], m.get("userPrincipalName")])

    print(f"Export complete: {filename}")

if __name__ == "__main__":
    group_id = input("Enter Group ID: ")
    export_group_membership(group_id)
