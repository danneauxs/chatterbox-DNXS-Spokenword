# tools.trace_pipeline_flow

> Pipeline Flow Tracer

## Public API


### Functions
- **monitor_gpu** — Quick GPU utilization check
- **trace_single_chunk_pipeline** — Trace pipeline for a single chunk with detailed monitoring
- **analyze_pipeline_bottlenecks** — Analyze where time is spent in the pipeline
- **trace_multiple_chunks** — Trace multiple chunks to find inter-chunk timing patterns
- **main**

## Imports (local guesses)
- gc, json, modules.tts_engine, os, pathlib, src.chatterbox.tts, subprocess, sys, time, torch, traceback

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block