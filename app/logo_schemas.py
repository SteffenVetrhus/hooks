"""
Pydantic schemas for the logo generation service.

Defines the request model used by the logo generation endpoint to validate
incoming data.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator


class LogoRequest(BaseModel):
    """
    Schema for requesting a generated logo.

    Attributes:
        name: The brand or company name to render in the logo.
        color: Primary hex colour string (e.g. ``#3B82F6``).
        format: Desired output format – ``"svg"`` (default) or ``"png"``.
        size: Canvas size in pixels for the SVG viewBox and PNG output.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Brand or company name (1–50 characters)",
    )
    color: str = Field(
        ...,
        description="Primary hex colour, e.g. '#3B82F6'",
    )
    format: str = Field(
        "svg",
        description="Output format: 'svg' or 'png'",
    )
    size: int = Field(
        400,
        ge=200,
        le=1024,
        description="Canvas size in pixels (200–1024)",
    )

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        """
        Ensure the colour value is a valid 6-digit hex string prefixed with ``#``.

        Args:
            v: The raw colour string from the request.

        Returns:
            str: The validated (uppercased) hex colour.

        Raises:
            ValueError: If the string does not match the ``#RRGGBB`` pattern.
        """
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
            raise ValueError("color must be a valid hex colour like '#3B82F6'")
        return v.upper()

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """
        Ensure the requested format is one of the supported types.

        Args:
            v: The raw format string from the request.

        Returns:
            str: The validated lowercase format.

        Raises:
            ValueError: If the format is not ``svg`` or ``png``.
        """
        v = v.lower()
        if v not in ("svg", "png"):
            raise ValueError("format must be 'svg' or 'png'")
        return v
