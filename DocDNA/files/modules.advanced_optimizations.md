# modules.advanced_optimizations

> Advanced Optimizations Module

## Public API

### Classes
- **AdvancedOptimizer** — Advanced optimization suite for ChatterboxTTS performance  
  Methods: diagnose_and_fix_torch_compile, apply_smart_torch_compile, apply_advanced_int8_quantization, apply_memory_optimizations, revert_optimizations

### Functions
- **set_warmup_mode** — Set global warm-up mode flag to use safe optimizations
- **get_advanced_optimizer** — Get global advanced optimizer instance
- **optimize_model_advanced** — Apply comprehensive advanced optimizations to ChatterboxTTS model
- **diagnose_and_fix_torch_compile** — Diagnose and fix common torch.compile issues based on 2025 research
- **apply_smart_torch_compile** — Apply torch.compile with intelligent backend selection and error handling
- **apply_advanced_int8_quantization** — Apply advanced INT8 quantization based on 2025 research
- **apply_memory_optimizations** — Apply comprehensive memory optimizations based on 2025 research
- **revert_optimizations** — Revert all applied optimizations

## Imports (local guesses)
- logging, os, pathlib, subprocess, torch, torch._dynamo, triton, typing, warnings

## Side-effect signals
- subprocess