# modules.dual_t3_engine

> Dual T3 Parallel Inference Engine

## Public API

### Classes
- **WorkItem** — Work item for T3 worker input queue  
  Methods: (no public methods)
- **TokenResult** — Result from T3 worker for S3Gen processing  
  Methods: (no public methods)
- **AudioResult** — Final result from S3Gen worker  
  Methods: (no public methods)
- **TTSWorker** — Independent TTS worker thread with dedicated CUDA stream.  
  Methods: run, stop
- **S3GenWorker** — S3Gen worker thread with dedicated CUDA stream.  
  Methods: run, stop
- **DualT3Coordinator** — Coordinates dual T3 workers with completion-based dispatch.  
  Methods: start, stop, process_chunks

### Functions
- **load_dual_t3_models** — Load 2 T3 models + 1 S3Gen model for dual parallel inference.
- **run** — Main worker loop - completion-based dispatch
- **stop** — Signal worker to stop gracefully
- **run** — Main worker loop
- **stop** — Signal worker to stop gracefully
- **start** — Start all worker threads
- **stop** — Stop all worker threads gracefully
- **process_chunks** — Process chunks using completion-based dispatch.

## Imports (local guesses)
- config.config, dataclasses, logging, numpy, pathlib, queue, src.chatterbox.tts, threading, time, torch, typing