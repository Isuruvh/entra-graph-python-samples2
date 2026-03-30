# scim/scim_mapper.py

import json
import os

MAP_FILE = "scim/scim_mapping.json"

if not os.path.exists(MAP_FILE):
    with open(MAP_FILE, "w") as f:
        json.dump({"users": {}}, f)


def load_map():
    with open(MAP_FILE, "r") as f:
        return json.load(f)


def save_map(data):
    with open(MAP_FILE, "w") as f:
        json.dump(data, f, indent=4)


def store_scim_id(entra_id, scim_id):
    data = load_map()
    data["users"][entra_id] = scim_id
    save_map(data)


def get_scim_id(entra_id):
    data = load_map()
    return data["users"].get(entra_id)
