import msal
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET, GRAPH_SCOPE

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=[GRAPH_SCOPE])

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Token error: {result}")
