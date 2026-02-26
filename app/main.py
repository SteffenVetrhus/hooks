"""
FastAPI application entry point.

Creates the FastAPI app instance, registers the members and organizations
routers, and exposes a health-check endpoint at the root path.
"""

from fastapi import FastAPI

from app.organizations_routes import router as organizations_router
from app.routes import router as members_router

app = FastAPI(
    title="Members & Organizations API",
    description="CRUD service for the PocketBase members and organizations collections",
    version="1.0.0",
)

# Register the members CRUD router
app.include_router(members_router, prefix="/api")

# Register the organizations CRUD router
app.include_router(organizations_router, prefix="/api")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health-check endpoint.

    Returns a simple JSON payload indicating the service is running.
    Useful for container orchestrators and load-balancer probes.

    Returns:
        dict[str, str]: ``{"status": "healthy"}``.

    Side Effects:
        None.
    """
    return {"status": "healthy"}
