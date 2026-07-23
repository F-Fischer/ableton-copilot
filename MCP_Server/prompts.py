def register_prompts(mcp) -> None:
    @mcp.prompt(
        name="compose_track",
        description="Create a new Ableton arrangement from genre, mood, key, and length.",
    )
    def compose_track_prompt(
        genre: str,
        key: str = "",
        mood: str = "",
        length: str = "short",
    ) -> str:
        return f"""
Create a {length} Ableton arrangement in the style of {genre}.
Mood: {mood or "choose an appropriate mood"}
Preferred key: {key or "choose an appropriate key and mode"}

Workflow:
1. Read ableton://genres and ableton://project/key.
2. Call get_session_info to inspect the current set.
3. Call set_project_key with genre, tonic, mode, and tempo.
4. Call scaffold_track to create markers and core tracks.
5. Use browser tools to find and load suitable instruments/effects.
6. Generate or refine drums, bass, chords, pad, and fx parts.
7. Switch to Arrangement View.
8. Return a concise summary of tracks, sections, key, tempo, and manual follow-ups.
"""

    @mcp.prompt(
        name="arrange_existing_loop",
        description="Turn existing Session View material into a structured Arrangement View song.",
    )
    def arrange_existing_loop_prompt(
        target_structure: str = "intro, build, drop, breakdown, outro",
        length_bars: int = 64,
    ) -> str:
        return f"""
Arrange the existing Ableton material into a {length_bars}-bar song structure:
{target_structure}

Workflow:
1. Call get_session_info and inspect relevant tracks with get_track_info.
2. Read MIDI clips with get_clip_notes where variation is needed.
3. Create section markers with create_section_markers.
4. Duplicate useful Session clips into Arrangement View with duplicate_to_arrangement.
5. Vary density by section using clip placement, muting, and generated fills.
6. Switch to Arrangement View and summarize the arrangement.
"""

    @mcp.prompt(
        name="mix_session",
        description="Create a rough static mix for the current Ableton session.",
    )
    def mix_session_prompt(style: str = "balanced", headroom: str = "leave conservative headroom") -> str:
        return f"""
Create a {style} rough mix for the current Ableton session and {headroom}.

Workflow:
1. Call get_session_info and inspect all important tracks with get_track_info.
2. Identify drums, bass, harmony, lead, pad, fx, return, and master roles from names/devices.
3. Set initial volume with set_track_volume.
4. Set pan positions with set_track_pan where appropriate.
5. Configure sends with set_send_level when return tracks exist.
6. Avoid destructive edits unless explicitly requested.
7. Return a concise mix log with track changes and any assumptions.
"""

    @mcp.prompt(
        name="sound_design_patch",
        description="Design or refine a synth/effect patch from a text description.",
    )
    def sound_design_patch_prompt(
        sound: str,
        track_index: int,
        device_index: int = 0,
    ) -> str:
        return f"""
Design this sound on track {track_index}, device {device_index}: {sound}

Workflow:
1. Call get_track_info for track {track_index}.
2. Call get_device_parameters for device {device_index}, using name_filter if the parameter list is large.
3. If a matching preset exists, call apply_sound_design_preset.
4. Use set_device_parameter or set_multiple_device_parameters for targeted tweaks.
5. Keep values inside the parameter ranges returned by get_device_parameters.
6. Return a concise patch summary and any skipped parameters.
"""

    @mcp.prompt(
        name="remix_clip",
        description="Create a musical variation of an existing MIDI clip.",
    )
    def remix_clip_prompt(
        track_index: int,
        clip_index: int,
        variation: str = "make a complementary variation",
        destination_clip_index: int = -1,
    ) -> str:
        return f"""
Create a variation of the MIDI clip at track {track_index}, slot {clip_index}.
Variation request: {variation}
Destination clip slot: {destination_clip_index if destination_clip_index >= 0 else "choose an empty slot"}

Workflow:
1. Call get_project_key and get_clip_notes.
2. Preserve the original clip unless the user explicitly asked to overwrite it.
3. Create a destination clip with create_clip.
4. Transform the notes according to the variation request.
5. Use add_notes_to_clip, with snap_to_scale if a project key is available.
6. Name the new clip with set_clip_name and summarize the changes.
"""

    @mcp.prompt(
        name="debug_ableton_connection",
        description="Diagnose MCP server and Ableton Remote Script connection problems.",
    )
    def debug_ableton_connection_prompt() -> str:
        return """
Diagnose the Ableton Copilot connection.

Workflow:
1. Try get_session_info and report the exact error if it fails.
2. Confirm Ableton Live is open and the AbletonMCP Remote Script is selected as a Control Surface.
3. Confirm only one MCP server instance is running.
4. Confirm the server is using ABLETON_HOST/ABLETON_PORT, defaulting to localhost:9877.
5. If the connection times out, suggest restarting Ableton Live and the MCP client.
6. If Live version support is relevant, mention that create_audio_clip requires Live 12.0.5 or newer.
"""
