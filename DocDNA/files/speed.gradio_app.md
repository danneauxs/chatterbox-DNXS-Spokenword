# speed.gradio_app

> Gradio Interface for ChatterboxTTS Audiobook Pipeline

## Public API


### Functions
- **initialize_tts** — Initialize TTS model once at startup
- **process_text_to_chunks** — Process text into chunks with metadata
- **generate_chunk_audio** — Generate audio for a single chunk
- **generate_audiobook** — Main function to generate audiobook from text and voice sample
- **create_interface** — Create the Gradio interface

## Imports (local guesses)
- datetime, gradio, json, logging, modules.audio_processor, modules.file_manager, modules.text_processor, os, pathlib, src.chatterbox.tts, tempfile, torch, torchaudio, traceback, vaderSentiment.vaderSentiment, zipfile

## Entrypoint
- Contains `if __name__ == '__main__':` block