# speed.modules.audio_processor

> ChatterboxTTS Audio Processing & Quality Control Module

## Public API


### Functions
- **check_audio_health** — Enhanced audio health checking
- **detect_tts_hum_artifact** — Detect low-frequency TTS confusion hum using configurable parameters
- **smart_audio_validation** — Comprehensive audio validation with intelligent responses
- **has_mid_energy_drop** — Detect mid-chunk energy drops
- **detect_spectral_artifacts** — Enhanced spectral anomaly detection using MFCC analysis.
- **evaluate_chunk_quality** — Composite quality evaluation for a single audio chunk.
- **validate_output_matches_input** — Validate that TTS audio output matches the input text using ASR transcription.
- **calculate_text_similarity** — Calculate similarity between two texts using word-level F1 score.
- **adjust_parameters_for_retry** — Adjust TTS parameters for regeneration attempts.
- **handle_problematic_chunks** — Handle chunks with audio issues - quarantine for review
- **pause_for_chunk_review** — Pause processing to allow manual chunk review/editing with proper workflow
- **detect_end_artifact** — Enhanced artifact detection
- **find_end_of_speech** — Find end of speech using Silero VAD
- **fade_out_wav** — Apply fade-out to audio
- **apply_smart_fade** — Apply smart fade with artifact detection
- **apply_smart_fade_memory** — Apply smart fade with artifact detection - in memory version
- **smart_audio_validation_memory** — Enhanced audio validation in memory - returns (audio, is_quarantined)
- **add_contextual_silence_memory** — Add appropriate silence based on content boundary type - in memory
- **smart_fade_out** — Smart fade-out for natural audio endings
- **trim_audio_endpoint** — Trim audio to the detected end of speech using RMS energy analysis.
- **process_audio_with_trimming_and_silence** — Complete audio processing: trim to speech endpoint + add punctuation-based silence.
- **add_contextual_silence** — Add appropriate silence based on content boundary type
- **add_chunk_end_silence** — Add configurable silence to end of chunk if enabled
- **get_wav_duration** — Get WAV file duration
- **get_chunk_audio_duration** — Get actual audio duration from WAV file
- **normalize_text**

## Imports (local guesses)
- config.config, librosa, logging, modules.asr_manager, numpy, os, pathlib, pydub, re, shutil, soundfile, tempfile, time, torch, wave