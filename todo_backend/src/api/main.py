from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.db import init_db
from src.api.routers_tasks import router as tasks_router

app = FastAPI(
    title="Todo Backend",
    description="A simple FastAPI backend for managing todo tasks with SQLite persistence.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness"},
        {"name": "Tasks", "description": "CRUD operations for tasks"},
    ],
)

# Enable permissive CORS for development and integration with potential frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this appropriately.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize database on FastAPI application startup.

    This hook ensures that the SQLite database and required tables are present
    before the API begins handling requests. It calls src.api.db.init_db(),
    which creates the 'tasks' table if it does not already exist.

    No parameters.
    Returns: None
    """
    init_db()


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """
    Health check endpoint.

    Returns a simple JSON payload indicating the service is healthy.
    Useful for readiness/liveness probes.

    Returns:
        dict: {"message": "Healthy"}
    """
    return {"message": "Healthy"}


# Register routers
app.include_router(tasks_router)
