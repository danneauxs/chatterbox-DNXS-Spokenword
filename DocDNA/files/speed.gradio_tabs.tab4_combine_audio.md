# speed.gradio_tabs.tab4_combine_audio

> Gradio Tab 4: Combine Audio

## Public API


### Functions
- **get_available_books** — Get list of books with audio chunks available for combining
- **get_book_info** — Get detailed information about a book's audio chunks
- **run_combine_operation** — Run the audio combine operation
- **create_combine_audio_tab** — Create Tab 4: Combine Audio with all GUI functionality
- **update_book_info** — Update book information when selection changes
- **refresh_book_list** — Refresh the list of available books
- **get_selected_book_path** — Get the actual book path from selection or manual input
- **start_combine_operation** — Start the combine operation
- **stop_combine_operation** — Stop the current combine operation
- **get_current_status** — Get current operation status for periodic updates
- **combine_audio_for_book**
- **get_audio_files_in_directory**
- **get_wav_duration**
- **run_combine_thread**

## Imports (local guesses)
- gradio, modules.audio_processor, modules.file_manager, os, pathlib, sys, threading, time, tools.combine_only, typing

## Entrypoint
- Contains `if __name__ == '__main__':` block