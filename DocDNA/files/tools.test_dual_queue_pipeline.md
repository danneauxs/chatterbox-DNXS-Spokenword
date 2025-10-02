# tools.test_dual_queue_pipeline

> Dual Queue Pipeline Performance Test

## Public API

### Classes
- **DualQueueManager** — Manages dual queue system for T3 → S3Gen pipeline  
  Methods: switch_queues, get_queue_status

### Functions
- **load_test_content** — Load designated test files
- **prepare_text_chunks** — Process text into chunks for testing
- **t3_worker** — T3 worker thread - generates speech tokens
- **s3gen_worker** — S3Gen worker thread - processes speech tokens to audio
- **monitor_gpu_utilization** — Monitor GPU utilization during pipeline operation
- **analyze_pipeline_performance** — Analyze pipeline performance results
- **main**
- **switch_queues** — Switch queue roles when one becomes full
- **get_queue_status** — Get current queue status

## Imports (local guesses)
- collections, gc, json, modules.text_processor, modules.tts_engine, os, pathlib, psutil, queue, src.chatterbox.tts, subprocess, sys, threading, time, torch, traceback

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block