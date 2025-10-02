# tools.test_sequence_batching

> Test True Sequence-Level Batching

## Public API


### Functions
- **clear_memory** — Clear GPU memory
- **get_test_voice** — Get first available voice for testing
- **create_test_chunks** — Create test chunks with varying parameters to test batching effectiveness
- **benchmark_individual_processing** — Benchmark individual chunk processing (baseline)
- **benchmark_sequence_batching** — Benchmark sequence-level batch processing
- **compare_performance** — Compare performance between individual and batch processing
- **main**

## Imports (local guesses)
- gc, json, modules.file_manager, modules.sequence_batch_processor, modules.tts_engine, os, pathlib, sys, time, torch

## Entrypoint
- Contains `if __name__ == '__main__':` block