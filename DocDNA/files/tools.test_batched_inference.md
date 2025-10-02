# tools.test_batched_inference

> Batched T3 Inference Tester

## Public API


### Functions
- **load_batching_plan** — Load batching plan from analysis file
- **prepare_text_batches** — Prepare text batches from batching plan
- **tokenize_text_batch** — Tokenize a batch of text chunks
- **benchmark_sequential_inference** — Benchmark sequential processing (current method)
- **benchmark_batched_inference** — Benchmark batched processing
- **run_batch_comparison** — Run comprehensive comparison of sequential vs batched inference
- **analyze_batch_results** — Analyze overall batching performance
- **main**

## Imports (local guesses)
- gc, json, modules.tts_engine, pathlib, sys, time, torch, typing

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block