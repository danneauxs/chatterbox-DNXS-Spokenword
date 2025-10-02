# speed.tools.combine_only

> Combine Only Tool

## Public API


### Functions
- **combine_audio_for_book** — Combine audio chunks for a specific book (GUI-friendly version)
- **run_combine_only_mode** — Combine existing chunks into audiobook (CLI version)
- **verify_chunk_sequence** — Verify chunk sequence and return missing chunk numbers
- **list_available_books_for_combine** — List books available for combine operation
- **quick_combine** — Quick combine operation for specific book (CLI usage)

## Imports (local guesses)
- config.config, datetime, logging, modules.audio_processor, modules.file_manager, modules.progress_tracker, pathlib, re, shutil, subprocess, sys, time

## Entrypoint
- Contains `if __name__ == '__main__':` block