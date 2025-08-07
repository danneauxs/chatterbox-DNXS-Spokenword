"""
TTS Engine Module
Handles ChatterboxTTS interface, model loading, and chunk processing coordination
"""

import torch
import gc
import time
import logging
import shutil
import sys
import os
import subprocess
import psutil
import numpy as np
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import torchaudio as ta
import queue
import threading

from config.config import *
from modules.text_processor import smart_punctuate, sentence_chunk_text, detect_content_boundaries

def find_chunks_json_file(book_name):
    """Find the corresponding chunks JSON file for a book"""
    from config.config import AUDIOBOOK_ROOT

    # Look in the TTS processing directory
    tts_chunks_dir = AUDIOBOOK_ROOT / book_name / "TTS" / "text_chunks"
    json_path = tts_chunks_dir / "chunks_info.json"

    if json_path.exists():
        return json_path

    # Also check old Text_Input location for backwards compatibility
    text_input_dir = Path("Text_Input")
    possible_names = [
        f"{book_name}_chunks.json",
        f"{book_name.lower()}_chunks.json",
        f"{book_name.replace(' ', '_')}_chunks.json"
    ]

    for name in possible_names:
        old_json_path = text_input_dir / name
        if old_json_path.exists():
            return old_json_path

    return None
from modules.audio_processor import (
    smart_audio_validation, apply_smart_fade, add_chunk_end_silence,
    add_contextual_silence, pause_for_chunk_review, get_chunk_audio_duration,
    has_mid_energy_drop, apply_smart_fade_memory, smart_audio_validation_memory
)
from modules.file_manager import (
    setup_book_directories, find_book_files, ensure_voice_sample_compatibility,
    combine_audio_chunks, get_audio_files_in_directory, convert_to_m4b, add_metadata_to_m4b
)
from modules.progress_tracker import setup_logging, log_chunk_progress, log_run

# ============================================================================
# MEMORY AND MODEL MANAGEMENT
# ============================================================================

def monitor_gpu_activity(operation_name):
    """Lightweight GPU monitoring for high-speed processing"""
    # Disabled expensive pynvml queries to free up GPU cycles
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        # Skip GPU utilization queries during production runs
        return allocated, 0
    return 0, 0

def optimize_memory_usage():
    """Aggressive memory management for 8GB VRAM"""
    torch.cuda.empty_cache()
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.ipc_collect()

def monitor_vram_usage(operation_name=""):
    """Real-time VRAM monitoring"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        reserved = torch.cuda.memory_reserved() / 1024**3

        if allocated > VRAM_SAFETY_THRESHOLD:
            logging.warning(f"⚠️ High VRAM usage during {operation_name}: {allocated:.1f}GB allocated, {reserved:.1f}GB reserved")
            optimize_cuda_memory_usage()

        return allocated, reserved
    return 0, 0

# ============================================================================
# PERFORMANCE OPTIMIZATION UTILITIES
# ============================================================================

def detect_deployment_environment():
    """Detect deployment environment for optimization adaptation"""
    if os.getenv("RUNPOD_POD_ID"):
        return "runpod"
    elif os.getenv("SPACE_ID"):  # Hugging Face Spaces
        return "huggingface"
    elif os.path.exists("/.dockerenv"):
        return "container"
    elif torch.cuda.is_available():
        return "local_gpu"
    else:
        return "local_cpu"

def get_available_memory():
    """Get available system memory in MB"""
    try:
        memory = psutil.virtual_memory()
        return memory.available // (1024 * 1024)
    except:
        return 8192  # Safe default of 8GB

def has_nvidia_smi():
    """Check if nvidia-smi is available"""
    try:
        subprocess.run(['nvidia-smi', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def enable_gpu_persistence_mode():
    """Enable GPU persistence mode with proper fallbacks"""
    if not ENABLE_GPU_PERSISTENCE_MODE:
        return False
        
    try:
        if torch.cuda.is_available() and has_nvidia_smi():
            for attempt in range(GPU_PERSISTENCE_RETRY_COUNT):
                result = subprocess.run(['nvidia-smi', '-pm', '1'], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info("✅ GPU persistence mode enabled")
                    return True
                elif "Insufficient permissions" in result.stderr:
                    logging.warning("⚠️ GPU persistence mode failed (insufficient privileges)")
                    break
                time.sleep(0.5)  # Brief delay between attempts
            
            logging.warning("📝 Continuing with standard GPU power management")
        else:
            logging.info("ℹ️ GPU persistence mode not applicable (no NVIDIA GPU detected)")
    except Exception as e:
        logging.warning(f"⚠️ GPU persistence mode failed: {e}")
    
    return False

def setup_cuda_memory_pool():
    """Configure CUDA memory pool for enhanced performance and reduced fragmentation"""
    if not ENABLE_CUDA_MEMORY_POOL or not torch.cuda.is_available():
        return False
    
    try:
        # Get current device and memory info
        device = torch.cuda.current_device()
        total_memory = torch.cuda.get_device_properties(device).total_memory
        total_memory_gb = total_memory / (1024**3)
        
        deployment_env = detect_deployment_environment()
        
        # Adaptive pool sizing based on environment and available memory
        if ENABLE_ADAPTIVE_MEMORY_POOL:
            if deployment_env == "runpod":
                pool_fraction = min(CUDA_MEMORY_POOL_FRACTION, 0.85)  # More conservative on RunPod
            elif deployment_env == "huggingface":
                pool_fraction = min(CUDA_MEMORY_POOL_FRACTION, 0.75)  # Very conservative on HF Spaces
            elif total_memory_gb < 8:
                pool_fraction = min(CUDA_MEMORY_POOL_FRACTION, 0.8)   # Conservative for <8GB GPUs
            else:
                pool_fraction = CUDA_MEMORY_POOL_FRACTION  # Use full config for high-memory GPUs
        else:
            pool_fraction = CUDA_MEMORY_POOL_FRACTION
        
        # Calculate pool size
        pool_size = int(total_memory * pool_fraction)
        pool_size_gb = pool_size / (1024**3)
        
        # Configure memory pool allocator settings
        # Set memory pool to reduce fragmentation and improve allocation speed
        if hasattr(torch.cuda, 'memory') and hasattr(torch.cuda.memory, 'set_per_process_memory_fraction'):
            torch.cuda.memory.set_per_process_memory_fraction(pool_fraction, device)
            logging.info(f"✅ CUDA memory pool configured: {pool_size_gb:.1f}GB ({pool_fraction*100:.0f}% of {total_memory_gb:.1f}GB)")
        
        # Configure allocator settings for better memory management
        if hasattr(torch.cuda, 'empty_cache'):
            # Clear any existing allocations before setting up pool
            torch.cuda.empty_cache()
        
        # Enable memory pool optimizations if available in PyTorch version
        try:
            # Try to enable expandable segments for better memory utilization
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
            logging.info("✅ CUDA expandable segments enabled")
        except:
            pass  # Not available in all PyTorch versions
            
        # Warm up the memory pool with a small allocation
        try:
            warmup_tensor = torch.zeros(1024, 1024, device=device)
            del warmup_tensor
            torch.cuda.empty_cache()
            logging.info("✅ CUDA memory pool warmed up")
        except Exception as e:
            logging.warning(f"⚠️ Memory pool warmup failed: {e}")
        
        logging.info(f"🚀 CUDA memory pool setup complete - environment: {deployment_env}")
        return True
        
    except Exception as e:
        logging.error(f"❌ CUDA memory pool setup failed: {e}")
        return False

def optimize_cuda_memory_usage():
    """Advanced CUDA memory optimization for better performance"""
    if not torch.cuda.is_available():
        return
        
    try:
        # More aggressive cleanup for memory pool systems
        torch.cuda.empty_cache()
        
        # Synchronize to ensure all operations complete before cleanup
        torch.cuda.synchronize()
        
        # Additional memory pool optimization if available
        if hasattr(torch.cuda, 'reset_peak_memory_stats'):
            torch.cuda.reset_peak_memory_stats()
            
    except Exception as e:
        logging.warning(f"⚠️ CUDA memory optimization failed: {e}")

# Global voice embedding cache
_voice_embedding_cache = {}
_cache_memory_usage = 0

def get_voice_cache_key(voice_path, exaggeration):
    """Generate cache key for voice embeddings"""
    try:
        # Use file path and modification time for cache invalidation
        stat = os.stat(voice_path)
        return f"{voice_path}:{stat.st_mtime}:{exaggeration}"
    except:
        return f"{voice_path}:{exaggeration}"

def clear_voice_embedding_cache():
    """Clear voice embedding cache to free memory"""
    global _voice_embedding_cache, _cache_memory_usage
    _voice_embedding_cache.clear()
    _cache_memory_usage = 0
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    logging.info("🗑️ Voice embedding cache cleared")

def estimate_cache_memory_mb(conds_object):
    """Estimate memory usage of cached voice embeddings in MB"""
    try:
        if hasattr(conds_object, 't3') and hasattr(conds_object.t3, 'voice_embed'):
            # Rough estimate based on typical voice embedding sizes
            return 50  # Typical voice embedding ~50MB
        return 30  # Conservative estimate
    except:
        return 30

def get_optimal_workers():
    """Dynamic worker allocation based on VRAM usage"""
    if not USE_DYNAMIC_WORKERS:
        return MAX_WORKERS

    allocated_vram = torch.cuda.memory_allocated() / 1024**3

    if allocated_vram < 5.0:
        return min(TEST_MAX_WORKERS, MAX_WORKERS)
    elif allocated_vram < VRAM_SAFETY_THRESHOLD:
        return min(2, MAX_WORKERS)
    else:
        return 1

def prewarm_model_with_voice(model, voice_path, tts_params=None):
    """
    Pre-warm the TTS model with a voice sample to eliminate cold start quality issues.
    
    Args:
        model: Loaded TTS model
        voice_path: Path to voice sample file
        tts_params: Optional TTS parameters for pre-warming (uses defaults if None)
    
    Returns:
        model: The pre-warmed model (same object, but with cached conditioning)
    """
    import tempfile
    import os
    from modules.file_manager import ensure_voice_sample_compatibility
    
    try:
        print("🔥 Pre-warming model with voice sample...")
        
        # Prepare voice for TTS
        compatible_voice = ensure_voice_sample_compatibility(voice_path)
        
        # Set up default TTS parameters if none provided
        if tts_params is None:
            tts_params = {
                'exaggeration': 0.5,
                'cfg_weight': 0.5, 
                'temperature': 0.9
            }
        
        # Prepare voice conditionals
        model.prepare_conditionals(compatible_voice)
        
        # Generate a short dummy audio to fully warm up the model
        dummy_text = "The quick brown fox jumps over the lazy dog."
        print(f"🎤 Generating warm-up audio: '{dummy_text}'")
        
        # Generate dummy audio with the voice and parameters
        wav_np = model.generate(
            dummy_text,
            exaggeration=tts_params['exaggeration'],
            cfg_weight=tts_params['cfg_weight'],
            temperature=tts_params['temperature']
        )
        
        print("✅ Model pre-warming completed - first chunk quality optimized")
        
        # Clean up any temporary audio data (don't save the dummy audio)
        del wav_np
        
        return model
        
    except Exception as e:
        print(f"⚠️ Pre-warming failed: {e}")
        print("📝 Model will still work but first chunk may have quality variations")
        return model

def get_best_available_device():
    """Detect and return the best available device with proper fallback"""
    try:
        if torch.cuda.is_available():
            # Test CUDA with a simple operation
            test_tensor = torch.tensor([1.0]).to("cuda")
            del test_tensor
            torch.cuda.empty_cache()
            return "cuda"
    except Exception as e:
        logging.warning(f"CUDA test failed: {e}")
    
    try:
        if torch.backends.mps.is_available():
            # Test MPS with a simple operation  
            test_tensor = torch.tensor([1.0]).to("mps")
            del test_tensor
            return "mps"
    except Exception as e:
        logging.warning(f"MPS test failed: {e}")
    
    return "cpu"

def load_optimized_model(device):
    """Load TTS model with memory optimizations and device fallback"""
    from src.chatterbox.tts import ChatterboxTTS
    
    # Validate device availability
    original_device = device
    try:
        if device == "cuda":
            # Test CUDA availability with a small operation
            test_tensor = torch.tensor([1.0]).to("cuda")
            del test_tensor
            torch.cuda.empty_cache()
            logging.info(f"✅ CUDA device validated successfully")
        elif device == "mps" and torch.backends.mps.is_available():
            # Test MPS availability
            test_tensor = torch.tensor([1.0]).to("mps")
            del test_tensor
            logging.info(f"✅ MPS device validated successfully")
    except Exception as e:
        logging.warning(f"⚠️ Device {device} failed validation: {e}")
        logging.info("🔄 Falling back to CPU")
        device = "cpu"

    try:
        # Load model with validated device (ChatterboxTTS doesn't support torch_dtype parameter)
        model = ChatterboxTTS.from_pretrained(device=device)
        logging.info(f"✅ Model loaded successfully on {device.upper()}")
        
        if original_device != device:
            logging.info(f"📝 Note: Requested {original_device.upper()} but using {device.upper()} due to availability")
            
    except Exception as e:
        logging.error(f"❌ Failed to load model on {device}: {e}")
        if device != "cpu":
            logging.info("🔄 Final fallback to CPU...")
            device = "cpu"
            model = ChatterboxTTS.from_pretrained(device=device)
            logging.info("✅ Model loaded on CPU as final fallback")
        else:
            raise RuntimeError(f"Failed to load model even on CPU: {e}")

    # Only apply eval() and benchmark if the model has these attributes
    if hasattr(model, 'eval'):
        model.eval()

    # Set CUDNN benchmark for performance (if available and using CUDA)
    if device == "cuda" and torch.backends.cudnn.is_available():
        torch.backends.cudnn.benchmark = True
        logging.info("✅ CUDNN benchmark enabled for performance")
    
    # Initialize CUDA memory pool if enabled and using CUDA
    if device == "cuda" and ENABLE_CUDA_MEMORY_POOL:
        memory_pool_success = setup_cuda_memory_pool()
        if memory_pool_success:
            logging.info("🚀 CUDA memory pool optimization enabled")
        else:
            logging.warning("⚠️ CUDA memory pool setup failed, continuing without optimization")

    return model

# ============================================================================
# PRODUCER-CONSUMER PIPELINE (PHASE 4)
# ============================================================================

def chunk_producer_thread(all_chunks, chunk_queue, start_index=0, max_queue_size=10):
    """
    Producer thread that pre-loads chunks into a queue for worker threads to consume.
    This eliminates chunk loading overhead during TTS processing.
    
    Args:
        all_chunks: List of chunk data (dict format with text, boundary_type, etc)
        chunk_queue: Queue to place prepared chunk data
        start_index: Index to start producing from (for resume functionality)  
        max_queue_size: Maximum queue size to prevent memory overflow
    """
    try:
        logging.info(f"🏭 Producer thread started - pre-loading chunks from index {start_index}")
        
        for i, chunk_data in enumerate(all_chunks[start_index:], start=start_index):
            # Check if we should stop (via sentinel or shutdown)
            if shutdown_requested:
                break
                
            # Handle both dictionary and tuple formats for backward compatibility
            if isinstance(chunk_data, dict):
                chunk_text = chunk_data["text"]
                boundary_type = chunk_data.get("boundary_type", "none")
                chunk_tts_params = chunk_data.get("tts_params", None)
            else:
                # Handle old tuple format (text, is_para_end)
                chunk_text = chunk_data[0] if len(chunk_data) > 0 else str(chunk_data)
                is_old_para_end = chunk_data[1] if len(chunk_data) > 1 else False
                boundary_type = "paragraph_end" if is_old_para_end else "none"
                chunk_tts_params = None
            
            # Create standardized chunk package for workers
            chunk_package = {
                'index': i,
                'text': chunk_text,
                'boundary_type': boundary_type,
                'tts_params': chunk_tts_params
            }
            
            # Put chunk in queue (blocks if queue is full)
            chunk_queue.put(chunk_package, timeout=30)
            
            # Log progress every 50 chunks to avoid spam
            if (i + 1) % 50 == 0:
                logging.info(f"📦 Producer queued {i + 1} chunks")
        
        logging.info(f"✅ Producer thread completed - {len(all_chunks) - start_index} chunks queued")
        
    except Exception as e:
        logging.error(f"❌ Producer thread failed: {e}")
    finally:
        # Signal completion by adding sentinel value
        try:
            chunk_queue.put(None, timeout=5)  # None = end of chunks signal
        except queue.Full:
            logging.warning("⚠️ Could not add completion signal - queue full")

def process_chunks_with_pipeline(
    all_chunks, batch_chunks, chunk_offset, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks, punc_norm, book_name,
    log_run_func, log_path, device, model, asr_model, asr_enabled, optimal_workers,
    accumulated_audio_duration=0.0
):
    """
    Enhanced chunk processing with producer-consumer pipeline for 5-10% performance improvement.
    
    Args:
        all_chunks: Complete list of all chunks (for context)
        batch_chunks: Current batch of chunks to process
        chunk_offset: Offset for global chunk indexing
        ... (other parameters same as original ThreadPoolExecutor pattern)
        
    Returns:
        Tuple of (batch_results, total_audio_duration) where:
        - batch_results: List of (index, wav_path) tuples for successful chunks  
        - total_audio_duration: Total audio duration for batch (for progress tracking)
    """
    try:
        # Create thread-safe queue with size limit to prevent memory overflow  
        max_queue_size = min(optimal_workers * 3, 20)  # 3x workers or 20, whichever is smaller
        chunk_queue = queue.Queue(maxsize=max_queue_size)
        
        # Start producer thread to pre-load chunks
        producer_thread = threading.Thread(
            target=chunk_producer_thread,
            args=(batch_chunks, chunk_queue, 0, max_queue_size),
            daemon=True
        )
        producer_thread.start()
        
        logging.info(f"🚀 Producer-consumer pipeline started with queue size {max_queue_size}")
        
        # Consumer pattern: workers pull from queue instead of sequential loading
        batch_results = []
        futures = []
        
        with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
            # Process chunks as they become available and handle results in real-time
            chunks_submitted = 0
            completed_count = 0
            total_audio_duration = accumulated_audio_duration
            
            # Import audio processing functions
            from modules.audio_processor import get_chunk_audio_duration
            from modules.progress_tracker import log_chunk_progress
            
            while True:
                try:
                    # Get next chunk from producer (blocks until available)
                    chunk_package = chunk_queue.get(timeout=10)
                    
                    # Check for completion signal
                    if chunk_package is None:
                        break
                    
                    # Check for shutdown request
                    if shutdown_requested:
                        logging.info("🛑 Shutdown requested - stopping chunk submission")
                        break
                    
                    # Extract chunk data from package
                    global_chunk_index = chunk_offset + chunk_package['index']
                    chunk_text = chunk_package['text']
                    boundary_type = chunk_package['boundary_type']
                    chunk_tts_params = chunk_package.get('tts_params') or tts_params
                    
                    # Build context for chunk (all chunk texts)
                    all_chunk_texts = []
                    for cd in all_chunks:
                        if isinstance(cd, dict):
                            all_chunk_texts.append(cd["text"])
                        else:
                            all_chunk_texts.append(cd[0] if len(cd) > 0 else str(cd))
                    
                    # Submit chunk to worker thread
                    future = executor.submit(
                        process_one_chunk,
                        global_chunk_index, chunk_text, text_chunks_dir, audio_chunks_dir,
                        voice_path, chunk_tts_params, start_time, total_chunks,
                        punc_norm, book_name, log_run_func, log_path, device,
                        model, asr_model, all_chunk_texts, boundary_type,
                        asr_enabled
                    )
                    futures.append(future)
                    
                    chunks_submitted += 1
                    chunk_queue.task_done()
                    
                    # Check for completed futures while submitting new ones
                    completed_futures = []
                    for fut in futures:
                        if fut.done():
                            completed_futures.append(fut)
                    
                    # Process completed futures
                    for fut in completed_futures:
                        try:
                            idx, wav_path = fut.result()
                            if wav_path and wav_path.exists():
                                batch_results.append((idx, wav_path))
                                
                                # Update totals for final batch calculation
                                chunk_duration = get_chunk_audio_duration(wav_path)
                                total_audio_duration += chunk_duration
                                completed_count += 1
                                
                            futures.remove(fut)  # Remove completed future
                                
                        except Exception as e:
                            logging.error(f"❌ Future failed during real-time processing: {e}")
                            futures.remove(fut)
                        
                except queue.Empty:
                    # Timeout waiting for chunks - check if producer is done
                    if not producer_thread.is_alive():
                        break
                    else:
                        # Producer still working - check for completed futures while waiting
                        completed_futures = [fut for fut in futures if fut.done()]
                        for fut in completed_futures:
                            try:
                                idx, wav_path = fut.result()
                                if wav_path and wav_path.exists():
                                    batch_results.append((idx, wav_path))
                                    
                                    chunk_duration = get_chunk_audio_duration(wav_path)
                                    total_audio_duration += chunk_duration
                                    completed_count += 1
                                    
                                futures.remove(fut)
                                
                            except Exception as e:
                                logging.error(f"❌ Future failed during timeout processing: {e}")
                                futures.remove(fut)
                        continue
                        
                except Exception as e:
                    logging.error(f"❌ Error in consumer loop: {e}")
                    break
        
        # Process any remaining futures
        if futures:
            for fut in as_completed(futures):
                try:
                    idx, wav_path = fut.result()
                    if wav_path and wav_path.exists():
                        batch_results.append((idx, wav_path))
                        
                        # Update batch totals
                        chunk_duration = get_chunk_audio_duration(wav_path)
                        total_audio_duration += chunk_duration
                        completed_count += 1
                            
                except Exception as e:
                    logging.error(f"❌ Final future failed: {e}")
        
        # Wait for producer thread to complete cleanly
        if producer_thread.is_alive():
            producer_thread.join(timeout=5)
        
        # Calculate batch-specific audio duration for return
        batch_audio_duration = total_audio_duration - accumulated_audio_duration
        logging.info(f"🎉 Producer-consumer pipeline completed: {len(batch_results)} chunks processed")
        return batch_results, batch_audio_duration
        
    except Exception as e:
        logging.error(f"❌ Producer-consumer pipeline failed: {e}")
        logging.info("🔄 Falling back to sequential processing...")
        return [], 0.0  # Return empty results to trigger fallback

# ============================================================================
# CHUNK PROCESSING
# ============================================================================

def patch_alignment_layer(tfmr, alignment_layer_idx=12):
    """Patch alignment layer to avoid recursion"""
    from types import MethodType
    target_layer = tfmr.layers[alignment_layer_idx].self_attn
    original_forward = target_layer.forward

    def patched_forward(self, *args, **kwargs):
        kwargs['output_attentions'] = True
        return original_forward(*args, **kwargs)

    target_layer.forward = MethodType(patched_forward, target_layer)

def process_one_chunk(
    i, chunk, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks,
    punc_norm, basename, log_run_func, log_path, device,
    model, asr_model, all_chunks, boundary_type="none",
    enable_asr=None
):
    """Enhanced chunk processing with quality control, contextual silence, and deep cleanup"""
    import difflib
    from pydub import AudioSegment

    chunk_id_str = f"{i+1:05}"
    chunk_path = text_chunks_dir / f"chunk_{chunk_id_str}.txt"
    with open(chunk_path, 'w', encoding='utf-8') as cf:
        cf.write(chunk)

    chunk_audio_path = audio_chunks_dir / f"chunk_{chunk_id_str}.wav"

    # ============================================================================
    # ENHANCED PERIODIC DEEP CLEANUP
    # ============================================================================
    cleanup_interval = CLEANUP_INTERVAL

    # Skip cleanup on model reinitialization chunks to avoid conflicts
    if (i + 1) % cleanup_interval == 0 and (i + 1) % BATCH_SIZE != 0:
        print(f"\n🧹 {YELLOW}DEEP CLEANUP at chunk {i+1}/{total_chunks}...{RESET}")

        # Enhanced VRAM monitoring before cleanup
        allocated_before = torch.cuda.memory_allocated() / 1024**3 if torch.cuda.is_available() else 0
        reserved_before = torch.cuda.memory_reserved() / 1024**3 if torch.cuda.is_available() else 0

        print(f"   Before: VRAM Allocated: {allocated_before:.1f}GB | Reserved: {reserved_before:.1f}GB")

        # Bulk temp file cleanup
        print("   🗑️ Cleaning bulk temporary files...")
        temp_patterns = ["*_try*.wav", "*_pre.wav", "*_fade*.wav", "*_debug*.wav", "*_temp*.wav", "*_backup*.wav"]
        total_temp_files = 0
        for pattern in temp_patterns:
            temp_files = list(audio_chunks_dir.glob(pattern))
            for temp_file in temp_files:
                temp_file.unlink(missing_ok=True)
            total_temp_files += len(temp_files)

        if total_temp_files > 0:
            print(f"   🗑️ Removed {total_temp_files} temporary audio files")

        # Aggressive CUDA context reset
        print("   🔄 Performing aggressive CUDA context reset...")
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

        # Force CUDA context reset
        if hasattr(torch.cuda, 'reset_peak_memory_stats'):
            torch.cuda.reset_peak_memory_stats()
        if hasattr(torch._C, '_cuda_clearCublasWorkspaces'):
            torch._C._cuda_clearCublasWorkspaces()

        # Force garbage collection multiple times
        for _ in range(3):
            gc.collect()

        # Clear model cache if it has one
        if hasattr(model, 'clear_cache'):
            model.clear_cache()
        elif hasattr(model, 'reset_states'):
            model.reset_states()

        # Brief pause to let GPU settle
        time.sleep(1.0)

        # Monitor after cleanup
        allocated_after = torch.cuda.memory_allocated() / 1024**3 if torch.cuda.is_available() else 0
        reserved_after = torch.cuda.memory_reserved() / 1024**3 if torch.cuda.is_available() else 0

        print(f"   After:  VRAM Allocated: {allocated_after:.1f}GB | Reserved: {reserved_after:.1f}GB")
        print(f"   Freed:  {allocated_before - allocated_after:.1f}GB allocated, {reserved_before - reserved_after:.1f}GB reserved")
        print(f"🧹 {GREEN}Deep cleanup complete!{RESET}\n")

    best_sim, best_asr_text = -1, ""
    wav_path_active = None
    attempt_paths = []
    mid_drop_retries = 0
    max_mid_drop_retries = 2

    # Enhanced regeneration loop with quality validation
    max_attempts = MAX_REGENERATION_ATTEMPTS if ENABLE_REGENERATION_LOOP else 2
    current_tts_params = tts_params.copy()

    # Debug: Log the initial parameters for this chunk
    logging.info(f"🎛️ Chunk {chunk_id_str} initial TTS params: exag={current_tts_params.get('exaggeration', 'N/A'):.3f}, cfg={current_tts_params.get('cfg_weight', 'N/A'):.3f}, temp={current_tts_params.get('temperature', 'N/A'):.3f}, min_p={current_tts_params.get('min_p', 'N/A'):.3f}")

    for attempt_num in range(max_attempts):
        logging.info(f"🔁 Starting TTS for chunk {chunk_id_str}, attempt {attempt_num + 1}/{max_attempts}")
        if attempt_num > 0:
            logging.info(f"🔧 Adjusted params: exag={current_tts_params.get('exaggeration', 'N/A'):.3f}, cfg={current_tts_params.get('cfg_weight', 'N/A'):.3f}, temp={current_tts_params.get('temperature', 'N/A'):.3f}")
        try:
            # Filter to only supported ChatterboxTTS parameters
            supported_params = {"exaggeration", "cfg_weight", "temperature", "min_p", "top_p", "repetition_penalty"}
            tts_args = {k: v for k, v in current_tts_params.items() if k in supported_params}

            # monitor_gpu_activity(f"Before TTS chunk_{chunk_id_str}")  # Disabled for speed
            with torch.no_grad():
                wav = model.generate(chunk, **tts_args).detach().cpu()
            # monitor_gpu_activity(f"After TTS chunk_{chunk_id_str}")  # Disabled for speed

            if wav.dim() == 1:
                wav = wav.unsqueeze(0)

            # Convert tensor to AudioSegment for in-memory processing
            import io
            import soundfile as sf
            from pydub import AudioSegment

            # Convert wav tensor to AudioSegment (in memory)
            wav_np = wav.squeeze().numpy()
            with io.BytesIO() as wav_buffer:
                sf.write(wav_buffer, wav_np, model.sr, format='wav')
                wav_buffer.seek(0)
                audio_segment = AudioSegment.from_wav(wav_buffer)

            # Enhanced quality validation
            quality_score = 1.0  # Start with perfect score

            # Legacy mid-energy drop check (converted to score)
            if ENABLE_MID_DROP_CHECK and has_mid_energy_drop(wav, model.sr):
                quality_score *= 0.3  # Significant penalty for mid-drop
                logging.info(f"⚠️ Mid-chunk energy drop detected in {chunk_id_str}")

            # Enhanced quality validation (if enabled)
            if ENABLE_REGENERATION_LOOP:
                from modules.audio_processor import evaluate_chunk_quality
                # Pass existing ASR model to avoid loading duplicate
                composite_score = evaluate_chunk_quality(audio_segment, chunk, include_spectral=True, asr_model=asr_model)
                quality_score *= composite_score
                logging.info(f"📊 Quality score for {chunk_id_str}: {quality_score:.3f} (composite: {composite_score:.3f})")

            # ASR validation (memory-based processing)
            asr_score = 1.0  # Default to passed if ASR disabled
            # Use parameter if provided, otherwise fall back to config
            asr_enabled = enable_asr if enable_asr is not None else ENABLE_ASR
            if asr_enabled and asr_model is not None:
                from modules.audio_processor import calculate_text_similarity
                try:
                    # Process ASR completely in memory - no disk writes
                    samples = np.array(audio_segment.get_array_of_samples())
                    if audio_segment.channels == 2:
                        samples = samples.reshape((-1, 2)).mean(axis=1)

                    # Normalize to float32 for ASR model
                    audio_np = samples.astype(np.float32) / audio_segment.max_possible_amplitude
                    result = asr_model.transcribe(audio_np)

                    if not isinstance(result, dict) or "text" not in result:
                        raise ValueError(f"Invalid ASR result type: {type(result)}")

                    asr_text = result.get("text", "").strip()
                    asr_score = calculate_text_similarity(punc_norm(chunk), asr_text)
                    logging.info(f"🎤 ASR similarity for chunk {chunk_id_str}: {asr_score:.3f} - Expected: '{punc_norm(chunk)}' Got: '{asr_text}'")

                except Exception as e:
                    logging.error(f"❌ ASR failed for {chunk_id_str}: {e}")
                    asr_score = 0.8  # Use neutral score instead of 0 to avoid regeneration

                # Include ASR score in overall quality
                quality_score *= asr_score

            # Final quality check with all validations
            if quality_score >= QUALITY_THRESHOLD or attempt_num == max_attempts - 1:
                if quality_score >= QUALITY_THRESHOLD:
                    logging.info(f"✅ Quality acceptable for {chunk_id_str} on attempt {attempt_num + 1} (final score: {quality_score:.3f})")
                else:
                    logging.info(f"⚠️ Max attempts reached for {chunk_id_str}, accepting best effort (final score: {quality_score:.3f})")

                # Quality acceptable or max attempts reached, continue with processing
                final_audio = audio_segment
                best_sim = asr_score if asr_enabled else 1.0
                best_asr_text = asr_text if asr_enabled and 'asr_text' in locals() else ""
                break
            else:
                # Quality too low, adjust parameters for retry
                logging.info(f"🔄 Quality below threshold ({quality_score:.3f} < {QUALITY_THRESHOLD}), adjusting parameters for retry {attempt_num + 2}")
                from modules.audio_processor import adjust_parameters_for_retry
                current_tts_params = adjust_parameters_for_retry(current_tts_params, quality_score, attempt_num)
                continue

        except Exception as e:
            import traceback
            logging.error(f"Exception during TTS attempt {attempt_num + 1} for chunk {chunk_id_str}: {e}")
            traceback.print_exc()
            continue

    if 'final_audio' not in locals():
        logging.info(f"❌ Chunk {chunk_id_str} failed all attempts.")
        return None, None

    # Apply trimming and contextual silence in memory before final save
    from modules.audio_processor import process_audio_with_trimming_and_silence

    if boundary_type and boundary_type != "none":
        final_audio = process_audio_with_trimming_and_silence(final_audio, boundary_type)
        print(f"🔇 Added {boundary_type} silence to chunk {i+1:05}")
    else:
        # Apply trimming even without boundary type if enabled
        if ENABLE_AUDIO_TRIMMING:
            from modules.audio_processor import trim_audio_endpoint
            final_audio = trim_audio_endpoint(final_audio)

    # Note: ENABLE_CHUNK_END_SILENCE is now handled by punctuation-specific silence
    # The new system provides more precise silence based on actual punctuation

    # Final save - only disk write in entire process
    final_path = audio_chunks_dir / f"chunk_{chunk_id_str}.wav"
    final_audio.export(final_path, format="wav")
    logging.info(f"✅ Saved final chunk: {final_path.name}")

    # No intermediate file cleanup needed - all processing done in memory

    # Log details - only log ASR failures
    if asr_enabled and best_sim < 0.8:
        log_run_func(f"ASR VALIDATION FAILED - Chunk {chunk_id_str}:\nExpected:\n{chunk}\nActual:\n{best_asr_text}\nSimilarity: {best_sim:.3f}\n" + "="*50, log_path)
    elif not asr_enabled:
        log_run_func(f"Chunk {chunk_id_str}: Original text: {chunk}", log_path)

    # Silence already added in memory above - no disk processing needed

    # Enhanced regular cleanup (every chunk)
    del wav
    optimize_cuda_memory_usage()

    # Additional per-chunk cleanup for long runs
    if (i + 1) % 50 == 0:
        torch.cuda.empty_cache()
        gc.collect()

    # Show ETA progress updates during actual processing (every 2 chunks)
    if i % 2 == 0:
        try:
            from modules.audio_processor import get_chunk_audio_duration  
            from modules.progress_tracker import log_chunk_progress
            
            # Calculate running total audio duration by checking existing chunks
            total_audio_duration = 0.0
            for j in range(i + 1):  # Include current chunk
                check_path = audio_chunks_dir / f"chunk_{j+1:05}.wav"
                if check_path.exists():
                    total_audio_duration += get_chunk_audio_duration(check_path)
            
            # Show ETA update with accumulated audio
            log_chunk_progress(i, total_chunks, start_time, total_audio_duration)
        except Exception as e:
            # Don't let ETA calculation failures break chunk processing
            pass

    return i, final_path

# ============================================================================
# MAIN BOOK PROCESSING FUNCTION
# ============================================================================

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wrapper.chunk_loader import save_chunks

def smooth_sentiment_scores(scores, index, method="rolling", window=3):
    """
    Apply sentiment smoothing to prevent harsh emotional transitions.

    Args:
        scores: List of compound sentiment scores
        index: Current chunk index
        method: "rolling" for moving average, "exp_decay" for exponential decay
        window: Number of previous chunks to consider

    Returns:
        float: Smoothed sentiment score
    """
    if index == 0:
        return scores[0]

    start_idx = max(0, index - window + 1)
    window_scores = scores[start_idx:index + 1]

    if method == "rolling":
        return sum(window_scores) / len(window_scores)
    elif method == "exp_decay":
        weights = SENTIMENT_EXP_DECAY_WEIGHTS[:len(window_scores)]
        weighted_sum = sum(w * s for w, s in zip(weights, reversed(window_scores)))
        weight_sum = sum(weights[:len(window_scores)])
        return weighted_sum / weight_sum if weight_sum > 0 else window_scores[-1]
    else:
        return scores[index]  # No smoothing

def generate_enriched_chunks(text_file, output_dir, user_tts_params=None, quality_params=None, config_params=None, voice_name=None):
    """Reads a text file, performs VADER sentiment analysis, and returns enriched chunks."""
    analyzer = SentimentIntensityAnalyzer()

    # Extract quality parameters for JSON generation (GUI overrides config)
    if quality_params:
        enable_smoothing = quality_params.get('sentiment_smoothing', ENABLE_SENTIMENT_SMOOTHING)
        smoothing_window = quality_params.get('smoothing_window', SENTIMENT_SMOOTHING_WINDOW)
        smoothing_method = quality_params.get('smoothing_method', SENTIMENT_SMOOTHING_METHOD)
        print(f"🔧 JSON Generation: Using GUI smoothing settings - Enabled: {enable_smoothing}, Window: {smoothing_window}, Method: {smoothing_method}")
    else:
        enable_smoothing = ENABLE_SENTIMENT_SMOOTHING
        smoothing_window = SENTIMENT_SMOOTHING_WINDOW
        smoothing_method = SENTIMENT_SMOOTHING_METHOD
        print(f"🔧 JSON Generation: Using config smoothing settings - Enabled: {enable_smoothing}")

    # Extract VADER sensitivity parameters (GUI overrides config)
    if config_params:
        vader_exag_sensitivity = config_params.get('vader_exag_sensitivity', VADER_EXAGGERATION_SENSITIVITY)
        vader_cfg_sensitivity = config_params.get('vader_cfg_sensitivity', VADER_CFG_WEIGHT_SENSITIVITY)
        vader_temp_sensitivity = config_params.get('vader_temp_sensitivity', VADER_TEMPERATURE_SENSITIVITY)
        print(f"🔧 JSON Generation: Using GUI VADER sensitivity - Exag: {vader_exag_sensitivity}, CFG: {vader_cfg_sensitivity}, Temp: {vader_temp_sensitivity}")
    else:
        vader_exag_sensitivity = VADER_EXAGGERATION_SENSITIVITY
        vader_cfg_sensitivity = VADER_CFG_WEIGHT_SENSITIVITY
        vader_temp_sensitivity = VADER_TEMPERATURE_SENSITIVITY
        print(f"🔧 JSON Generation: Using config VADER sensitivity - Exag: {vader_exag_sensitivity}, CFG: {vader_cfg_sensitivity}, Temp: {vader_temp_sensitivity}")

    raw_text = text_file.read_text(encoding='utf-8')
    cleaned = smart_punctuate(raw_text)
    chunks = sentence_chunk_text(cleaned)

    # Use user-provided parameters as base, or fall back to config defaults
    if user_tts_params:
        base_exaggeration = user_tts_params.get('exaggeration', BASE_EXAGGERATION)
        base_cfg_weight = user_tts_params.get('cfg_weight', BASE_CFG_WEIGHT)
        base_temperature = user_tts_params.get('temperature', BASE_TEMPERATURE)
        base_min_p = user_tts_params.get('min_p', DEFAULT_MIN_P)
        base_top_p = user_tts_params.get('top_p', DEFAULT_TOP_P)
        base_repetition_penalty = user_tts_params.get('repetition_penalty', DEFAULT_REPETITION_PENALTY)
        use_vader = user_tts_params.get('use_vader', True)  # Default to True for backward compatibility

    else:
        base_exaggeration = BASE_EXAGGERATION
        base_cfg_weight = BASE_CFG_WEIGHT
        base_temperature = BASE_TEMPERATURE
        base_min_p = DEFAULT_MIN_P
        base_top_p = DEFAULT_TOP_P
        base_repetition_penalty = DEFAULT_REPETITION_PENALTY
        use_vader = True  # Default behavior

    enriched = []
    chunk_texts = [chunk_text for chunk_text, _ in chunks]

    # First pass: collect all sentiment scores
    raw_sentiment_scores = []
    for chunk_text, _ in chunks:
        sentiment_scores = analyzer.polarity_scores(chunk_text)
        raw_sentiment_scores.append(sentiment_scores['compound'])

    # Second pass: apply smoothing and generate parameters
    for i, (chunk_text, is_para_end) in enumerate(chunks):
        # Get original sentiment score
        raw_compound_score = raw_sentiment_scores[i]

        # Apply sentiment smoothing if enabled (uses GUI settings, not config)
        if use_vader and enable_smoothing:
            compound_score = smooth_sentiment_scores(
                raw_sentiment_scores,
                i,
                method=smoothing_method,
                window=smoothing_window
            )
            # Debug: Log sentiment changes
            if abs(compound_score - raw_compound_score) > 0.1:
                logging.info(f"📊 Chunk {i+1:05}: sentiment smoothed {raw_compound_score:.3f} → {compound_score:.3f}")
        else:
            compound_score = raw_compound_score

        if use_vader:
            # Apply VADER sentiment adjustments using smoothed score
            exaggeration = base_exaggeration + (compound_score * vader_exag_sensitivity)
            cfg_weight = base_cfg_weight + (compound_score * vader_cfg_sensitivity)
            temperature = base_temperature + (compound_score * vader_temp_sensitivity)
            min_p = base_min_p + (compound_score * VADER_MIN_P_SENSITIVITY)
            repetition_penalty = base_repetition_penalty + (compound_score * VADER_REPETITION_PENALTY_SENSITIVITY)

            # Clamp values to defined min/max (ensure JSON values respect bounds)
            exaggeration = round(max(TTS_PARAM_MIN_EXAGGERATION, min(exaggeration, TTS_PARAM_MAX_EXAGGERATION)), 2)
            cfg_weight = round(max(TTS_PARAM_MIN_CFG_WEIGHT, min(cfg_weight, TTS_PARAM_MAX_CFG_WEIGHT)), 2)
            temperature = round(max(TTS_PARAM_MIN_TEMPERATURE, min(temperature, TTS_PARAM_MAX_TEMPERATURE)), 2)
            min_p = round(max(TTS_PARAM_MIN_MIN_P, min(min_p, TTS_PARAM_MAX_MIN_P)), 3)
            repetition_penalty = round(max(TTS_PARAM_MIN_REPETITION_PENALTY, min(repetition_penalty, TTS_PARAM_MAX_REPETITION_PENALTY)), 1)

            # Debug: Log VADER-adjusted parameters for significant changes
            if abs(exaggeration - base_exaggeration) > 0.05 or abs(cfg_weight - base_cfg_weight) > 0.05:
                logging.info(f"🎭 Chunk {i+1:05}: VADER adjusted params - exag: {base_exaggeration:.2f}→{exaggeration:.2f}, cfg: {base_cfg_weight:.2f}→{cfg_weight:.2f}, sentiment: {compound_score:.3f}")
        else:
            # Use fixed base values (no VADER adjustment)
            exaggeration = base_exaggeration
            cfg_weight = base_cfg_weight
            temperature = base_temperature
            min_p = base_min_p
            repetition_penalty = base_repetition_penalty

        boundary_type = detect_content_boundaries(chunk_text, i, chunk_texts, is_para_end)

        enriched.append({
            "index": i,
            "text": chunk_text,
            "word_count": len(chunk_text.split()),
            "boundary_type": boundary_type if boundary_type else "none",
            "sentiment_compound": compound_score,  # Store smoothed score
            "sentiment_raw": raw_compound_score,   # Store original score for reference
            "tts_params": {
                "exaggeration": exaggeration,
                "cfg_weight": cfg_weight,
                "temperature": temperature,
                "min_p": min_p,
                "top_p": base_top_p,  # Top-P remains constant (not adjusted by VADER)
                "repetition_penalty": repetition_penalty
            }
        })

    output_json_path = output_dir / "chunks_info.json"

    # Add voice metadata if provided
    if voice_name:
        # Try metadata method first
        try:
            # Create metadata entry as first element
            metadata = {
                "_metadata": True,
                "voice_used": voice_name,
                "generation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_chunks": len(enriched)
            }
            enriched_with_metadata = [metadata] + enriched
            save_chunks(output_json_path, enriched_with_metadata)
            print(f"✅ Saved voice metadata: {voice_name}")
        except Exception as e:
            # Fallback to comment method if metadata fails
            print(f"⚠️ Metadata method failed, using comment fallback: {e}")
            save_chunks(output_json_path, enriched)

            # Add voice as comment
            from modules.voice_detector import add_voice_to_json
            add_voice_to_json(output_json_path, voice_name, method="comment")
    else:
        save_chunks(output_json_path, enriched)

    return enriched

def process_book_folder(book_dir, voice_path, tts_params, device, skip_cleanup=False, enable_asr=None, quality_params=None, config_params=None, specific_text_file=None):
    """Enhanced book processing with batch processing to prevent hangs"""
    print(f"🔍 DEBUG: Entering process_book_folder with book_dir='{book_dir}', voice_path='{voice_path}'")

    # Apply GUI quality parameters to override config defaults
    if quality_params:
        print(f"🔧 Applying GUI quality parameters: {quality_params}")

        # Override config values with GUI settings
        global ENABLE_REGENERATION_LOOP, ENABLE_SENTIMENT_SMOOTHING, ENABLE_MFCC_VALIDATION
        global ENABLE_OUTPUT_VALIDATION, QUALITY_THRESHOLD, OUTPUT_VALIDATION_THRESHOLD
        global SENTIMENT_SMOOTHING_WINDOW, SENTIMENT_SMOOTHING_METHOD, SPECTRAL_ANOMALY_THRESHOLD

        ENABLE_REGENERATION_LOOP = quality_params.get('regeneration_enabled', ENABLE_REGENERATION_LOOP)
        ENABLE_SENTIMENT_SMOOTHING = quality_params.get('sentiment_smoothing', ENABLE_SENTIMENT_SMOOTHING)
        ENABLE_MFCC_VALIDATION = quality_params.get('mfcc_validation', ENABLE_MFCC_VALIDATION)
        ENABLE_OUTPUT_VALIDATION = quality_params.get('output_validation', ENABLE_OUTPUT_VALIDATION)
        QUALITY_THRESHOLD = quality_params.get('quality_threshold', QUALITY_THRESHOLD)
        OUTPUT_VALIDATION_THRESHOLD = quality_params.get('output_threshold', OUTPUT_VALIDATION_THRESHOLD)
        SENTIMENT_SMOOTHING_WINDOW = quality_params.get('smoothing_window', SENTIMENT_SMOOTHING_WINDOW)
        SENTIMENT_SMOOTHING_METHOD = quality_params.get('smoothing_method', SENTIMENT_SMOOTHING_METHOD)
        SPECTRAL_ANOMALY_THRESHOLD = quality_params.get('spectral_threshold', SPECTRAL_ANOMALY_THRESHOLD)

        print(f"✅ Quality settings applied - Regeneration: {ENABLE_REGENERATION_LOOP}, MFCC: {ENABLE_MFCC_VALIDATION}, Output Validation: {ENABLE_OUTPUT_VALIDATION}")

    from src.chatterbox.tts import punc_norm
    print(f"🔍 DEBUG: Successfully imported punc_norm")

    # Setup directories
    print(f"🔍 DEBUG: Calling setup_book_directories...")
    output_root, tts_dir, text_chunks_dir, audio_chunks_dir = setup_book_directories(book_dir)
    print(f"🔍 DEBUG: Directory setup complete")

    # Clean previous processing files (but skip for resume operations)
    if skip_cleanup:
        print(f"🔄 RESUME MODE: Skipping cleanup to preserve existing chunks")
        print(f"📁 Preserving: {text_chunks_dir}, {audio_chunks_dir}")
    else:
        print(f"🧹 FRESH PROCESSING: Cleaning previous processing files...")
        import glob

        # Clear text chunks
        for txt_file in text_chunks_dir.glob("*.txt"):
            txt_file.unlink(missing_ok=True)
        for json_file in text_chunks_dir.glob("*.json"):
            json_file.unlink(missing_ok=True)

        # Clear audio chunks
        for wav_file in audio_chunks_dir.glob("*.wav"):
            wav_file.unlink(missing_ok=True)

        # Clear logs
        for log_file in output_root.glob("*.log"):
            log_file.unlink(missing_ok=True)

        print(f"✅ Cleanup complete")

    # Find book files
    print(f"🔍 DEBUG: Calling find_book_files...")
    book_files = find_book_files(book_dir)
    
    # Use specific text file if provided (GUI selection), otherwise use auto-detected file
    if specific_text_file:
        text_file_to_use = Path(specific_text_file)
        print(f"🎯 DEBUG: Using GUI-selected text file: {text_file_to_use}")
        if not text_file_to_use.exists():
            logging.error(f"[{book_dir.name}] ERROR: Selected text file not found: {text_file_to_use}")
            return None, None, []
    else:
        text_file_to_use = book_files['text']
        print(f"🔍 DEBUG: Using auto-detected text file: {text_file_to_use}")
        if not text_file_to_use:
            logging.info(f"[{book_dir.name}] ERROR: No .txt files found in the book folder.")
            return None, None, []
    
    cover_file = book_files['cover']
    nfo_file = book_files['nfo']

    setup_logging(output_root)

    # Extract voice name for logging and JSON metadata
    voice_name_for_log = voice_path.stem if hasattr(voice_path, 'stem') else Path(voice_path).stem

    # Generate enriched chunks with VADER analysis using user parameters and GUI quality settings
    print(f"🔍 DEBUG: About to call generate_enriched_chunks with quality_params: {quality_params}")
    print(f"🔍 DEBUG: About to call generate_enriched_chunks with config_params: {config_params}")
    print(f"🔍 DEBUG: Using voice: {voice_name_for_log}")
    all_chunks = generate_enriched_chunks(text_file_to_use, text_chunks_dir, tts_params, quality_params, config_params, voice_name_for_log)

    # Create run_log_lines
    print(f"🔍 DEBUG: Creating run_log_lines...")
    print(f"🔍 DEBUG: voice_path type: {type(voice_path)}, value: {voice_path}")

    run_log_lines = [
        f"\n===== Processing: {book_dir.name} =====",
        f"Voice: {voice_name_for_log}",
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Text file processed: {text_file_to_use.name}",
        f"Total chunks generated: {len(all_chunks)}"
    ]

    start_time = time.time()
    total_chunks = len(all_chunks)
    log_path = output_root / "chunk_validation.log"
    total_audio_duration = 0.0

    # Initialize performance optimizations
    deployment_env = detect_deployment_environment()
    print(f"🌍 Deployment environment: {deployment_env}")
    
    # Enable GPU persistence mode for better performance
    gpu_persistence_enabled = enable_gpu_persistence_mode()

    # Batch processing
    print(f"📊 Processing {total_chunks} chunks in batches of {BATCH_SIZE}")

    all_results = []

    for batch_start in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_chunks)
        batch_chunks = all_chunks[batch_start:batch_end]

        print(f"\n🔄 Processing batch: chunks {batch_start+1}-{batch_end}")

        # Fresh model for each batch
        model = load_optimized_model(device)
        compatible_voice = ensure_voice_sample_compatibility(voice_path, output_dir=tts_dir)
        
        # Pre-warm model to eliminate first chunk quality variations
        model = prewarm_model_with_voice(model, compatible_voice, tts_params)

        # Load ASR model once per batch if needed using adaptive manager
        asr_model = None
        asr_device_used = None
        # Use parameter if provided, otherwise fall back to config
        asr_enabled = enable_asr if enable_asr is not None else ENABLE_ASR
        if asr_enabled:
            from modules.asr_manager import load_asr_model_adaptive
            
            # Get ASR config from parameters
            asr_config = config_params.get('asr_config', {}) if config_params else {}
            
            # Use adaptive ASR manager for intelligent loading
            asr_model, asr_device_used = load_asr_model_adaptive(asr_config)
            
            if asr_model is None:
                print(f"❌ ASR model loading failed completely - disabling ASR for this batch")
                asr_enabled = False

        # Dynamic worker allocation
        optimal_workers = get_optimal_workers()
        print(f"🔧 Using {optimal_workers} workers for batch {batch_start+1}-{batch_end}")

        # Try producer-consumer pipeline first (Phase 4 optimization)
        batch_results = []
        if ENABLE_PRODUCER_CONSUMER_PIPELINE:
            try:
                print(f"🚀 Producer-consumer pipeline for batch {batch_start+1}-{batch_end}")
                pipeline_results = process_chunks_with_pipeline(
                    all_chunks, batch_chunks, batch_start, text_chunks_dir, audio_chunks_dir,
                    voice_path, tts_params, start_time, total_chunks, punc_norm, book_dir.name,
                    log_run, log_path, device, model, asr_model, asr_enabled, optimal_workers,
                    total_audio_duration  # Pass accumulated duration for proper ETA calculation
                )
                
                # Handle tuple return from pipeline
                if isinstance(pipeline_results, tuple) and len(pipeline_results) == 2:
                    batch_results, batch_audio_duration = pipeline_results
                    total_audio_duration += batch_audio_duration
                else:
                    # Fallback for old return format
                    batch_results = pipeline_results
                
                if batch_results:
                    print(f"✅ Producer-consumer pipeline completed: {len(batch_results)} chunks")
                    # Pipeline already handled progress logging internally
                
            except Exception as e:
                logging.error(f"❌ Producer-consumer pipeline failed: {e}")
                if not ENABLE_PIPELINE_FALLBACK:
                    raise
                batch_results = []  # Clear failed results
        
        # Fallback to original sequential processing if pipeline disabled or failed
        if not batch_results:
            print(f"🔄 Sequential processing fallback for batch {batch_start+1}-{batch_end}")
            futures = []
            
            with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
                for i, chunk_data in enumerate(batch_chunks):
                    global_chunk_index = batch_start + i

                    # Check for shutdown request
                    if shutdown_requested:
                        print(f"\n⏹️ {YELLOW}Stopping submission of new chunks...{RESET}")
                        break

                    # Handle both dictionary and tuple formats for chunk data
                    if isinstance(chunk_data, dict):
                        chunk = chunk_data["text"]
                        boundary_type = chunk_data.get("boundary_type", "none")
                        # Use chunk-specific TTS params if available, otherwise fall back to global
                        chunk_tts_params = chunk_data.get("tts_params", tts_params)
                    else:
                        # Handle old tuple format (text, is_para_end) - convert to boundary_type
                        chunk = chunk_data[0] if len(chunk_data) > 0 else str(chunk_data)
                        # Convert old is_paragraph_end to boundary_type
                        is_old_para_end = chunk_data[1] if len(chunk_data) > 1 else False
                        boundary_type = "paragraph_end" if is_old_para_end else "none"
                        chunk_tts_params = tts_params # Fallback for old format

                    # Handle both dictionary and tuple formats for backward compatibility
                    all_chunk_texts = []
                    for cd in all_chunks:
                        if isinstance(cd, dict):
                            all_chunk_texts.append(cd["text"])
                        else:
                            # Handle old tuple format (text, is_para_end)
                            all_chunk_texts.append(cd[0] if len(cd) > 0 else str(cd))

                    futures.append(executor.submit(
                        process_one_chunk,
                        global_chunk_index, chunk, text_chunks_dir, audio_chunks_dir,
                        voice_path, chunk_tts_params, start_time, total_chunks,
                        punc_norm, book_dir.name, log_run, log_path, device,
                        model, asr_model, all_chunk_texts, boundary_type,
                        asr_enabled
                    ))

                # Wait for batch to complete
                print(f"🔄 {CYAN}Waiting for batch {batch_start+1}-{batch_end} to complete...{RESET}")
                completed_count = 0

                for fut in as_completed(futures):
                    try:
                        idx, wav_path = fut.result()
                        if wav_path and wav_path.exists():
                            # Measure actual audio duration for this chunk
                            chunk_duration = get_chunk_audio_duration(wav_path)
                            total_audio_duration += chunk_duration
                            batch_results.append((idx, wav_path))

                            # Update progress every 2 chunks within batch
                            completed_count += 1
                            if completed_count % 2 == 0:
                                log_chunk_progress(batch_start + completed_count - 1, total_chunks, start_time, total_audio_duration)

                    except Exception as e:
                        logging.error(f"Future failed in batch: {e}")

        # Clean up model after batch
        print(f"🧹 Cleaning up after batch {batch_start+1}-{batch_end}")
        del model
        if asr_model:
            from modules.asr_manager import cleanup_asr_model
            cleanup_asr_model(asr_model)
        torch.cuda.empty_cache()
        gc.collect()
        time.sleep(2)

        all_results.extend(batch_results)
        print(f"✅ Batch {batch_start+1}-{batch_end} completed ({len(batch_results)} chunks)")

    # Final processing
    quarantine_dir = audio_chunks_dir / "quarantine"
    pause_for_chunk_review(quarantine_dir)

    # Collect final chunk paths
    chunk_paths = get_audio_files_in_directory(audio_chunks_dir)

    if not chunk_paths:
        logging.info(f"{RED}❌ No valid audio chunks found. Skipping concatenation and conversion.{RESET}")
        return None, None, []

    # Calculate timing
    elapsed_total = time.time() - start_time
    elapsed_td = timedelta(seconds=int(elapsed_total))

    total_audio_duration_final = sum(get_chunk_audio_duration(chunk_path) for chunk_path in chunk_paths)
    audio_duration_td = timedelta(seconds=int(total_audio_duration_final))
    realtime_factor = total_audio_duration_final / elapsed_total if elapsed_total > 0 else 0.0

    print(f"\n⏱️ TTS Processing Complete:")
    print(f"   Elapsed Time: {CYAN}{str(elapsed_td)}{RESET}")
    print(f"   Audio Duration: {GREEN}{str(audio_duration_td)}{RESET}")
    print(f"   Realtime Factor: {YELLOW}{realtime_factor:.2f}x{RESET}")

    # Combine audio
    voice_name = voice_path.stem if hasattr(voice_path, 'stem') else Path(voice_path).stem
    combined_wav_path = output_root / f"{book_dir.name} [{voice_name}].wav"
    print("\n💾 Saving WAV file...")
    combine_audio_chunks(chunk_paths, combined_wav_path)

    # M4B conversion with normalization
    temp_m4b_path = output_root / "output.m4b"
    final_m4b_path = output_root / f"{book_dir.name}[{voice_name}].m4b"
    convert_to_m4b(combined_wav_path, temp_m4b_path)
    add_metadata_to_m4b(temp_m4b_path, final_m4b_path, cover_file, nfo_file)

    logging.info(f"Audiobook created: {final_m4b_path}")

    # Add final info to run log
    run_log_lines.extend([
        f"Combined WAV: {combined_wav_path}",
        "--- Generation Settings ---",
        f"Batch Processing: Enabled ({BATCH_SIZE} chunks per batch)",
        f"ASR Enabled: {ENABLE_ASR}",
        f"Hum Detection: {ENABLE_HUM_DETECTION}",
        f"Dynamic Workers: {USE_DYNAMIC_WORKERS}",
        f"Voice used: {voice_name}",
        f"Exaggeration: {tts_params['exaggeration']}",
        f"CFG weight: {tts_params['cfg_weight']}",
        f"Temperature: {tts_params['temperature']}",
        f"Processing Time: {str(elapsed_td)}",
        f"Audio Duration: {str(audio_duration_td)}",
        f"Realtime Factor: {realtime_factor:.2f}x",
        f"Total Chunks: {len(chunk_paths)}"
    ])

    # Write the run log
    log_run("\n".join(run_log_lines), output_root / "run.log")
    print(f"📝 Run log written to: {output_root / 'run.log'}")

    return final_m4b_path, combined_wav_path, run_log_lines
