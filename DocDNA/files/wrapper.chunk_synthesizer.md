# wrapper.chunk_synthesizer

## Public API


### Functions
- **get_original_voice_from_log** — Extract original voice name from run log
- **get_original_voice_from_filename** — Extract voice name from existing audiobook filename
- **find_voice_file_by_name** — Find voice file by name in Voice_Samples directory
- **get_tts_params_for_chunk** — Extract TTS parameters from chunk data or prompt user
- **synthesize_chunk** — Generate audio for a single chunk using specified or detected voice and TTS parameters
- **get_float_input**

## Imports (local guesses)
- config.config, io, modules.audio_processor, modules.file_manager, modules.tts_engine, modules.voice_detector, pathlib, pydub, re, soundfile, time, torch, traceback