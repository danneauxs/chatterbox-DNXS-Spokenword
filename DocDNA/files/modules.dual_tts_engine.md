# modules.dual_tts_engine

> Dual TTS Parallel Inference Engine (Simplified)

## Public API

### Classes
- **WorkItem** — Work item for TTS worker  
  Methods: (no public methods)
- **AudioResult** — Result from TTS worker  
  Methods: (no public methods)
- **TTSWorker** — Complete TTS worker with dedicated CUDA stream.  
  Methods: run, stop
- **DualTTSCoordinator** — Coordinates two TTS workers with completion-based dispatch.  
  Methods: start, stop, process_chunks

### Functions
- **load_dual_tts_models** — Load 2 complete ChatterboxTTS models for parallel inference.
- **run** — Main worker loop
- **stop** — Stop worker gracefully
- **start** — Start workers
- **stop** — Stop workers
- **process_chunks** — Process chunks with completion-based dispatch.

## Imports (local guesses)
- config.config, dataclasses, logging, numpy, pathlib, queue, src.chatterbox.models.s3tokenizer, src.chatterbox.tts, threading, time, torch, torch.nn.functional, typing