# tools.trace_t3_inference

> T3 Inference Breakdown Tracer

## Public API


### Functions
- **monitor_gpu** — Quick GPU utilization check
- **patched_t3_inference_with_timing** — Monkey-patch T3 inference with detailed timing measurements
- **trace_t3_inference_detailed** — Trace T3 inference with detailed internal measurements
- **main**

## Imports (local guesses)
- gc, json, modules.tts_engine, os, pathlib, src.chatterbox.models.t3.inference.alignment_stream_analyzer, src.chatterbox.models.t3.inference.t3_hf_backend, src.chatterbox.models.t3.t3, subprocess, sys, time, torch, traceback, transformers.generation.logits_process

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block