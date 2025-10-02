# tools.test_sequential_pipeline

> Sequential Pipeline Performance Test

## Public API


### Functions
- **get_memory_usage** — Get current memory usage
- **monitor_gpu_simple** — Simple GPU utilization check
- **phase_1_t3_processing** — Phase 1: T3 fills RAM with speech tokens (100% GPU for T3)
- **clear_t3_from_memory** — Phase 1.5: Clear T3 from GPU memory
- **phase_2_s3gen_processing** — Phase 2: Dual S3Gen workers consume RAM queue (100% GPU for S3Gen)
- **main**

## Imports (local guesses)
- gc, json, modules.text_processor, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, subprocess, sys, time, torch, traceback

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block