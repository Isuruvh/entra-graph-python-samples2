# logger.py

import os
import json
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "iam_audit.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def log_event(action: str, details: dict):
    """
    Write a structured audit log entry.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
