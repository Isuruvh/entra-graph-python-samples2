import os
from dotenv import load_dotenv

# Load .env file
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
