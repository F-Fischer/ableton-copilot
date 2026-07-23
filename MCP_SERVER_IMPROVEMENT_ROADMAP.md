# MCP Server Improvement Roadmap

This document captures suggested next steps for improving Ableton Copilot from a raw Ableton control surface into a more complete music-production assistant.

## Plan Status

| Step | Area | Status |
| --- | --- | --- |
| 1 | Add MCP prompts and resources | Done |
| 2 | Add high-value tools | Pending |
| 3 | Improve composition generators | Pending |
| 4 | Improve sound design | Pending |
| 5 | Improve reliability and architecture | In progress |
| 6 | Improve documentation | Pending |

## 1. Add MCP Prompts

Status: Done

Prompts should guide the model through multi-step workflows instead of relying on it to infer tool order from individual tool descriptions.

Implemented prompts:

- `compose_track`: Collect genre, key, mood, and target length, then set project key, scaffold tracks, load instruments, generate parts, and summarize the result.
- `arrange_existing_loop`: Inspect existing clips, duplicate material into Arrangement View, create section markers, and vary density across intro, build, drop, breakdown, and outro.
- `mix_session`: Inspect tracks, set rough gain balance, pan, mute/solo as needed, configure sends, and return a mix summary.
- `sound_design_patch`: Load or inspect a device, list useful parameters, apply a preset, and make parameter tweaks from a sound description.
- `remix_clip`: Read MIDI notes from a clip, create variations, transpose or reharmonize, and write the result to a new clip.
- `debug_ableton_connection`: Walk users through checking the MCP server, Remote Script, port, Ableton control surface setup, and common timeout cases.

Example:

```python
@mcp.prompt()
def compose_track_prompt(
    genre: str,
    key: str = "",
    mood: str = "",
    length: str = "short",
) -> str:
    return f"""
Create a {length} Ableton arrangement in the style of {genre}.
Mood: {mood}
Preferred key: {key or "choose one"}

Workflow:
1. Inspect the session.
2. Set project key, tempo, and genre.
3. Scaffold section markers and core tracks.
4. Load appropriate instruments/effects.
5. Generate drums, bass, chords, and optional pad/fx.
6. Switch to Arrangement View.
7. Return a concise summary of tracks, sections, and manual follow-ups.
"""
```

## 2. Add MCP Resources

Status: Done

Resources should expose read-only context that clients can fetch without invoking a mutating tool.

Implemented resources:

- `ableton://session/current`: Current Live session snapshot.
- `ableton://project/key`: Saved key, mode, tempo, and genre.
- `ableton://genres`: Supported genres, tempos, default modes, drum patterns, and bass styles.
- `ableton://browser/favorites`: Curated instruments, effects, drum racks, and known-good browser URIs.
- `ableton://tool-guide`: Recommended tool workflows and constraints for the model.

## 3. Add High-Value Tools

Status: Pending

Prioritize tools that unlock common production workflows and reduce manual Ableton work.

Track and clip tools:

- `create_audio_track`
- `duplicate_track`
- `duplicate_clip`
- `clear_clip_notes`
- `quantize_clip`
- `transpose_clip`
- `humanize_clip`
- `crop_clip`

Arrangement tools:

- `set_loop_region`
- `enable_arrangement_loop`
- `duplicate_arrangement_region`
- `delete_arrangement_clip`
- `move_arrangement_clip`
- `create_full_arrangement`

Session View tools:

- `create_scene`
- `rename_scene`
- `fire_scene`
- `stop_all_clips`

Browser and device tools:

- `search_browser_items`
- `load_best_instrument`
- `load_best_effect`
- `load_best_drum_kit`
- `create_return_track`
- `load_return_effect`
- `set_return_track_volume`

Project organization tools:

- `group_tracks`, if Live API support is workable.
- `set_track_arm`, with safe handling for group, return, and master tracks.
- `set_selected_track`
- `set_selected_clip`

## 4. Improve Composition Generators

Status: Pending

The current chord, bass, drum, and scaffold generators are a good base. Next additions should make generated projects feel less static.

Recommended generators:

- Melody generator with motifs, contour, density, call-and-response, and scale awareness.
- Arpeggio generator with rate, octave range, direction, and gate controls.
- Pad generator that turns chord progressions into long, voiced textures.
- Drum fill generator for section transitions.
- FX riser/downlifter generator using MIDI notes or automation-ready clips.
- Variation generator that creates A/B versions of drums, bass, chords, and melodies.
- Arrangement density rules, such as hats-only intro, reduced breakdown, and full drop.

Recommended theory/style expansions:

- Borrowed chords and modal interchange.
- Secondary dominants and passing diminished chords.
- More chord rhythm patterns.
- More genres: techno, afro house, UK garage, dubstep, synthwave, ambient, lo-fi, reggaeton, trance, and pop.
- Genre-specific drum velocities and timing templates.

## 5. Improve Sound Design

Status: Pending

Sound design should move from generic parameter setting to role-aware patches.

Recommended improvements:

- Add more presets to `music_theory.SOUND_PRESETS`.
- Create presets by role: sub, reese, pluck, pad, lead, arp, stab, riser, drum bus, vocal bus, master roughing chain.
- Add device-specific parameter maps for Wavetable, Operator, Analog, Drift, EQ Eight, Compressor, Glue Compressor, Saturator, Reverb, Delay, Auto Filter, and Utility.
- Add a `describe_device_parameters` helper that groups parameters by oscillator, filter, envelope, LFO, effect, and output.
- Add `apply_effect_chain_preset` for common chains like sidechain-ready bass, washed pad, drum glue, and send reverb.

## 6. Improve Reliability and Architecture

Status: In progress

These changes make the server easier to maintain and less fragile under real sessions.

Completed:

- Extracted MCP prompts into `MCP_Server/prompts.py`.
- Extracted MCP resources into `MCP_Server/resources.py`.
- Extracted Ableton socket connection management into `MCP_Server/connection.py`.
- Extracted persisted project key state into `MCP_Server/state.py`.
- Kept tool implementations in `MCP_Server/server.py` as the next refactor boundary.

Recommended engineering work:

- Replace the large Remote Script command `if/elif` router with a command registry.
- Add explicit socket message framing instead of reading until bytes parse as JSON.
- Return structured JSON consistently from all MCP tools instead of mixing JSON and prose strings.
- Add input validation for tool arguments, preferably with Pydantic models or small local validators.
- Move `project_key.json` out of the package directory and into a user state/config directory.
- Add a fake Ableton socket server for integration tests.
- Add unit tests for `music_theory.py`.
- Add tests for tool argument validation and command payloads.
- Add clearer errors for missing Ableton connection, unsupported Live versions, and unsupported track types.
- Avoid checking generated `.venv`, `.DS_Store`, and IDE files into package artifacts.

## 7. Documentation Improvements

Status: Pending

Recommended docs:

- Add a tool reference generated from MCP tool docstrings.
- Add workflow examples for full track creation, remixing a loop, sound design, and rough mixing.
- Add troubleshooting for HTTPS/git, Ableton port conflicts, missing Remote Script, and Live API version limitations.
- Document supported genres, modes, drum pitch mappings, and sound presets.
- Document which tools mutate the Live set and which are read-only.

## Suggested Implementation Order

1. Add prompts and resources. Done.
2. Add `create_audio_track`, browser search, and loop-region tools.
3. Add clip editing tools: quantize, transpose, clear notes, duplicate, humanize.
4. Expand `scaffold_track` into a true `create_full_arrangement` workflow.
5. Add melody, arp, pad, fill, and variation generators.
6. Refactor command routing and add structured response validation.
7. Add tests and generated tool documentation.
