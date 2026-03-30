# hr/workday_feed.py

import json

def load_workday_feed(file_path="workday_feed.json"):
    with open(file_path, "r") as f:
        return json.load(f)
