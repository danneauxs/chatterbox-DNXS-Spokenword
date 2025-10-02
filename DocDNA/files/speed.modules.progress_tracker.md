# speed.modules.progress_tracker

> ChatterboxTTS Progress Tracking & Performance Monitoring Module

## Public API

### Classes
- **PerformanceTracker** — PERFORMANCE TRACKING CLASS - Core metrics collection and analysis  
  Methods: log_chunk_completion, log_batch_completion, get_performance_summary

### Functions
- **setup_logging** — Setup logging configuration
- **log_console** — Log to both console and file with optional color
- **log_run** — Log to run file
- **log_chunk_progress** — Enhanced progress logging with configurable display frequency and average it/s
- **display_batch_progress** — Display batch processing progress
- **display_final_summary** — Display final processing summary
- **monitor_vram_usage** — Real-time VRAM monitoring with threshold warnings
- **monitor_gpu_utilization** — Monitor GPU utilization if pynvml is available
- **optimize_memory_if_needed** — Trigger memory optimization when thresholds are exceeded
- **display_system_info** — Display system information at startup
- **log_processing_error** — Log processing errors with categorization
- **log_processing_warning** — Log processing warnings with categorization
- **create_status_line** — Create a single-line status for real-time updates
- **update_status_line** — Update status line in place
- **export_performance_report** — Export detailed performance report
- **fmt**
- **log_chunk_completion** — Log individual chunk completion
- **log_batch_completion** — Log batch completion
- **get_performance_summary** — Get comprehensive performance summary

## Imports (local guesses)
- config.config, datetime, gc, logging, modules.smart_reload_manager, modules.terminal_logger, modules.tts_engine, pathlib, pynvml, sys, time, torch