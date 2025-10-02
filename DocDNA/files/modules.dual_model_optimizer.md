# modules.dual_model_optimizer

> Dual Model Parallel Inference Optimizer

## Public API

### Classes
- **DualModelParallelOptimizer** — Run 2 ChatterboxTTS models in parallel to maximize bandwidth utilization  
  Methods: load_dual_models, generate_parallel_pair, benchmark_dual_vs_single, process_chunks_parallel, cleanup

### Functions
- **test_dual_model_optimization** — Test dual model optimization approach
- **load_dual_models** — Load two identical ChatterboxTTS models for parallel inference
- **generate_parallel_pair** — Generate audio for 2 chunks in parallel using both models
- **benchmark_dual_vs_single** — Benchmark dual-model vs single-model performance
- **process_chunks_parallel** — Process multiple chunks using dual-model parallelization
- **cleanup** — Clean up resources

## Imports (local guesses)
- asyncio, concurrent.futures, config.config, gc, modules.real_tts_optimizer, pathlib, src.chatterbox.tts, sys, threading, time, torch

## Entrypoint
- Contains `if __name__ == '__main__':` block