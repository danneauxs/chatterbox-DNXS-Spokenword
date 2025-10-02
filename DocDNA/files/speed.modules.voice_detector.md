# speed.modules.voice_detector

> Voice Detection Module

## Public API


### Functions
- **get_likely_voices_for_book** — Get the most likely voice candidates for a book using the 3 detection methods:
- **detect_voice_for_book** — Detect the most likely voice for a book (returns first candidate)
- **get_voice_from_json** — Extract voice information from JSON metadata
- **get_voice_from_log** — Extract voice information from run.log file
- **get_voices_from_filenames** — Extract voice names from existing audiobook filename patterns (may return multiple)
- **get_voice_from_filename** — Extract voice name from existing audiobook filename patterns (backwards compatibility)
- **find_voice_file_by_name** — Find voice file by name in Voice_Samples directory
- **add_voice_to_json** — Add voice information to JSON file
- **remove_voice_comment_from_json** — Remove voice comment from JSON file for clean processing

## Imports (local guesses)
- config.config, json, modules.file_manager, pathlib, re