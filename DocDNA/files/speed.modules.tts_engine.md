# speed.modules.tts_engine

> TTS Engine Module

## Public API


### Functions
- **clear_voice_cache** — Clear the global voice cache at start of new conversion
- **store_voice_cache** — Store voice embeddings from model to global cache
- **restore_voice_cache** — Restore voice embeddings from global cache to model
- **get_voice_cache_info** — Get information about current voice cache
- **find_chunks_json_file** — Find the corresponding chunks JSON file for a book
- **set_seed** — Sets the seed for torch, random, and numpy for reproducibility.
- **monitor_gpu_activity** — Lightweight GPU monitoring for high-speed processing
- **optimize_memory_usage** — Aggressive memory management for 8GB VRAM
- **monitor_vram_usage** — Real-time VRAM monitoring
- **get_optimal_workers** — Dynamic worker allocation based on VRAM usage
- **prewarm_model_with_voice** — Pre-warm the TTS model with a voice sample to eliminate cold start quality issues.
- **get_best_available_device** — Detect and return the best available device with proper fallback
- **load_optimized_model** — Load TTS model with REAL performance optimizations.
- **patch_alignment_layer** — Patch alignment layer to avoid recursion
- **process_batch**
- **process_one_chunk**
- **smooth_sentiment_scores** — Apply sentiment smoothing to prevent harsh emotional transitions.
- **generate_enriched_chunks** — Reads a text file, performs VADER sentiment analysis, and returns enriched chunks.
- **create_parameter_microbatches** — Group chunks by their rounded TTS parameters for micro-batching efficiency.
- **process_book_folder** — Enhanced book processing with batch processing to prevent hangs
- **process_single_batch** — Loads models and processes a single batch of chunks.
- **patched_forward**
- **log_run**
- **gen_with_backoff**

## Imports (local guesses)
- collections, concurrent.futures, config, config.config, datetime, difflib, gc, glob, io, logging, modules, modules.asr_manager, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.real_tts_optimizer, modules.terminal_logger, modules.text_processor, modules.voice_detector, numpy, os, pathlib, pydub, random, shutil, soundfile, src.chatterbox.tts, sys, tempfile, threading, time, torch, torchaudio, traceback, types, vaderSentiment.vaderSentiment, wrapper.chunk_loader

## Side-effect signals
- file_io