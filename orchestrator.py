"""
orchestrator.py
----------------
Central orchestration engine for IAM Automation Platform.

Coordinates:
- Workday feed events
- SCIM provisioning
- Microsoft Graph automation
- Logging and error handling

This module acts as the "brain" of the system.
"""

from logger import log
from hr.workday_events import WorkdayEventParser
from hr.provision_new_hire import process_new_hire
from hr.provision_update import process_update
from hr.provision_termination import process_termination

from graph_users import get_user

from utils import load_json_file


class IAMOrchestrator:

    def __init__(self, config_path="config.json"):
        log.info("Initializing IAM Orchestrator")
        self.config = load_json_file(config_path)
        self.parser = WorkdayEventParser()

    # ---------------------------------------------------------
    # HIGH-LEVEL ENTRYPOINTS
    # ---------------------------------------------------------

    def handle_workday_event(self, event: dict):
        """
        Main entrypoint for Workday -> IAM automation.
        """
        log.info(f"Received Workday event: {event}")

        event_type = self.parser.get_event_type(event)

        if event_type == "new_hire":
            return self._handle_new_hire(event)
        elif event_type == "update":
            return self._handle_update(event)
        elif event_type == "termination":
            return self._handle_termination(event)
        else:
            log.error(f"Unknown Workday event type: {event_type}")
            return {"status": "error", "message": "Unknown event type"}

    # ---------------------------------------------------------
    # EVENT HANDLERS
    # ---------------------------------------------------------

    def _handle_new_hire(self, event):
        log.info("Processing NEW HIRE event")
        result = process_new_hire(event)
        if not result.get("success"):
            return {"status": "error", "message": result.get("error", "New hire provisioning failed")}
        return {
            "status": "success",
            "message": "New hire provisioned successfully",
            "user_id": result.get("entra_user_id")
        }

    def _handle_update(self, event):
        log.info("Processing UPDATE event")
        user_id = event.get("employeeId")
        entra_user = get_user(user_id)
        result = process_update(event, entra_user)
        if not result.get("success"):
            return {"status": "error", "message": result.get("error", "User update failed")}
        return {
            "status": "success",
            "message": "User updated successfully",
            "user_id": user_id
        }

    def _handle_termination(self, event):
        log.info("Processing TERMINATION event")
        result = process_termination(event)
        if not result.get("success"):
            return {"status": "error", "message": result.get("error", "Termination failed")}
        return {
            "status": "success",
            "message": "User terminated successfully",
            "user_id": event.get("employeeId")
        }

    # ---------------------------------------------------------
    # BULK PROCESSING (CSV)
    # ---------------------------------------------------------

    def process_csv(self, csv_path: str):
        """
        Allows bulk provisioning via CSV upload.
        """
        import csv

        results = []

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                event = self.parser.from_csv_row(row)
                result = self.handle_workday_event(event)
                results.append(result)

        return results
