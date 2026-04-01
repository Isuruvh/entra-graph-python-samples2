# logger.py

import os
import json
import logging
from datetime import datetime

log = logging.getLogger("iam_orchestrator")
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


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
