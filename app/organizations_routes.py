"""
FastAPI router defining CRUD endpoints for the ``organizations`` collection.

Each endpoint delegates to the corresponding function in
:mod:`app.organizations_client` and translates PocketBase HTTP errors into
appropriate FastAPI HTTP exceptions.
"""

from __future__ import annotations

from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.organizations_client import (
    create_organization,
    delete_organization,
    get_organization,
    list_organizations,
    update_organization,
)
from app.organizations_schemas import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationUpdate,
)

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/organizations", tags=["organizations"])


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _handle_pocketbase_error(exc: httpx.HTTPStatusError) -> HTTPException:
    """
    Convert an ``httpx.HTTPStatusError`` from PocketBase into a FastAPI
    ``HTTPException`` with an appropriate status code and detail message.

    Args:
        exc: The HTTP status error raised by the PocketBase client.

    Returns:
        HTTPException: A FastAPI exception ready to be raised.

    Side Effects:
        None.
    """
    # Attempt to extract a human-readable message from PocketBase's JSON body
    try:
        detail = exc.response.json()
    except Exception:
        detail = exc.response.text

    return HTTPException(status_code=exc.response.status_code, detail=detail)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/", response_model=OrganizationListResponse)
async def list_organizations_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: Optional[str] = Query(
        None, description="PocketBase sort expression, e.g. '-created'"
    ),
    filter: Optional[str] = Query(
        None, alias="filter", description="PocketBase filter expression"
    ),
) -> OrganizationListResponse:
    """
    List organizations with pagination, sorting, and filtering.

    Delegates to :func:`app.organizations_client.list_organizations` and
    returns the paginated result set.

    Args:
        page: The page number to retrieve.  Must be >= 1.
        per_page: Number of records per page (1-100).
        sort: Optional PocketBase sort string (prefix with ``-`` for
              descending).
        filter: Optional PocketBase filter expression.

    Returns:
        OrganizationListResponse: A paginated list of organization records.

    Raises:
        HTTPException: If PocketBase returns an error.
    """
    try:
        data = await list_organizations(
            page=page, per_page=per_page, sort=sort, filter_query=filter
        )
        return OrganizationListResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization_endpoint(
    organization_id: str,
) -> OrganizationResponse:
    """
    Retrieve a single organization by ID.

    Args:
        organization_id: The PocketBase record ID of the organization to
                         retrieve.

    Returns:
        OrganizationResponse: The organization record.

    Raises:
        HTTPException: 404 if the organization is not found, or another
            status code for unexpected PocketBase errors.
    """
    try:
        data = await get_organization(organization_id)
        return OrganizationResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.post("/", response_model=OrganizationResponse, status_code=201)
async def create_organization_endpoint(
    organization: OrganizationCreate,
) -> OrganizationResponse:
    """
    Create a new organization.

    Accepts a JSON body conforming to
    :class:`app.organizations_schemas.OrganizationCreate` and forwards it to
    PocketBase.

    Args:
        organization: The validated organization creation payload.

    Returns:
        OrganizationResponse: The newly created organization record (HTTP 201).

    Raises:
        HTTPException: 400 if PocketBase validation fails, or another status
            code for unexpected errors.
    """
    try:
        # Serialize the Pydantic model to a dict, excluding unset optional fields
        data = await create_organization(
            organization.model_dump(exclude_none=True)
        )
        return OrganizationResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization_endpoint(
    organization_id: str, organization: OrganizationUpdate
) -> OrganizationResponse:
    """
    Update an existing organization (partial update / PATCH semantics).

    Only fields present in the request body are updated; omitted fields
    remain unchanged.

    Args:
        organization_id: The PocketBase record ID of the organization to
                         update.
        organization: The validated partial-update payload.

    Returns:
        OrganizationResponse: The updated organization record.

    Raises:
        HTTPException: 404 if the organization is not found, 400 for
            validation errors, or another status code for unexpected errors.
    """
    try:
        # Only send fields that were explicitly provided in the request
        payload = organization.model_dump(exclude_none=True)
        data = await update_organization(organization_id, payload)
        return OrganizationResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.delete("/{organization_id}", status_code=204)
async def delete_organization_endpoint(organization_id: str) -> None:
    """
    Delete an organization by ID.

    Args:
        organization_id: The PocketBase record ID of the organization to
                         delete.

    Returns:
        None (HTTP 204 No Content on success).

    Raises:
        HTTPException: 404 if the organization is not found, or another
            status code for unexpected errors.
    """
    try:
        await delete_organization(organization_id)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)
