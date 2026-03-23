import requests
from auth.msal_auth import get_access_token

def list_users():
    token = get_access_token()
    endpoint = "https://graph.microsoft.com/v1.0/users"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)

    print(response.json())

if __name__ == "__main__":
    list_users()
