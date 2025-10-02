# gradio_tabs.tab5_prepare_text

> Gradio Tab 5: Prepare Text

## Public API


### Functions
- **get_available_text_files** — Find available text files for preparation
- **load_text_file_info** — Load information about selected text file
- **start_text_preparation** — Start text preparation with enriched chunking
- **get_preparation_status** — Get current preparation status
- **stop_text_preparation** — Stop current preparation (if possible)
- **create_prepare_text_tab** — Create Tab 5: Prepare Text with all GUI functionality
- **refresh_file_list** — Refresh text files list
- **show_next_steps** — Show next steps information
- **generate_enriched_chunks**
- **preparation_worker**

## Imports (local guesses)
- config.config, gradio, json, modules.path_validator, modules.tts_engine, os, pathlib, sys, threading, time, typing

## Entrypoint
- Contains `if __name__ == '__main__':` block