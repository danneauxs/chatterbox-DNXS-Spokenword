# speed.modules.asr_manager

> ASR Manager Module

## Public API


### Functions
- **get_real_time_vram_status** — Get current GPU memory usage in real-time
- **calculate_available_vram_for_asr** — Calculate VRAM available for ASR with safety buffer
- **can_model_fit_gpu** — Check if a specific ASR model can fit in available VRAM
- **try_load_model_with_fallback** — Try to load model on primary device, fallback to secondary if it fails
- **load_asr_model_adaptive** — Adaptive ASR model loading with real-time VRAM checking and intelligent fallback
- **cleanup_asr_model** — Clean up ASR model to free memory
- **get_asr_memory_info** — Get memory information for ASR debugging
- **convert_device_name**

## Imports (local guesses)
- config.config, logging, pathlib, torch, whisper

## Entrypoint
- Contains `if __name__ == '__main__':` block