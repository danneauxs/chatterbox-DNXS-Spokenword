# speed.modules.system_detector

> System Resource Detection Module

## Public API


### Functions
- **get_gpu_memory** — Get total and available GPU memory in MB
- **get_system_memory** — Get total and available system RAM in MB
- **get_cpu_cores** — Get number of CPU cores
- **estimate_tts_vram_usage** — Estimate VRAM usage by ChatterboxTTS (updated based on real usage)
- **get_system_profile** — Get complete system resource profile
- **categorize_system** — Categorize system capabilities
- **get_safe_asr_models** — Get ASR models that can safely run on GPU with available VRAM
- **get_safe_cpu_models** — Get ASR models that can safely run on CPU with available RAM
- **recommend_asr_models** — Recommend Safe/Moderate/Insane ASR model configurations
- **print_system_summary** — Print a human-readable system summary

## Imports (local guesses)
- config.config, os, pathlib, psutil, sys, torch

## Entrypoint
- Contains `if __name__ == '__main__':` block