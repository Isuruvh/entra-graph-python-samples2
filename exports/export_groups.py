import requests
import csv
from config import GRAPH_BASE_URL, get_token

def export_groups():
    token = get_token()
    url = f"{GRAPH_BASE_URL}/groups?$select=id,displayName,mail,groupTypes"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    groups = response.json().get("value", [])

    with open("groups.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "mail", "groupTypes"])
        for g in groups:
            writer.writerow([g["id"], g["displayName"], g.get("mail"), ",".join(g.get("groupTypes", []))])

    print("Export complete: groups.csv")

if __name__ == "__main__":
    export_groups()
