# tools.measure_token_memory

> Speech Token Memory Footprint Analysis

## Public API


### Functions
- **get_memory_usage** — Get current memory usage
- **measure_tensor_size** — Measure actual tensor memory footprint
- **generate_test_tokens** — Generate speech tokens and measure memory usage
- **analyze_queue_capacity** — Analyze how many sequences can fit in system RAM
- **simulate_queue_transfer_overhead** — Simulate CPU ↔ GPU transfer overhead for queue operations
- **main**

## Imports (local guesses)
- gc, json, modules.file_manager, modules.tts_engine, numpy, os, pathlib, psutil, src.chatterbox.tts, sys, torch

## Entrypoint
- Contains `if __name__ == '__main__':` block