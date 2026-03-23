import csv
import requests
from auth.msal_auth import get_access_token

def export_users():
    token = get_access_token()
    endpoint = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,accountEnabled"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    data = response.json()["value"]

    with open("users_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "userPrincipalName", "accountEnabled"])

        for user in data:
            writer.writerow([
                user["id"],
                user["displayName"],
                user["userPrincipalName"],
                user["accountEnabled"]
            ])

    print("Export complete.")

if __name__ == "__main__":
    export_users()
