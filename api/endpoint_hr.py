# api/endpoints_hr.py

from fastapi import APIRouter, UploadFile, File
from orchestrator import IAMOrchestrator

router = APIRouter()
orchestrator = IAMOrchestrator()

@router.post("/new-hire")
async def new_hire(event: dict):
    return orchestrator.handle_workday_event(event)

@router.post("/update")
async def update(event: dict):
    return orchestrator.handle_workday_event(event)

@router.post("/termination")
async def termination(event: dict):
    return orchestrator.handle_workday_event(event)

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(contents)

    return orchestrator.process_csv(temp_path)
