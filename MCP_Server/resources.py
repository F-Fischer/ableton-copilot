import json
import logging
from typing import Any, Dict

from . import music_theory
from .connection import get_ableton_connection
from .state import project_key_payload


logger = logging.getLogger("AbletonMCPServer")


def _json_resource(payload: Dict[str, Any]) -> str:
    """Return a stable JSON string for MCP resources."""
    return json.dumps(payload, indent=2, sort_keys=True)


def _resource_error(message: str) -> str:
    return _json_resource({"status": "error", "message": message})


def _genre_payload() -> Dict[str, Any]:
    return {
        "genres": music_theory.GENRES,
        "modes": sorted(music_theory.SCALES.keys()),
        "tonics": sorted(music_theory.NOTE_NAMES.keys()),
        "default_progressions": music_theory.DEFAULT_PROGRESSIONS,
        "default_structure": music_theory.DEFAULT_STRUCTURE,
        "drum_pitches": music_theory.DRUM_PITCHES,
        "sound_presets": {
            name: {"device": preset.get("device"), "parameters": sorted(preset.get("params", {}).keys())}
            for name, preset in music_theory.SOUND_PRESETS.items()
        },
    }


def _browser_favorites_payload() -> Dict[str, Any]:
    favorites = []
    for genre, definition in music_theory.GENRES.items():
        for role in ("chord_instrument", "bass_instrument", "drum_rack", "pad_instrument"):
            uri = definition.get(role)
            if uri:
                favorites.append({"genre": genre, "role": role, "uri": uri})

    return {
        "favorites": favorites,
        "notes": [
            "Use get_browser_tree and get_browser_items_at_path to discover more browser URIs.",
            "Use load_instrument_or_effect once a specific URI is known.",
            "This resource is intentionally curated and may be empty until more known-good URIs are added.",
        ],
    }


TOOL_GUIDE = """# Ableton Copilot Tool Guide

Recommended workflow:
1. Start with get_session_info and get_project_key.
2. For composition, call set_project_key before generators.
3. Use scaffold_track for a first arrangement pass, then inspect tracks/clips.
4. Use browser tools to discover and load instruments or effects by URI.
5. Use get_device_parameters before setting device parameters.
6. Prefer Arrangement View tools for full songs and Session View tools for loop sketching.

Read-only tools/resources should be used before mutating tools when the current set is unknown.
Destructive tools include delete_track, delete_clip, and delete_device.
"""


def register_resources(mcp) -> None:
    @mcp.resource(
        "ableton://session/current",
        name="Current Ableton Session",
        description="Read-only snapshot of the current Ableton Live session.",
        mime_type="application/json",
    )
    def current_session_resource() -> str:
        try:
            ableton = get_ableton_connection()
            return _json_resource({"status": "ok", "session": ableton.send_command("get_session_info")})
        except Exception as e:
            logger.error(f"Error reading current session resource: {str(e)}")
            return _resource_error(f"Could not read Ableton session: {str(e)}")

    @mcp.resource(
        "ableton://project/key",
        name="Project Key",
        description="Saved key, mode, tempo, genre, and scale pitch classes.",
        mime_type="application/json",
    )
    def project_key_resource() -> str:
        try:
            return _json_resource({"status": "ok", "project": project_key_payload()})
        except Exception as e:
            logger.error(f"Error reading project key resource: {str(e)}")
            return _resource_error(f"Could not read project key: {str(e)}")

    @mcp.resource(
        "ableton://genres",
        name="Supported Genres",
        description="Supported genres, modes, drum mappings, default progressions, and sound presets.",
        mime_type="application/json",
    )
    def genres_resource() -> str:
        return _json_resource({"status": "ok", **_genre_payload()})

    @mcp.resource(
        "ableton://browser/favorites",
        name="Browser Favorites",
        description="Curated browser URI hints for known-good instruments, racks, and effects.",
        mime_type="application/json",
    )
    def browser_favorites_resource() -> str:
        return _json_resource({"status": "ok", **_browser_favorites_payload()})

    @mcp.resource(
        "ableton://tool-guide",
        name="Tool Guide",
        description="Workflow guidance for choosing Ableton Copilot tools safely.",
        mime_type="text/markdown",
    )
    def tool_guide_resource() -> str:
        return TOOL_GUIDE
