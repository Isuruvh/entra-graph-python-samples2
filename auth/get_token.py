from msal_auth import get_access_token

if __name__ == "__main__":
    token = get_access_token()
    print("Access Token:")
    print(token)
