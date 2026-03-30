# run_demo.py

from hr.workday_feed import load_workday_feed
from hr.workday_events import detect_event
from hr.provision_new_hire import process_new_hire
from hr.provision_update import process_update
from hr.provision_termination import process_termination
from graph_users import get_user
from logger import log_event
import json


def run_demo():
    print("\n==============================")
    print(" WORKDAY → ENTRA → SCIM DEMO ")
    print("==============================\n")

    feed = load_workday_feed()

    results = []

    for record in feed:
        event = detect_event(record)
        employee_id = record["employeeId"]

        print(f"\nProcessing employee: {employee_id} ({event})")

        if event == "NewHire":
            summary = process_new_hire(record)
            results.append({"employeeId": employee_id, "event": event, "result": summary})

        elif event == "Update":
            entra_user = get_user(record["employeeId"])
            summary = process_update(record, entra_user)
            results.append({"employeeId": employee_id, "event": event, "result": summary})

        elif event == "Termination":
            summary = process_termination(record)
            results.append({"employeeId": employee_id, "event": event, "result": summary})

        else:
            print(f"Skipping employee {employee_id} (no actionable event).")

    print("\n==============================")
    print("        DEMO COMPLETE         ")
    print("==============================\n")

    print(json.dumps(results, indent=4))

    log_event("DemoRunCompleted", {"results": results})


if __name__ == "__main__":
    run_demo()
