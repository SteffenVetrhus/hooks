"""
FastAPI router defining the logo generation endpoint.

Generates SVG (and optionally PNG) logos on-the-fly from a brand name and
primary colour.  Purely stateless – no PocketBase persistence.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from app.logo_generator import generate_logo
from app.logo_schemas import LogoRequest

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/logos", tags=["logos"])


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/generate")
async def generate_logo_endpoint(req: LogoRequest) -> Response:
    """
    Generate a logo for the given brand name and colour.

    The logo style is deterministically chosen based on a hash of the name,
    so repeated calls with the same inputs always produce the same logo.
    The response body is the raw image data (SVG or PNG).

    Args:
        req: Validated ``LogoRequest`` containing the brand name, colour,
            desired output format, and canvas size.

    Returns:
        Response: The generated logo with an appropriate ``Content-Type``
        header (``image/svg+xml`` or ``image/png``).

    Raises:
        HTTPException: 500 if PNG conversion fails (e.g. ``cairosvg`` or
            its system dependency ``libcairo2`` is not installed).

    Side Effects:
        None (stateless generation).
    """
    # Generate the SVG content
    svg_content = generate_logo(req.name, req.color, req.size)

    # Build a filesystem-safe filename from the brand name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in req.name)[:50]

    if req.format == "svg":
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={
                "Content-Disposition": f'inline; filename="logo-{safe_name}.svg"',
            },
        )

    # PNG conversion – import cairosvg lazily so SVG-only usage works without cairo
    try:
        import cairosvg  # noqa: F811
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail=(
                "PNG conversion requires the 'cairosvg' package and its "
                "system dependency 'libcairo2'. Install with: "
                "pip install cairosvg && apt install libcairo2-dev"
            ),
        )

    try:
        png_bytes: bytes = cairosvg.svg2png(
            bytestring=svg_content.encode("utf-8"),
            output_width=req.size,
            output_height=req.size,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PNG conversion failed: {exc}",
        )

    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": f'inline; filename="logo-{safe_name}.png"',
        },
    )
