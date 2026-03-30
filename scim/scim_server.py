# scim/scim_server.py

from fastapi import FastAPI, HTTPException
from uuid import uuid4
import json
import os

app = FastAPI(title="Local SCIM 2.0 Server")

DATA_FILE = "scim_storage.json"

# Ensure storage exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"Users": []}, f)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.post("/Users")
def create_user(user: dict):
    data = load_data()
    scim_id = str(uuid4())

    user["id"] = scim_id
    data["Users"].append(user)

    save_data(data)
    return user


@app.get("/Users")
def list_users():
    data = load_data()
    return {"Resources": data["Users"], "totalResults": len(data["Users"])}


@app.get("/Users/{user_id}")
def get_user(user_id: str):
    data = load_data()
    for user in data["Users"]:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.patch("/Users/{user_id}")
def update_user(user_id: str, changes: dict):
    data = load_data()
    for user in data["Users"]:
        if user["id"] == user_id:
            for op in changes.get("Operations", []):
                if op["op"].lower() == "replace":
                    for key, value in op["value"].items():
                        user[key] = value
            save_data(data)
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/Users/{user_id}")
def delete_user(user_id: str):
    data = load_data()
    new_users = [u for u in data["Users"] if u["id"] != user_id]

    if len(new_users) == len(data["Users"]):
        raise HTTPException(status_code=404, detail="User not found")

    data["Users"] = new_users
    save_data(data)
    return {"status": "deleted"}
