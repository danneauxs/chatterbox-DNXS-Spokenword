# gradio_tabs.tab1_convert_book

> Gradio Tab 1: Convert Book

## Public API


### Functions
- **parse_progress_stats** — Parse progress statistics from TTS engine output
- **get_progress_stats** — Get current progress statistics for UI update
- **get_book_folders** — Get available book folders from Text_Input directory
- **get_text_files_in_folder** — Get text files in selected book folder
- **get_voice_samples** — Get available voice samples from Voice_Samples directory
- **find_generated_audiobook** — Find the generated audiobook files
- **run_book_conversion** — Run the actual book conversion - Direct call to TTS engine with progress monitoring
- **regenerate_m4b_file** — Regenerate M4B file with new playback speed using unified convert_to_m4b
- **list_text_files** — Scans a folder path and populates the text file dropdown.
- **play_voice_sample** — Plays the audio file at the given path.
- **create_convert_book_tab** — Create Tab 1: Convert Book with all GUI functionality
- **handle_voice_upload** — Handle voice file upload and show player
- **get_session_audiobooks** — Get list of M4B files from current session, sorted by creation time (newest first)
- **update_audiobook_dropdowns** — Update audiobook dropdowns - after conversion both show latest, after regeneration only playback updates
- **update_audiobook_dropdowns_after_conversion** — Update both dropdowns to show the newest generated file after conversion
- **update_playback_only** — Update only the playback dropdown after regeneration
- **load_selected_audiobook** — Load selected audiobook into player
- **handle_asr_toggle** — Show/hide ASR configuration when ASR is toggled
- **analyze_system** — Analyze system capabilities and return summary
- **update_asr_models** — Update ASR model display based on selected level
- **start_conversion** — Start the actual book conversion - file upload version
- **handle_m4b_regeneration** — Handle M4B regeneration and update player
- **apply_preset**
- **get_current_stats** — Get current progress statistics by monitoring output files
- **get_status_and_results** — Get conversion status and results after completion
- **progress_callback** — Callback function to update progress from TTS engine
- **run_conversion_thread**

## Imports (local guesses)
- config.config, datetime, gradio, importlib.util, json, modules.file_manager, modules.path_validator, modules.system_detector, modules.tts_engine, os, pathlib, pygame, re, shutil, subprocess, sys, tempfile, threading, time, traceback, typing, warnings

## Entrypoint
- Contains `if __name__ == '__main__':` block