"""
Programmatic SVG logo generator.

Generates simple, beautiful logos from a brand name and primary colour.
Five distinct visual styles are available; the style is chosen deterministically
from a hash of the name so the same input always produces the same logo.

No external services or AI APIs are used – logos are built entirely from
SVG primitives (shapes, text, gradients).
"""

from __future__ import annotations

import hashlib
import math


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------


def _parse_hex(hex_color: str) -> tuple[int, int, int]:
    """
    Parse a ``#RRGGBB`` hex string into an (r, g, b) tuple.

    Args:
        hex_color: A 7-character hex colour string (e.g. ``#3B82F6``).

    Returns:
        tuple[int, int, int]: Red, green, and blue channel values (0–255).

    Side Effects:
        None.
    """
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _to_hex(r: int, g: int, b: int) -> str:
    """
    Convert (r, g, b) integers into a ``#RRGGBB`` hex string.

    Args:
        r: Red channel (0–255).
        g: Green channel (0–255).
        b: Blue channel (0–255).

    Returns:
        str: The hex colour string.

    Side Effects:
        None.
    """
    return f"#{min(255, max(0, r)):02X}{min(255, max(0, g)):02X}{min(255, max(0, b)):02X}"


def _darken(hex_color: str, factor: float = 0.35) -> str:
    """
    Darken a hex colour by blending it toward black.

    Args:
        hex_color: The original ``#RRGGBB`` colour.
        factor: Blend factor – 0.0 returns the original, 1.0 returns black.

    Returns:
        str: The darkened hex colour.

    Side Effects:
        None.
    """
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        int(r * (1 - factor)),
        int(g * (1 - factor)),
        int(b * (1 - factor)),
    )


def _lighten(hex_color: str, factor: float = 0.45) -> str:
    """
    Lighten a hex colour by blending it toward white.

    Args:
        hex_color: The original ``#RRGGBB`` colour.
        factor: Blend factor – 0.0 returns the original, 1.0 returns white.

    Returns:
        str: The lightened hex colour.

    Side Effects:
        None.
    """
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        int(r + (255 - r) * factor),
        int(g + (255 - g) * factor),
        int(b + (255 - b) * factor),
    )


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def _extract_initials(name: str) -> str:
    """
    Extract up to two uppercase initials from a brand name.

    If the name contains multiple words the first letter of the first two
    words is used.  For a single word the first one or two characters are
    returned.

    Args:
        name: The brand / company name.

    Returns:
        str: One or two uppercase letters.

    Side Effects:
        None.
    """
    words = name.split()
    if len(words) >= 2:
        # First letter of the first two words
        return (words[0][0] + words[1][0]).upper()
    # Single word – take up to two characters
    return name[:2].upper() if len(name) >= 2 else name[0].upper()


# ---------------------------------------------------------------------------
# Style selector
# ---------------------------------------------------------------------------


def _select_style(name: str) -> int:
    """
    Deterministically select a logo style index (0–4) from the brand name.

    Uses an MD5 hash so the same name always maps to the same style.

    Args:
        name: The brand name.

    Returns:
        int: An index from 0 to 4 inclusive.

    Side Effects:
        None.
    """
    digest = hashlib.md5(name.encode()).hexdigest()
    return int(digest, 16) % 5


# ---------------------------------------------------------------------------
# SVG wrapper
# ---------------------------------------------------------------------------


def _svg_wrap(size: int, body: str) -> str:
    """
    Wrap inner SVG elements in a complete SVG document.

    Args:
        size: The width/height for the ``viewBox``.
        body: Raw SVG element markup to place inside the ``<svg>`` tag.

    Returns:
        str: A complete SVG document string.

    Side Effects:
        None.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
        f"{body}"
        f"</svg>"
    )


# ---------------------------------------------------------------------------
# Style 0 – Circle Monogram
# ---------------------------------------------------------------------------


def _generate_circle_monogram(
    name: str, color: str, size: int
) -> str:
    """
    Generate a filled-circle monogram logo.

    A large coloured circle sits at the centre-top of the canvas with the
    brand initials inside, and the full brand name is rendered below.

    Args:
        name: Brand name.
        color: Primary hex colour.
        size: Canvas size in pixels.

    Returns:
        str: Complete SVG string.

    Side Effects:
        None.
    """
    initials = _extract_initials(name)
    light = _lighten(color, 0.85)
    dark = _darken(color, 0.50)
    cx = size / 2
    # Circle centre placed in the upper portion of the canvas
    cy = size * 0.40
    r = size * 0.26

    # Font sizes scale with the canvas
    initials_font = size * 0.22
    name_font = size * 0.065

    body = (
        # Soft background rectangle
        f'<rect width="{size}" height="{size}" rx="{size * 0.04}" fill="{light}"/>'
        # Main circle
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
        # Initials text – white, bold, centred on the circle
        f'<text x="{cx}" y="{cy}" dy="0.35em" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="700" font-size="{initials_font}" fill="#FFFFFF" '
        f'letter-spacing="2">{initials}</text>'
        # Brand name below the circle
        f'<text x="{cx}" y="{size * 0.78}" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="600" font-size="{name_font}" fill="{dark}" '
        f'letter-spacing="3">{name.upper()}</text>'
    )
    return _svg_wrap(size, body)


# ---------------------------------------------------------------------------
# Style 1 – Rounded Square Badge
# ---------------------------------------------------------------------------


def _generate_rounded_square(
    name: str, color: str, size: int
) -> str:
    """
    Generate a rounded-square badge logo.

    A large rounded rectangle with the initials inside and the brand name
    sitting beneath it.

    Args:
        name: Brand name.
        color: Primary hex colour.
        size: Canvas size in pixels.

    Returns:
        str: Complete SVG string.

    Side Effects:
        None.
    """
    initials = _extract_initials(name)
    light = _lighten(color, 0.85)
    dark = _darken(color, 0.50)

    # Badge dimensions
    badge_size = size * 0.44
    badge_x = (size - badge_size) / 2
    badge_y = size * 0.16
    badge_rx = badge_size * 0.22

    initials_font = size * 0.18
    name_font = size * 0.065

    body = (
        # Background
        f'<rect width="{size}" height="{size}" rx="{size * 0.04}" fill="{light}"/>'
        # Rounded square badge
        f'<rect x="{badge_x}" y="{badge_y}" width="{badge_size}" '
        f'height="{badge_size}" rx="{badge_rx}" fill="{color}"/>'
        # Initials
        f'<text x="{size / 2}" y="{badge_y + badge_size / 2}" dy="0.35em" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="700" font-size="{initials_font}" fill="#FFFFFF" '
        f'letter-spacing="2">{initials}</text>'
        # Brand name
        f'<text x="{size / 2}" y="{badge_y + badge_size + size * 0.12}" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="600" font-size="{name_font}" fill="{dark}" '
        f'letter-spacing="3">{name.upper()}</text>'
    )
    return _svg_wrap(size, body)


# ---------------------------------------------------------------------------
# Style 2 – Hexagon Mark
# ---------------------------------------------------------------------------


def _generate_hexagon(
    name: str, color: str, size: int
) -> str:
    """
    Generate a hexagon-mark logo.

    A regular hexagon filled with the primary colour, containing the first
    letter of the brand, with the full name rendered below.

    Args:
        name: Brand name.
        color: Primary hex colour.
        size: Canvas size in pixels.

    Returns:
        str: Complete SVG string.

    Side Effects:
        None.
    """
    light = _lighten(color, 0.85)
    dark = _darken(color, 0.50)
    accent = _lighten(color, 0.35)

    cx = size / 2
    cy = size * 0.40
    r = size * 0.27  # "radius" of the hexagon

    # Build hexagon points (flat-top orientation)
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append(f"{px:.1f},{py:.1f}")
    points_str = " ".join(points)

    letter_font = size * 0.24
    name_font = size * 0.06

    body = (
        # Background
        f'<rect width="{size}" height="{size}" rx="{size * 0.04}" fill="{light}"/>'
        # Subtle smaller hexagon accent (rotated slightly via offset)
        f'<polygon points="{points_str}" fill="{accent}" '
        f'transform="translate(0, {size * 0.015}) scale(1.06)" '
        f'transform-origin="{cx} {cy}" opacity="0.3"/>'
        # Main hexagon
        f'<polygon points="{points_str}" fill="{color}"/>'
        # First letter centred
        f'<text x="{cx}" y="{cy}" dy="0.36em" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="700" font-size="{letter_font}" fill="#FFFFFF">'
        f'{name[0].upper()}</text>'
        # Brand name
        f'<text x="{cx}" y="{size * 0.80}" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="600" font-size="{name_font}" fill="{dark}" '
        f'letter-spacing="3">{name.upper()}</text>'
    )
    return _svg_wrap(size, body)


# ---------------------------------------------------------------------------
# Style 3 – Stacked Bars
# ---------------------------------------------------------------------------


def _generate_stacked_bars(
    name: str, color: str, size: int
) -> str:
    """
    Generate a stacked-bars logo.

    Two or three horizontal bars of varying width (derived from name
    characters) are drawn above the brand name, creating an abstract
    geometric mark.

    Args:
        name: Brand name.
        color: Primary hex colour.
        size: Canvas size in pixels.

    Returns:
        str: Complete SVG string.

    Side Effects:
        None.
    """
    light = _lighten(color, 0.85)
    dark = _darken(color, 0.50)
    mid = _lighten(color, 0.25)

    # Derive bar widths from name characters for deterministic variety
    chars = [ord(c) for c in name[:3].ljust(3)]
    # Normalise character codes to a 0.45–0.90 range to keep bars visually balanced
    widths = [0.45 + (c % 46) / 100 for c in chars]

    bar_height = size * 0.065
    gap = size * 0.03
    bar_colors = [color, mid, _lighten(color, 0.50)]

    # Start bars from upper portion of canvas
    start_y = size * 0.22
    bar_elements = ""
    for i, w in enumerate(widths):
        bar_w = size * w
        bar_x = (size - bar_w) / 2
        bar_y = start_y + i * (bar_height + gap)
        bar_rx = bar_height / 2  # Fully rounded ends
        bar_elements += (
            f'<rect x="{bar_x:.1f}" y="{bar_y:.1f}" '
            f'width="{bar_w:.1f}" height="{bar_height:.1f}" '
            f'rx="{bar_rx:.1f}" fill="{bar_colors[i]}"/>'
        )

    name_font = size * 0.075
    name_y = start_y + 3 * (bar_height + gap) + size * 0.14

    body = (
        # Background
        f'<rect width="{size}" height="{size}" rx="{size * 0.04}" fill="{light}"/>'
        # Bars
        f"{bar_elements}"
        # Brand name
        f'<text x="{size / 2}" y="{name_y:.1f}" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="700" font-size="{name_font}" fill="{dark}" '
        f'letter-spacing="4">{name.upper()}</text>'
    )
    return _svg_wrap(size, body)


# ---------------------------------------------------------------------------
# Style 4 – Circle Outline + Dot
# ---------------------------------------------------------------------------


def _generate_circle_outline(
    name: str, color: str, size: int
) -> str:
    """
    Generate a circle-outline-with-dot logo.

    A thin circle outline with a small coloured accent dot at the top-right,
    the brand initials centred inside, and the name below.

    Args:
        name: Brand name.
        color: Primary hex colour.
        size: Canvas size in pixels.

    Returns:
        str: Complete SVG string.

    Side Effects:
        None.
    """
    initials = _extract_initials(name)
    light = _lighten(color, 0.85)
    dark = _darken(color, 0.50)

    cx = size / 2
    cy = size * 0.40
    r = size * 0.24
    stroke_w = size * 0.018

    # Accent dot position – top-right of the circle
    dot_angle = math.radians(-45)
    dot_x = cx + r * math.cos(dot_angle)
    dot_y = cy + r * math.sin(dot_angle)
    dot_r = size * 0.04

    initials_font = size * 0.17
    name_font = size * 0.06

    body = (
        # Background
        f'<rect width="{size}" height="{size}" rx="{size * 0.04}" fill="{light}"/>'
        # Thin circle outline
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="{color}" stroke-width="{stroke_w}"/>'
        # Accent dot
        f'<circle cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="{dot_r}" fill="{color}"/>'
        # Initials
        f'<text x="{cx}" y="{cy}" dy="0.35em" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="600" font-size="{initials_font}" fill="{dark}" '
        f'letter-spacing="2">{initials}</text>'
        # Brand name
        f'<text x="{cx}" y="{size * 0.78}" '
        f'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-weight="600" font-size="{name_font}" fill="{dark}" '
        f'letter-spacing="3">{name.upper()}</text>'
    )
    return _svg_wrap(size, body)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

# Ordered list of generator functions – index matches _select_style output
_STYLES = [
    _generate_circle_monogram,
    _generate_rounded_square,
    _generate_hexagon,
    _generate_stacked_bars,
    _generate_circle_outline,
]


def generate_logo(name: str, color: str, size: int = 400) -> str:
    """
    Generate a complete SVG logo for the given brand name and colour.

    A logo style is selected deterministically from the name so that repeated
    calls with identical inputs always return the same result.

    Args:
        name: The brand or company name to render.
        color: Primary ``#RRGGBB`` hex colour.
        size: Canvas width and height in pixels (default 400).

    Returns:
        str: A complete SVG document string.

    Side Effects:
        None.
    """
    style_index = _select_style(name)
    generator = _STYLES[style_index]
    return generator(name, color, size)
