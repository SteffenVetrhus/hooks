"""
Pydantic schemas for the members collection.

Defines request and response models used by the FastAPI endpoints to validate
incoming data and serialise outgoing responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MemberCreate(BaseModel):
    """
    Schema for creating a new member.

    Attributes:
        name: Full name of the member.
        email: Email address of the member.  Must be unique within the collection.
        phone: Optional phone number.
        active: Whether the member is currently active.  Defaults to True.
    """

    name: str = Field(..., min_length=1, max_length=255, description="Full name of the member")
    email: str = Field(..., min_length=1, max_length=255, description="Email address of the member")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    active: bool = Field(True, description="Whether the member is active")


class MemberUpdate(BaseModel):
    """
    Schema for updating an existing member.

    All fields are optional so that partial updates (PATCH semantics) are supported.

    Attributes:
        name: Updated full name.
        email: Updated email address.
        phone: Updated phone number.
        active: Updated active status.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name of the member")
    email: Optional[str] = Field(None, min_length=1, max_length=255, description="Email address of the member")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    active: Optional[bool] = Field(None, description="Whether the member is active")


class MemberResponse(BaseModel):
    """
    Schema representing a member record returned from PocketBase.

    Includes all user-defined fields plus the auto-generated PocketBase metadata.

    Attributes:
        id: PocketBase record ID.
        collection_id: ID of the PocketBase collection this record belongs to.
        collection_name: Name of the PocketBase collection.
        name: Full name of the member.
        email: Email address of the member.
        phone: Optional phone number.
        active: Whether the member is active.
        created: Timestamp when the record was created.
        updated: Timestamp when the record was last updated.
    """

    id: str
    collection_id: str = Field(default="", alias="collectionId")
    collection_name: str = Field(default="", alias="collectionName")
    name: str
    email: str
    phone: Optional[str] = None
    active: bool = True
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class MemberListResponse(BaseModel):
    """
    Paginated list response returned by PocketBase for collection queries.

    Attributes:
        page: Current page number (1-indexed).
        per_page: Number of items per page.
        total_items: Total number of matching records.
        total_pages: Total number of pages.
        items: List of member records for the current page.
    """

    page: int = Field(..., alias="page")
    per_page: int = Field(..., alias="perPage")
    total_items: int = Field(..., alias="totalItems")
    total_pages: int = Field(..., alias="totalPages")
    items: list[MemberResponse]

    model_config = {"populate_by_name": True}
