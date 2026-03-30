# config.py

import os
import json
from dotenv import load_dotenv

# -----------------------------
# Load .env (secrets)
# -----------------------------
load_dotenv()

def get_env_variable(name: str) -> str:
    """Retrieve an environment variable or raise a clear error."""
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

TENANT_ID = get_env_variable("TENANT_ID")
CLIENT_ID = get_env_variable("CLIENT_ID")
CLIENT_SECRET = get_env_variable("CLIENT_SECRET")


# -----------------------------
# Load config.json (settings)
# -----------------------------
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Missing configuration file: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()


# -----------------------------
# Graph base URL
# -----------------------------
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


# -----------------------------
# Token retrieval wrapper
# -----------------------------
def get_token() -> str:
    """Wrapper to keep compatibility with existing modules."""
    from auth import get_access_token
    return get_access_token()
