import requests
from auth.msal_auth import get_access_token

def create_user():
    token = get_access_token()
    endpoint = "https://graph.microsoft.com/v1.0/users"

    body = {
        "accountEnabled": True,
        "displayName": "Test User",
        "mailNickname": "testuser",
        "userPrincipalName": "testuser@YOURDOMAIN.onmicrosoft.com",
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": "TempPass123!"
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, headers=headers, json=body)
    print(response.json())

if __name__ == "__main__":
    create_user()
