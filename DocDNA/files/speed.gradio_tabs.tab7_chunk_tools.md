# speed.gradio_tabs.tab7_chunk_tools

> Gradio Tab 7: Chunk Tools

## Public API


### Functions
- **get_available_repair_books** — Get list of books available for chunk repair/editing
- **load_book_chunks** — Load chunks for selected book
- **search_for_chunks** — Search for chunks containing the query text
- **select_chunk_for_editing** — Select a chunk for editing from search results
- **save_chunk_changes** — Save changes to the current chunk
- **play_original_audio** — Play the original audio for the current chunk
- **resynthesize_chunk_audio** — Regenerate audio for the current chunk with new parameters
- **play_revised_audio** — Play the revised audio for the current chunk
- **accept_chunk_revision** — Accept the current chunk revision
- **create_chunk_tools_tab** — Create Tab 7: Chunk Tools with all GUI functionality
- **refresh_book_list** — Refresh the available books list
- **refresh_voice_candidates** — Refresh voice candidates for current book
- **load_chunks**
- **save_chunks**
- **search_chunks**
- **update_chunk**
- **play_chunk_audio**
- **synthesize_chunk**
- **accept_revision**
- **get_likely_voices_for_book**
- **play_audio**
- **resynth_worker**
- **play_audio**

## Imports (local guesses)
- config.config, gradio, json, modules.voice_detector, os, pathlib, sys, threading, time, typing, wrapper.chunk_editor, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_revisions, wrapper.chunk_search, wrapper.chunk_synthesizer

## Entrypoint
- Contains `if __name__ == '__main__':` block