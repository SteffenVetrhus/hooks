"""
Pydantic schemas for the organizations collection.

Defines request and response models used by the FastAPI endpoints to validate
incoming data and serialise outgoing responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    """
    Schema for creating a new organization.

    Attributes:
        name: Name of the organization.
        description: Optional description providing details about the organization.
        website: Optional website URL for the organization.
        email: Optional contact email address for the organization.
        phone: Optional contact phone number.
        address: Optional physical address of the organization.
        active: Whether the organization is currently active.  Defaults to True.
    """

    name: str = Field(
        ..., min_length=1, max_length=255, description="Name of the organization"
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Description of the organization"
    )
    website: Optional[str] = Field(
        None, max_length=500, description="Website URL of the organization"
    )
    email: Optional[str] = Field(
        None, max_length=255, description="Contact email address"
    )
    phone: Optional[str] = Field(
        None, max_length=50, description="Contact phone number"
    )
    address: Optional[str] = Field(
        None, max_length=500, description="Physical address"
    )
    active: bool = Field(True, description="Whether the organization is active")


class OrganizationUpdate(BaseModel):
    """
    Schema for updating an existing organization.

    All fields are optional so that partial updates (PATCH semantics) are
    supported.

    Attributes:
        name: Updated organization name.
        description: Updated description.
        website: Updated website URL.
        email: Updated contact email address.
        phone: Updated contact phone number.
        address: Updated physical address.
        active: Updated active status.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Name of the organization"
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Description of the organization"
    )
    website: Optional[str] = Field(
        None, max_length=500, description="Website URL of the organization"
    )
    email: Optional[str] = Field(
        None, max_length=255, description="Contact email address"
    )
    phone: Optional[str] = Field(
        None, max_length=50, description="Contact phone number"
    )
    address: Optional[str] = Field(
        None, max_length=500, description="Physical address"
    )
    active: Optional[bool] = Field(
        None, description="Whether the organization is active"
    )


class OrganizationResponse(BaseModel):
    """
    Schema representing an organization record returned from PocketBase.

    Includes all user-defined fields plus the auto-generated PocketBase
    metadata.

    Attributes:
        id: PocketBase record ID.
        collection_id: ID of the PocketBase collection this record belongs to.
        collection_name: Name of the PocketBase collection.
        name: Name of the organization.
        description: Optional description of the organization.
        website: Optional website URL.
        email: Optional contact email address.
        phone: Optional contact phone number.
        address: Optional physical address.
        active: Whether the organization is active.
        created: Timestamp when the record was created.
        updated: Timestamp when the record was last updated.
    """

    id: str
    collection_id: str = Field(default="", alias="collectionId")
    collection_name: str = Field(default="", alias="collectionName")
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class OrganizationListResponse(BaseModel):
    """
    Paginated list response returned by PocketBase for collection queries.

    Attributes:
        page: Current page number (1-indexed).
        per_page: Number of items per page.
        total_items: Total number of matching records.
        total_pages: Total number of pages.
        items: List of organization records for the current page.
    """

    page: int = Field(..., alias="page")
    per_page: int = Field(..., alias="perPage")
    total_items: int = Field(..., alias="totalItems")
    total_pages: int = Field(..., alias="totalPages")
    items: list[OrganizationResponse]

    model_config = {"populate_by_name": True}
