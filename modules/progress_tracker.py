"""
Progress Tracker Module
Handles progress display, VRAM monitoring, logging systems, and performance tracking
"""

import time
import sys
import logging
from datetime import timedelta
from pathlib import Path
from config.config import *

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_dir):
    """Setup logging configuration"""
    log_file = log_dir / "chunk_validation.log"

    # Clear existing log
    open(log_file, 'w').close()

    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='w'  # Overwrite existing log
    )

    # Also log to console for important messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

def log_console(message, color=None):
    """Log to both console and file with optional color"""
    color_codes = {
        "RED": RED, "GREEN": GREEN, "YELLOW": YELLOW,
        "CYAN": CYAN, "BOLD": BOLD, "RESET": RESET
    }

    prefix = color_codes.get(color, "")
    suffix = RESET if color else ""

    print(f"{prefix}{message}{suffix}")
    logging.info(message)

def log_run(message, log_path):
    """Log to run file"""
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(message + "\n")

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

def log_chunk_progress(i, total_chunks, start_time, total_audio_duration=0.0):
    """Enhanced progress logging with accurate realtime factor"""
    elapsed = time.time() - start_time
    avg_time = elapsed / (i + 1)
    eta = avg_time * total_chunks
    remaining = eta - elapsed

    def fmt(seconds):
        return str(timedelta(seconds=int(seconds)))

    # Show VRAM usage in progress
    allocated, _ = monitor_vram_usage("chunk_progress")

    # Calculate ACCURATE realtime factor using actual audio duration
    if total_audio_duration > 0 and elapsed > 0:
        actual_realtime = total_audio_duration / elapsed
        realtime_str = f"{GREEN}{actual_realtime:.2f}x{RESET}"
        audio_str = f" | Audio: {GREEN}{fmt(total_audio_duration)}{RESET}"
    else:
        actual_realtime = 0.0  # Default value when calculating
        realtime_str = f"{YELLOW}Calculating...{RESET}"
        audio_str = ""

    # Force immediate output with explicit flushing
    progress_msg = (f"\n🌀 Chunk {i+1}/{total_chunks} | ⏱ Elapsed: {CYAN}{fmt(elapsed)}{RESET} | "
                   f"ETA: {CYAN}{fmt(eta)}{RESET} | Remaining: {YELLOW}{fmt(remaining)}{RESET} | "
                   f"Realtime: {realtime_str} | VRAM: {GREEN}{allocated:.1f}GB{RESET}{audio_str}")

    print(progress_msg)
    sys.stdout.flush()  # Force immediate output
    
    # Create clean status message for GUI (without ANSI color codes)
    realtime_display = f"{actual_realtime:.2f}x" if actual_realtime > 0 else "Calculating..."
    clean_status = (f"Elapsed: {fmt(elapsed)} | ETA: {fmt(eta)} | Remaining: {fmt(remaining)} | "
                   f"Realtime: {realtime_display} | VRAM: {allocated:.1f}GB" +
                   (f" | Audio: {fmt(total_audio_duration)}" if total_audio_duration > 0 else ""))
    
    # Emit status to GUI if callback is available
    if hasattr(log_chunk_progress, '_status_callback') and log_chunk_progress._status_callback:
        log_chunk_progress._status_callback(clean_status)

    # Also log to file for debugging
    realtime_log = f"{actual_realtime:.2f}x" if actual_realtime > 0 else "N/A"
    logging.info(f"Progress: Chunk {i+1}/{total_chunks}, Elapsed: {fmt(elapsed)}, "
                f"ETA: {fmt(eta)}, Realtime: {realtime_log}, "
                f"Audio Duration: {fmt(total_audio_duration)}, VRAM: {allocated:.1f}GB")

def display_batch_progress(batch_start, batch_end, total_chunks):
    """Display batch processing progress"""
    batch_progress = (batch_end / total_chunks) * 100
    print(f"\n📊 Batch Progress: {batch_start+1}-{batch_end}/{total_chunks} ({batch_progress:.1f}%)")

def display_final_summary(elapsed_time, audio_duration, chunk_count, realtime_factor):
    """Display final processing summary"""
    elapsed_td = timedelta(seconds=int(elapsed_time))
    audio_td = timedelta(seconds=int(audio_duration))

    print(f"\n🎉 {GREEN}Processing Complete!{RESET}")
    print(f"📊 Final Statistics:")
    print(f"   ⏱️ Processing Time: {CYAN}{elapsed_td}{RESET}")
    print(f"   🎵 Audio Duration: {GREEN}{audio_td}{RESET}")
    print(f"   📦 Total Chunks: {YELLOW}{chunk_count}{RESET}")
    print(f"   🚀 Realtime Factor: {BOLD}{realtime_factor:.2f}x{RESET}")
    print(f"   💾 Memory Efficiency: {GREEN}Optimized{RESET}")

# ============================================================================
# VRAM AND PERFORMANCE MONITORING
# ============================================================================

def monitor_vram_usage(operation_name=""):
    """Real-time VRAM monitoring with threshold warnings"""
    import torch

    if not torch.cuda.is_available():
        return 0, 0

    allocated = torch.cuda.memory_allocated() / 1024**3
    reserved = torch.cuda.memory_reserved() / 1024**3

    if allocated > VRAM_SAFETY_THRESHOLD:
        logging.warning(f"⚠️ High VRAM usage during {operation_name}: {allocated:.1f}GB allocated, {reserved:.1f}GB reserved")
        # Trigger memory optimization if available
        optimize_memory_if_needed()

    return allocated, reserved

def monitor_gpu_utilization():
    """Monitor GPU utilization if pynvml is available"""
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

        return {
            "gpu_util": util.gpu,
            "memory_util": util.memory,
            "temperature": temp
        }
    except:
        return {"gpu_util": "N/A", "memory_util": "N/A", "temperature": "N/A"}

def optimize_memory_if_needed():
    """Trigger memory optimization when thresholds are exceeded"""
    import torch
    import gc

    torch.cuda.empty_cache()
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.ipc_collect()

def display_system_info():
    """Display system information at startup"""
    import torch

    print(f"\n🖥️ {CYAN}System Information:{RESET}")

    # CUDA info
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"   GPU: {GREEN}{gpu_name}{RESET}")
        print(f"   VRAM: {GREEN}{total_vram:.1f}GB{RESET}")
        print(f"   CUDA Version: {GREEN}{torch.version.cuda}{RESET}")
    else:
        print(f"   GPU: {RED}Not Available{RESET}")

    # Memory threshold
    print(f"   VRAM Safety Threshold: {YELLOW}{VRAM_SAFETY_THRESHOLD}GB{RESET}")

    # Worker configuration
    print(f"   Max Workers: {YELLOW}{MAX_WORKERS}{RESET}")
    print(f"   Dynamic Workers: {YELLOW}{USE_DYNAMIC_WORKERS}{RESET}")

# ============================================================================
# PERFORMANCE TRACKING
# ============================================================================

class PerformanceTracker:
    """Track performance metrics throughout processing"""

    def __init__(self):
        self.start_time = time.time()
        self.chunk_times = []
        self.vram_usage = []
        self.batch_times = []

    def log_chunk_completion(self, chunk_index, audio_duration):
        """Log individual chunk completion"""
        current_time = time.time()
        chunk_time = current_time - (self.start_time + sum(self.chunk_times))

        self.chunk_times.append(chunk_time)

        # Track VRAM
        allocated, reserved = monitor_vram_usage()
        self.vram_usage.append((chunk_index, allocated, reserved))

    def log_batch_completion(self, batch_size):
        """Log batch completion"""
        if len(self.chunk_times) >= batch_size:
            batch_time = sum(self.chunk_times[-batch_size:])
            self.batch_times.append(batch_time)

    def get_performance_summary(self):
        """Get comprehensive performance summary"""
        total_time = time.time() - self.start_time
        avg_chunk_time = sum(self.chunk_times) / len(self.chunk_times) if self.chunk_times else 0

        vram_peak = max([usage[1] for usage in self.vram_usage]) if self.vram_usage else 0
        vram_avg = sum([usage[1] for usage in self.vram_usage]) / len(self.vram_usage) if self.vram_usage else 0

        return {
            "total_time": total_time,
            "avg_chunk_time": avg_chunk_time,
            "total_chunks": len(self.chunk_times),
            "vram_peak": vram_peak,
            "vram_average": vram_avg,
            "batch_count": len(self.batch_times)
        }

# ============================================================================
# ERROR AND WARNING TRACKING
# ============================================================================

def log_processing_error(chunk_id, error_message, error_type="GENERAL"):
    """Log processing errors with categorization"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    error_log = f"[{timestamp}] {error_type} ERROR - Chunk {chunk_id}: {error_message}"

    logging.error(error_log)
    print(f"{RED}❌ Error in chunk {chunk_id}: {error_message}{RESET}")

def log_processing_warning(chunk_id, warning_message, warning_type="GENERAL"):
    """Log processing warnings with categorization"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    warning_log = f"[{timestamp}] {warning_type} WARNING - Chunk {chunk_id}: {warning_message}"

    logging.warning(warning_log)
    print(f"{YELLOW}⚠️ Warning in chunk {chunk_id}: {warning_message}{RESET}")

# ============================================================================
# REAL-TIME STATUS DISPLAY
# ============================================================================

def create_status_line(current_chunk, total_chunks, elapsed_time, realtime_factor, vram_usage):
    """Create a single-line status for real-time updates"""
    progress_percent = (current_chunk / total_chunks) * 100
    elapsed_str = str(timedelta(seconds=int(elapsed_time)))

    status = (f"🔄 {current_chunk}/{total_chunks} ({progress_percent:.1f}%) | "
             f"⏱️ {elapsed_str} | 🚀 {realtime_factor:.2f}x | 💾 {vram_usage:.1f}GB")

    return status

def update_status_line(status_message):
    """Update status line in place"""
    print(f"\r{status_message}", end='', flush=True)

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_performance_report(output_dir, performance_data):
    """Export detailed performance report"""
    report_path = output_dir / "performance_report.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("GenTTS Performance Report\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Processing Summary:\n")
        f.write(f"  Total Processing Time: {timedelta(seconds=int(performance_data['total_time']))}\n")
        f.write(f"  Average Chunk Time: {performance_data['avg_chunk_time']:.2f}s\n")
        f.write(f"  Total Chunks Processed: {performance_data['total_chunks']}\n")
        f.write(f"  Peak VRAM Usage: {performance_data['vram_peak']:.2f}GB\n")
        f.write(f"  Average VRAM Usage: {performance_data['vram_average']:.2f}GB\n")
        f.write(f"  Batch Count: {performance_data['batch_count']}\n")

    return report_path
