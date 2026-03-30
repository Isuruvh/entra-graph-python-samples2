# hr/workday_events.py
# hr/workday_events.py

def detect_event(record):
    if record["status"] == "Active" and record.get("isNewHire"):
        return "NewHire"
    if record["status"] == "Active" and record.get("isUpdated"):
        return "Update"
    if record["status"] == "Terminated":
        return "Termination"
    return "Ignore"

