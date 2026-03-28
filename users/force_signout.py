import requests

user_id = input("Enter User ID: ")

endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/invalidateAllRefreshTokens"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(endpoint, headers=headers, json={})  # <-- REQUIRED

print("Status Code:", response.status_code)
print("Response:", response.text)
