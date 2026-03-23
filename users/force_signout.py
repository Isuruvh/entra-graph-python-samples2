import requests
from config import GRAPH_BASE_URL, get_token

def force_signout(user_id):
    token = get_token()
    url = f"{GRAPH_BASE_URL}/users/{user_id}/invalidateAllRefreshTokens"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    print("User forced to sign out successfully.")

if __name__ == "__main__":
    user_id = input("User ID: ")
    force_signout(user_id)
