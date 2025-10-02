# tools.cuda_kernel_profiler

> CUDA Kernel Utilization Profiler and Optimizer

## Public API

### Classes
- **CudaUtilizationSnapshot** — Single GPU utilization measurement  
  Methods: (no public methods)
- **KernelProfilingResult** — Results from kernel profiling session  
  Methods: (no public methods)
- **CudaKernelProfiler** — Main CUDA kernel profiling and optimization tool  
  Methods: start_monitoring, stop_monitoring, analyze_utilization, profile_inference_workload, generate_optimization_recommendations, run_comprehensive_profile, save_profile_results, print_summary

### Functions
- **main**
- **start_monitoring** — Start GPU utilization monitoring
- **stop_monitoring** — Stop monitoring and return collected data
- **analyze_utilization** — Analyze GPU utilization patterns
- **profile_inference_workload** — Profile GPU utilization during a single inference
- **generate_optimization_recommendations** — Generate optimization recommendations based on profiling results
- **run_comprehensive_profile** — Run comprehensive CUDA kernel profiling
- **save_profile_results** — Save profiling results to file
- **print_summary** — Print profiling summary

## Imports (local guesses)
- argparse, config.config, dataclasses, gc, json, modules.file_manager, modules.tts_engine, os, pathlib, psutil, signal, subprocess, sys, threading, time, torch, traceback, typing

## Framework signals
- argparse

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block