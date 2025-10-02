# speed.modules.file_manager

> ChatterboxTTS File Management & Media Processing Module

## Public API


### Functions
- **is_ffmpeg_available** — Check if FFmpeg is available in system PATH
- **ffmpeg_error_message** — Standard error message for missing FFmpeg
- **list_voice_samples** — List available voice samples
- **ensure_voice_sample_compatibility** — Ensure voice sample is compatible with TTS (24kHz mono)
- **run_ffmpeg** — Run FFmpeg command with error handling
- **convert_to_m4b_with_peak_normalization** — Convert WAV to M4B with peak normalization
- **convert_to_m4b_with_loudness_normalization** — Convert WAV to M4B with two-pass loudness normalization
- **convert_to_m4b_with_simple_normalization** — Convert WAV to M4B with simple peak normalization
- **convert_to_m4b** — Convert WAV to M4B with configurable normalization and optional custom speed/sample rate
- **add_metadata_to_m4b** — Add metadata and cover to M4B
- **chunk_sort_key** — Extracts the chunk number for natural sorting
- **create_concat_file** — Create FFmpeg concat file for audio chunks
- **cleanup_temp_files** — Clean up temporary files matching patterns
- **sanitize_filename** — Sanitize filename for cross-platform compatibility
- **setup_book_directories** — Set up directory structure for book processing
- **find_book_files** — Find text files, cover, and metadata for a book
- **combine_audio_chunks** — Combine audio chunks into single file using FFmpeg
- **get_audio_files_in_directory** — Get sorted list of audio files matching pattern
- **verify_audio_file** — Verify audio file is valid and readable
- **verify_chunk_completeness** — Verify all expected chunks exist and are valid
- **export_processing_log** — Export comprehensive processing log
- **save_chunk_info** — Save chunk information for debugging/resume
- **apply_batch_binning** — Round VADER parameters to nearest bin for better microbatching
- **load_chunk_info** — Load chunk information if available

## Imports (local guesses)
- config.config, json, logging, os, pathlib, re, soundfile, subprocess, time

## Side-effect signals
- subprocess