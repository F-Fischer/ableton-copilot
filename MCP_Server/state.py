import json
import os
from typing import Any, Dict

from . import music_theory


PROJECT_STATE_PATH = os.path.join(os.path.dirname(__file__), "project_key.json")


def _load_project_state() -> Dict[str, Any]:
    try:
        with open(PROJECT_STATE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {"tonic": None, "mode": None, "tempo": None, "genre": None}


def save_project_state(state: Dict[str, Any]) -> None:
    with open(PROJECT_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


PROJECT = _load_project_state()


def project_key_payload() -> Dict[str, Any]:
    result = dict(PROJECT)
    if PROJECT.get("tonic") and PROJECT.get("mode"):
        result["scale_pitch_classes"] = sorted(
            music_theory.scale_pitch_classes(PROJECT["tonic"], PROJECT["mode"])
        )
    return result
