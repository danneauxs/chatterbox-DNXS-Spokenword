# GARBAGE.gpu_utilization_optimizer

> GPU Utilization Optimizer

## Public API

### Classes
- **AsyncTTSProcessor** — Asynchronous TTS processor with GPU utilization smoothing  
  Methods: start, stop, generate_async, get_result, get_stats
- **PipelinedTTSProcessor** — Pipelined TTS processor for smoother GPU utilization  
  Methods: start, stop, generate_pipelined, get_result
- **SmoothGPUOptimizer** — Main GPU utilization optimizer combining multiple strategies  
  Methods: generate_optimized, cleanup, get_optimization_stats

### Functions
- **create_gpu_optimizer** — Create GPU utilization optimizer
- **start** — Start async processing threads
- **stop** — Stop async processing
- **generate_async** — Add text to async processing queue
- **get_result** — Get next completed result
- **get_stats** — Get processing statistics
- **start** — Start pipelined processing
- **stop** — Stop pipelined processing
- **generate_pipelined** — Add text to pipelined processing
- **get_result** — Get next completed result from pipeline
- **generate_optimized** — Generate audio with optimized GPU utilization
- **cleanup** — Clean up processor resources
- **get_optimization_stats** — Get optimization statistics

## Imports (local guesses)
- asyncio, collections, concurrent.futures, logging, queue, threading, time, torch, typing