# interface

> ==============================================================================

## Public API


### Functions
- **signal_handler** — Handle Ctrl+C gracefully
- **prompt_book_selection** — Interactive book selection from available directories
- **prompt_voice_selection** — Interactive voice selection from available samples
- **prompt_tts_params** — Interactive TTS parameter configuration
- **pipeline_book_processing** — Processes a queue of books, calling the main processing function for each.
- **main** — Main entry point for GenTTS processing
- **main_with_resume** — Main entry point with resume option
- **get_float_input**
- **get_yes_no_input**
- **get_choice_input**

## Imports (local guesses)
- argparse, config.config, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.resume_handler, modules.system_detector, modules.text_processor, modules.tts_engine, os, pathlib, signal, src.chatterbox.tts, sys, tools.combine_only, torch, traceback, warnings

## Framework signals
- argparse

## Entrypoint
- Contains `if __name__ == '__main__':` block