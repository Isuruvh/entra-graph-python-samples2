import requests
import csv
from config import GRAPH_BASE_URL, get_token

def export_user_access(user_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/users/{user_id}/memberOf?$select=id,displayName"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    groups = response.json().get("value", [])

    filename = f"user_{user_id}_access.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName"])
        for g in groups:
            writer.writerow([g["id"], g["displayName"]])

    print(f"Export complete: {filename}")

if __name__ == "__main__":
    user_id = input("Enter User ID: ")
    export_user_access(user_id)
