import msal
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

def get_access_token():
    """Acquire a Microsoft Graph access token using client credentials."""
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in result:
        raise Exception(f"Token acquisition failed: {result}")

    return result["access_token"]
