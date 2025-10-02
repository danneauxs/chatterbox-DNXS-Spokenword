# modules.resume_handler

> ChatterboxTTS Resume Handler Module

## Public API


### Functions
- **analyze_existing_chunks** — CHUNK ANALYSIS FUNCTION - Core resume logic
- **suggest_resume_point** — Suggest optimal resume point based on existing chunks
- **validate_resume_point** — Validate that resume point makes sense
- **process_book_folder_resume** — Enhanced book processing with resume capability
- **resume_book_from_chunk** — Interactive resume function for stuck book
- **find_incomplete_books** — Find books that appear to be incomplete
- **auto_resume_incomplete** — Automatically suggest resume for incomplete books
- **prompt_float**

## Imports (local guesses)
- concurrent.futures, config.config, datetime, gc, logging, modules.asr_manager, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.text_processor, modules.tts_engine, pathlib, re, shutil, src.chatterbox.tts, time, torch, wrapper.chunk_loader