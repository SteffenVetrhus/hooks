"""
FastAPI router defining CRUD endpoints for the ``members`` collection.

Each endpoint delegates to the corresponding function in
:mod:`app.pocketbase_client` and translates PocketBase HTTP errors into
appropriate FastAPI HTTP exceptions.
"""

from __future__ import annotations

from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.pocketbase_client import (
    create_member,
    delete_member,
    get_member,
    list_members,
    update_member,
)
from app.schemas import MemberCreate, MemberListResponse, MemberResponse, MemberUpdate

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/members", tags=["members"])


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


@router.get("/", response_model=MemberListResponse)
async def list_members_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: Optional[str] = Query(None, description="PocketBase sort expression, e.g. '-created'"),
    filter: Optional[str] = Query(None, alias="filter", description="PocketBase filter expression"),
) -> MemberListResponse:
    """
    List members with pagination, sorting, and filtering.

    Delegates to :func:`app.pocketbase_client.list_members` and returns the
    paginated result set.

    Args:
        page: The page number to retrieve.  Must be >= 1.
        per_page: Number of records per page (1–100).
        sort: Optional PocketBase sort string (prefix with ``-`` for descending).
        filter: Optional PocketBase filter expression.

    Returns:
        MemberListResponse: A paginated list of member records.

    Raises:
        HTTPException: If PocketBase returns an error.
    """
    try:
        data = await list_members(
            page=page, per_page=per_page, sort=sort, filter_query=filter
        )
        return MemberListResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.get("/{member_id}", response_model=MemberResponse)
async def get_member_endpoint(member_id: str) -> MemberResponse:
    """
    Retrieve a single member by ID.

    Args:
        member_id: The PocketBase record ID of the member to retrieve.

    Returns:
        MemberResponse: The member record.

    Raises:
        HTTPException: 404 if the member is not found, or another status code
            for unexpected PocketBase errors.
    """
    try:
        data = await get_member(member_id)
        return MemberResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.post("/", response_model=MemberResponse, status_code=201)
async def create_member_endpoint(member: MemberCreate) -> MemberResponse:
    """
    Create a new member.

    Accepts a JSON body conforming to :class:`app.schemas.MemberCreate` and
    forwards it to PocketBase.

    Args:
        member: The validated member creation payload.

    Returns:
        MemberResponse: The newly created member record (HTTP 201).

    Raises:
        HTTPException: 400 if PocketBase validation fails, or another status
            code for unexpected errors.
    """
    try:
        # Serialize the Pydantic model to a dict, excluding unset optional fields
        data = await create_member(member.model_dump(exclude_none=True))
        return MemberResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.patch("/{member_id}", response_model=MemberResponse)
async def update_member_endpoint(
    member_id: str, member: MemberUpdate
) -> MemberResponse:
    """
    Update an existing member (partial update / PATCH semantics).

    Only fields present in the request body are updated; omitted fields
    remain unchanged.

    Args:
        member_id: The PocketBase record ID of the member to update.
        member: The validated partial-update payload.

    Returns:
        MemberResponse: The updated member record.

    Raises:
        HTTPException: 404 if the member is not found, 400 for validation
            errors, or another status code for unexpected errors.
    """
    try:
        # Only send fields that were explicitly provided in the request
        payload = member.model_dump(exclude_none=True)
        data = await update_member(member_id, payload)
        return MemberResponse(**data)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)


@router.delete("/{member_id}", status_code=204)
async def delete_member_endpoint(member_id: str) -> None:
    """
    Delete a member by ID.

    Args:
        member_id: The PocketBase record ID of the member to delete.

    Returns:
        None (HTTP 204 No Content on success).

    Raises:
        HTTPException: 404 if the member is not found, or another status code
            for unexpected errors.
    """
    try:
        await delete_member(member_id)
    except httpx.HTTPStatusError as exc:
        raise _handle_pocketbase_error(exc)
