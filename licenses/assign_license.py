import requests
from auth.msal_auth import get_access_token

def assign_license(user_id, sku_id):
    token = get_access_token()
    endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/assignLicense"

    body = {
        "addLicenses": [{"skuId": sku_id}],
        "removeLicenses": []
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, headers=headers, json=body)
    print(response.json())

if __name__ == "__main__":
    assign_license("USER_ID_HERE", "SKU_ID_HERE")
