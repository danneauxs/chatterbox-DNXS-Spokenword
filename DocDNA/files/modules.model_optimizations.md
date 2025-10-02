# modules.model_optimizations

> Model Optimization Module

## Public API

### Classes
- **MixedPrecisionOptimizer** — Mixed precision optimization for faster inference  
  Methods: (no public methods)
- **TextTokenizationCache** — Smart caching system for text tokenization  
  Methods: get, put, get_stats, clear
- **MemoryOptimizer** — Advanced memory optimization strategies  
  Methods: optimize_memory_usage, get_gpu_memory_usage, should_optimize_memory, monitor_memory_usage
- **MemoryMonitor** — Context manager for monitoring memory usage  
  Methods: (no public methods)
- **InferenceOptimizer** — Optimizations specifically for inference performance  
  Methods: setup_inference_optimizations, optimize_model_for_inference
- **OptimizedTTSWrapper** — Wrapper that applies all optimizations to TTS operations  
  Methods: generate, prepare_conditionals, get_optimization_stats, log_performance_summary

### Functions
- **create_optimized_model** — Create an optimized wrapper around a ChatterboxTTS model
- **get** — Get cached tokenization result
- **put** — Store tokenization result in cache
- **get_stats** — Get cache performance statistics
- **clear** — Clear the cache
- **optimize_memory_usage** — Optimize memory usage with various strategies
- **get_gpu_memory_usage** — Get current GPU memory usage in GB
- **should_optimize_memory** — Check if memory optimization is needed
- **monitor_memory_usage** — Context manager for monitoring memory usage during operations
- **setup_inference_optimizations** — Setup general inference optimizations
- **optimize_model_for_inference** — Apply inference-specific optimizations to a model
- **generate** — Optimized generation with all optimizations applied
- **prepare_conditionals** — Optimized voice conditioning preparation
- **get_optimization_stats** — Get comprehensive optimization statistics
- **log_performance_summary** — Log comprehensive performance summary

## Imports (local guesses)
- gc, hashlib, logging, pathlib, time, torch, typing