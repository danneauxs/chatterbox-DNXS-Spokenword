# gradio_tabs.tab8_json_generate

> Gradio Tab 8: JSON Generate

## Public API


### Functions
- **get_available_json_files** — Find available JSON chunk files for generation
- **get_available_voices** — Get list of available voice samples
- **load_json_file_info** — Load information about selected JSON file
- **start_json_generation** — Start JSON-to-audiobook generation
- **get_generation_status** — Get current generation status
- **stop_json_generation** — Stop current generation (if possible)
- **play_audio** — Play generated audiobook
- **create_json_generate_tab** — Create Tab 8: JSON Generate with all GUI functionality
- **refresh_json_files** — Refresh JSON files list
- **refresh_voice_list** — Refresh voice samples list
- **show_download_info** — Show download/playback instructions
- **generate_audiobook_from_json**
- **list_voice_samples**
- **generation_worker**

## Imports (local guesses)
- config.config, gradio, json, modules.file_manager, modules.gui_json_generator, os, pathlib, subprocess, sys, threading, time, typing

## Entrypoint
- Contains `if __name__ == '__main__':` block