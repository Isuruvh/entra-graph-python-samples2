# hr/workday_events.py

def detect_event(record):
    if record["status"] == "Active" and record.get("isNewHire"):
        return "NewHire"
    if record["status"] == "Active" and record.get("isUpdated"):
        return "Update"
    if record["status"] == "Terminated":
        return "Termination"
    return "Ignore"


class WorkdayEventParser:
    def get_event_type(self, event: dict) -> str:
        """Map a Workday event dict to a normalized event type string."""
        raw = detect_event(event)
        mapping = {
            "NewHire": "new_hire",
            "Update": "update",
            "Termination": "termination",
            "Ignore": "ignore",
        }
        return mapping.get(raw, "ignore")

    def from_csv_row(self, row: dict) -> dict:
        """Convert a CSV row (DictReader) into a Workday event dict."""
        return {
            "firstName": row.get("firstName", ""),
            "lastName": row.get("lastName", ""),
            "department": row.get("department", ""),
            "jobTitle": row.get("jobTitle", ""),
            "location": row.get("location", ""),
            "employeeId": row.get("employeeId", ""),
            "status": row.get("status", "Active"),
            "isNewHire": row.get("isNewHire", "").lower() in ("true", "1", "yes"),
            "isUpdated": row.get("isUpdated", "").lower() in ("true", "1", "yes"),
        }

