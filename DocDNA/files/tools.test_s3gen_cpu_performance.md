# tools.test_s3gen_cpu_performance

> S3Gen CPU vs GPU Performance Test

## Public API


### Functions
- **clear_memory** — Clear GPU memory
- **get_test_voice** — Get first available voice for testing
- **get_memory_usage** — Get current memory usage statistics
- **create_test_speech_tokens** — Generate speech tokens using T3 for testing S3Gen
- **test_s3gen_gpu_performance** — Test S3Gen performance on GPU
- **test_s3gen_cpu_performance** — Test S3Gen performance on CPU
- **analyze_pipeline_potential** — Analyze potential for T3 GPU + S3Gen CPU pipeline
- **main**

## Imports (local guesses)
- gc, json, modules.file_manager, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, sys, time, torch

## Entrypoint
- Contains `if __name__ == '__main__':` block