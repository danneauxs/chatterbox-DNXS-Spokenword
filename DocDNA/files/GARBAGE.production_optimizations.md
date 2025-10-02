# GARBAGE.production_optimizations

> Production-Ready Model Optimizations

## Public API

### Classes
- **ProductionOptimizer** — Production-ready optimization wrapper for ChatterboxTTS  
  Methods: generate, prepare_conditionals, get_stats, log_performance_summary
- **TextCache** — Lightweight text caching for repeated generations  
  Methods: get, put, get_stats
- **MemoryManager** — Smart memory management for stable performance  
  Methods: get_memory_usage, should_cleanup, cleanup, get_stats
- **BatchOptimizer** — Optimized batch processing for multiple texts  
  Methods: generate_batch

### Functions
- **create_production_optimizer** — Create a production-ready optimized wrapper for ChatterboxTTS
- **create_batch_optimizer** — Create an optimized batch processor
- **generate** — Optimized generation with production-safe enhancements
- **prepare_conditionals** — Optimized voice conditioning
- **get_stats** — Get performance statistics
- **log_performance_summary** — Log comprehensive performance summary
- **get** — Get cached result
- **put** — Store result in cache
- **get_stats** — Get cache statistics
- **get_memory_usage** — Get current GPU memory usage in GB
- **should_cleanup** — Check if memory cleanup is needed
- **cleanup** — Perform memory cleanup and return amount freed
- **get_stats** — Get memory management statistics
- **generate_batch** — Generate audio for multiple texts with optimizations

## Imports (local guesses)
- gc, hashlib, logging, pathlib, time, torch, typing