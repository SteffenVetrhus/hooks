"""
Async HTTP client wrapper for the PocketBase REST API.

Provides methods that map directly to PocketBase's records REST endpoints for
the ``members`` collection.  Uses ``httpx.AsyncClient`` for non-blocking I/O
so that the FastAPI event-loop is never stalled by upstream requests.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

from app.config import settings


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# The PocketBase collection name this client targets.
COLLECTION_NAME = "members"

# Base URL for the records API, built once at module load time.
BASE_URL = f"{settings.pocketbase_url}/api/collections/{COLLECTION_NAME}/records"


# ---------------------------------------------------------------------------
# Client helpers
# ---------------------------------------------------------------------------


def _get_client() -> httpx.AsyncClient:
    """
    Create and return a new ``httpx.AsyncClient`` configured with a reasonable
    timeout.

    Returns:
        httpx.AsyncClient: A fresh async HTTP client instance.

    Side Effects:
        None.  The caller is responsible for closing the client (or using it
        inside an ``async with`` block).
    """
    return httpx.AsyncClient(timeout=30.0)


async def _authenticate(client: httpx.AsyncClient) -> dict[str, str]:
    """
    Authenticate with PocketBase as an admin and return an authorization header
    dictionary.

    If admin credentials are not configured the function returns an empty dict
    so that unauthenticated requests can still be made (useful when PocketBase
    API rules allow public access).

    Args:
        client: An active ``httpx.AsyncClient`` to use for the auth request.

    Returns:
        dict[str, str]: A dictionary containing the ``Authorization`` header,
        or an empty dict when no credentials are configured.

    Side Effects:
        Performs an HTTP POST to the PocketBase admin auth endpoint.
    """
    # Skip authentication when no credentials are provided
    if not settings.pocketbase_admin_email or not settings.pocketbase_admin_password:
        return {}

    # Authenticate via the admins auth-with-password endpoint
    auth_url = f"{settings.pocketbase_url}/api/admins/auth-with-password"
    response = await client.post(
        auth_url,
        json={
            "identity": settings.pocketbase_admin_email,
            "password": settings.pocketbase_admin_password,
        },
    )
    response.raise_for_status()

    # Extract the JWT token from the response body
    token = response.json().get("token", "")
    return {"Authorization": f"Bearer {token}"} if token else {}


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------


async def list_members(
    page: int = 1,
    per_page: int = 20,
    sort: Optional[str] = None,
    filter_query: Optional[str] = None,
) -> dict[str, Any]:
    """
    Retrieve a paginated list of members from PocketBase.

    Args:
        page: The page number to retrieve (1-indexed).  Defaults to 1.
        per_page: The number of records per page.  Defaults to 20.
        sort: Optional PocketBase sort expression (e.g. ``"-created"``).
        filter_query: Optional PocketBase filter expression
                      (e.g. ``'name ~ "John"'``).

    Returns:
        dict[str, Any]: The raw JSON response from PocketBase containing
        ``page``, ``perPage``, ``totalItems``, ``totalPages``, and ``items``.

    Raises:
        httpx.HTTPStatusError: If PocketBase returns a non-2xx status code.

    Side Effects:
        Performs an HTTP GET request to PocketBase.
    """
    async with _get_client() as client:
        headers = await _authenticate(client)

        # Build query parameters, omitting any that are None
        params: dict[str, Any] = {"page": page, "perPage": per_page}
        if sort:
            params["sort"] = sort
        if filter_query:
            params["filter"] = filter_query

        response = await client.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


async def get_member(member_id: str) -> dict[str, Any]:
    """
    Retrieve a single member record by its PocketBase ID.

    Args:
        member_id: The unique PocketBase record ID of the member.

    Returns:
        dict[str, Any]: The raw JSON object representing the member record.

    Raises:
        httpx.HTTPStatusError: If the record is not found (404) or another
            HTTP error occurs.

    Side Effects:
        Performs an HTTP GET request to PocketBase.
    """
    async with _get_client() as client:
        headers = await _authenticate(client)
        response = await client.get(f"{BASE_URL}/{member_id}", headers=headers)
        response.raise_for_status()
        return response.json()


async def create_member(data: dict[str, Any]) -> dict[str, Any]:
    """
    Create a new member record in PocketBase.

    Args:
        data: A dictionary of field values for the new member.  Must conform
              to the ``MemberCreate`` schema.

    Returns:
        dict[str, Any]: The newly created member record as returned by
        PocketBase (includes ``id``, ``created``, ``updated``, etc.).

    Raises:
        httpx.HTTPStatusError: If validation fails (400) or another HTTP
            error occurs.

    Side Effects:
        Creates a new record in the PocketBase ``members`` collection.
    """
    async with _get_client() as client:
        headers = await _authenticate(client)
        response = await client.post(BASE_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


async def update_member(member_id: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Update an existing member record in PocketBase using PATCH semantics.

    Only the fields present in *data* are updated; all other fields remain
    unchanged.

    Args:
        member_id: The unique PocketBase record ID of the member to update.
        data: A dictionary of field values to update.

    Returns:
        dict[str, Any]: The updated member record as returned by PocketBase.

    Raises:
        httpx.HTTPStatusError: If the record is not found (404), validation
            fails (400), or another HTTP error occurs.

    Side Effects:
        Modifies an existing record in the PocketBase ``members`` collection.
    """
    async with _get_client() as client:
        headers = await _authenticate(client)
        response = await client.patch(
            f"{BASE_URL}/{member_id}", json=data, headers=headers
        )
        response.raise_for_status()
        return response.json()


async def delete_member(member_id: str) -> None:
    """
    Delete a member record from PocketBase.

    Args:
        member_id: The unique PocketBase record ID of the member to delete.

    Returns:
        None

    Raises:
        httpx.HTTPStatusError: If the record is not found (404) or another
            HTTP error occurs.

    Side Effects:
        Permanently removes the record from the PocketBase ``members``
        collection.
    """
    async with _get_client() as client:
        headers = await _authenticate(client)
        response = await client.delete(
            f"{BASE_URL}/{member_id}", headers=headers
        )
        response.raise_for_status()
