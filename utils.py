# utils.py

import json
import secrets
import string
from config import config

def load_json_file(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def generate_password() -> str:
    length = config.get("default_password_length", 16)
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
