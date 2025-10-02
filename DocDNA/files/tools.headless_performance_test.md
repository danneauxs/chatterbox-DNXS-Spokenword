# tools.headless_performance_test

> Headless Performance Testing Framework for Chatterbox TTS

## Public API

### Classes
- **PerformanceResult** — Single performance measurement result  
  Methods: (no public methods)
- **HeadlessPerformanceTester** — Main performance testing framework  
  Methods: test_torch_compile_configurations, test_batching_configurations, test_memory_optimizations, run_full_test_suite, save_results, print_summary

### Functions
- **main**
- **test_torch_compile_configurations** — Test different torch.compile configurations
- **test_batching_configurations** — Test different batching configurations
- **test_memory_optimizations** — Test memory layout and optimization configurations
- **run_full_test_suite** — Run comprehensive performance test suite
- **save_results** — Save test results to file
- **print_summary** — Print a summary of results

## Imports (local guesses)
- argparse, config.config, dataclasses, gc, json, logging, modules.file_manager, modules.terminal_logger, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, subprocess, sys, time, torch, typing

## Framework signals
- argparse

## Side-effect signals
- env_reads

## Entrypoint
- Contains `if __name__ == '__main__':` block