# api/api_server.py

from fastapi import FastAPI
from api.endpoint_hr import router as hr_router
from api.endpoint_scim import router as scim_router
from api.endpoint_graph import router as graph_router

app = FastAPI(
    title="IAM Automation API",
    description="API backend for IAM Automation Platform",
    version="1.0.0"
)

# Register routers
app.include_router(hr_router, prefix="/hr", tags=["HR Events"])
app.include_router(scim_router, prefix="/scim", tags=["SCIM"])
app.include_router(graph_router, prefix="/graph", tags=["Graph Operations"])

@app.get("/")
def root():
    return {"status": "ok", "message": "IAM Automation API is running"}
