"""
TTS Engine Module
Handles ChatterboxTTS interface, model loading, and chunk processing coordination
"""

import torch
import threading
import gc
import time
import logging
import shutil
import sys
import numpy as np
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import torchaudio as ta

from config.config import *
from modules.text_processor import smart_punctuate, sentence_chunk_text, detect_content_boundaries

# ============================================================================
# GLOBAL VOICE CACHE FOR PREWARM OPTIMIZATION
# ============================================================================
# Cache to persist voice embeddings across model reloads within a conversion session
_global_voice_cache = None
_voice_cache_info = None
_GPU_INFER_LOCK = threading.Lock()

def clear_voice_cache():
    """Clear the global voice cache at start of new conversion"""
    global _global_voice_cache, _voice_cache_info
    _global_voice_cache = None
    _voice_cache_info = None
    logging.info("🗑️ Voice cache cleared for new conversion session")

def store_voice_cache(model):
    """Store voice embeddings from model to global cache"""
    global _global_voice_cache, _voice_cache_info
    if hasattr(model, 'conds') and model.conds is not None:
        _global_voice_cache = model.conds
        _voice_cache_info = {
            'cached_at': time.time(),
            'cache_size_mb': sys.getsizeof(_global_voice_cache) / 1024 / 1024
        }
        logging.info(f"💾 Voice embeddings cached ({_voice_cache_info['cache_size_mb']:.1f}MB)")
    else:
        logging.warning("⚠️ No voice embeddings found to cache")

def restore_voice_cache(model):
    """Restore voice embeddings from global cache to model"""
    global _global_voice_cache, _voice_cache_info
    if _global_voice_cache is not None:
        model.conds = _global_voice_cache
        logging.info(f"🚀 Voice embeddings restored from cache (skipping {2.9:.1f}s warmup)")
        return True
    else:
        logging.debug("📝 No voice cache available - will need fresh prewarm")
        return False

def get_voice_cache_info():
    """Get information about current voice cache"""
    global _voice_cache_info
    return _voice_cache_info


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
from modules.terminal_logger import start_terminal_logging, stop_terminal_logging
from modules.file_manager import (
    setup_book_directories, find_book_files, ensure_voice_sample_compatibility,
    combine_audio_chunks, get_audio_files_in_directory, convert_to_m4b, add_metadata_to_m4b
)
from modules.progress_tracker import setup_logging, log_chunk_progress, log_run

# Global shutdown flag
shutdown_requested = False

# ---------------------------------------------------------------------------
# Global model cache to prevent double-loading across conversions
# ---------------------------------------------------------------------------
_GLOBAL_TTS_MODEL = None
_GLOBAL_TTS_MODEL_DEVICE = None
_LAST_RUN_SIGNATURE = None
_VOICE_CONDS_CACHE = {}
_FORCE_MODEL_RELOAD = False

# Prewarm tracking (used by legacy cleanup paths)
# Define defaults so cleanup can always safely reset these.
_GLOBAL_TTS_PREWARMED = False
_PREWARMED_KEYS = set()  # e.g., keys of (voice_sig, core_tts_params_sig)

# Capability probe cache: does current model expose a batch API?
_BATCH_API_SUPPORTED = None

def _release_global_tts_model():
    global _GLOBAL_TTS_MODEL, _GLOBAL_TTS_MODEL_DEVICE, _FORCE_MODEL_RELOAD

    # Step 0: Clear optimizer references that may hold model methods
    try:
        from modules.real_tts_optimizer import get_tts_optimizer
        optimizer = get_tts_optimizer()
        if hasattr(optimizer, 'original_methods'):
            optimizer.original_methods.clear()
            print("🧹 Cleared optimizer method references")
        if hasattr(optimizer, 'reset'):
            optimizer.reset()
    except Exception as e:
        print(f"⚠️ Warning during optimizer cleanup: {e}")

    # Step 1: Explicitly clear model subcomponents before deletion
    if _GLOBAL_TTS_MODEL is not None:
        try:
            # Restore original methods if optimizer modified them
            try:
                from modules.real_tts_optimizer import get_tts_optimizer
                optimizer = get_tts_optimizer()
                if hasattr(optimizer, 'restore_original_methods'):
                    optimizer.restore_original_methods(_GLOBAL_TTS_MODEL)
                    print("🔄 Restored original model methods")
            except Exception:
                pass

            # Clear model conditionals if they exist
            if hasattr(_GLOBAL_TTS_MODEL, 'conds'):
                _GLOBAL_TTS_MODEL.conds = None

            # Move model to CPU to release GPU memory
            if hasattr(_GLOBAL_TTS_MODEL, 'cpu'):
                _GLOBAL_TTS_MODEL.cpu()

            # Clear any cached states
            if hasattr(_GLOBAL_TTS_MODEL, 'clear_cache'):
                _GLOBAL_TTS_MODEL.clear_cache()
            elif hasattr(_GLOBAL_TTS_MODEL, 'reset_states'):
                _GLOBAL_TTS_MODEL.reset_states()

            print("🧹 Explicitly cleared model subcomponents")

        except Exception as e:
            print(f"⚠️ Warning during model component cleanup: {e}")

        # Step 2: Delete the model object
        try:
            del _GLOBAL_TTS_MODEL
            print("🗑️ Deleted global TTS model object")
        except Exception as e:
            print(f"❌ Failed to delete model: {e}")

    # Step 3: Clear all global variables
    _GLOBAL_TTS_MODEL = None
    _GLOBAL_TTS_MODEL_DEVICE = None
    _FORCE_MODEL_RELOAD = True

    # Step 4: Clear caches and prewarming state
    global _GLOBAL_TTS_PREWARMED
    _GLOBAL_TTS_PREWARMED = False
    global _PREWARMED_KEYS, _LAST_RUN_SIGNATURE
    _PREWARMED_KEYS.clear()
    _LAST_RUN_SIGNATURE = None

    # Step 5: Forcibly clear voice conditionals cache (may contain GPU tensors)
    if _VOICE_CONDS_CACHE:
        for key, cached_conds in _VOICE_CONDS_CACHE.items():
            try:
                if hasattr(cached_conds, 'cpu'):
                    cached_conds.cpu()
                del cached_conds
            except Exception:
                pass
        _VOICE_CONDS_CACHE.clear()
        print("🧹 Cleared voice conditionals cache")

    # Step 6: Force Python garbage collection
    import gc
    gc.collect()
    gc.collect()  # Call twice to ensure cleanup

    # Step 7: Aggressive CUDA cleanup
    try:
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            # Reset memory stats to clear fragmentation tracking
            if hasattr(torch.cuda, 'reset_peak_memory_stats'):
                torch.cuda.reset_peak_memory_stats()
            print("🧹 Performed aggressive CUDA cleanup")
    except Exception as e:
        print(f"⚠️ CUDA cleanup warning: {e}")

    print("✅ Model release completed - VRAM should be freed")

# Console colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

import random
import numpy as np
import torch

def set_seed(seed_value: int):
    """
    Sets the seed for torch, random, and numpy for reproducibility.
    This is called if a non-zero seed is provided for generation.
    """
    torch.manual_seed(seed_value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)  # if using multi-GPU
    if torch.backends.mps.is_available():
        # Check if torch.mps exists before calling
        if hasattr(torch, 'mps') and torch.mps.is_available():
            torch.mps.manual_seed(seed_value)
    random.seed(seed_value)
    np.random.seed(seed_value)
    logging.info(f"Global seed set to: {seed_value}")

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
            optimize_memory_usage()

        return allocated, reserved
    return 0, 0

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

def _voice_sig(voice_path):
    try:
        vpath = Path(voice_path)
        return (str(vpath.resolve()), vpath.stat().st_mtime_ns)
    except Exception:
        return (str(voice_path), None)


def _core_tts_params_sig(tts_params: dict | None):
    tp = tts_params or {}
    return (
        round(float(tp.get('cfg_weight', 0.5)), 3),
        round(float(tp.get('temperature', 0.85)), 3),
        round(float(tp.get('min_p', 0.05)), 3),
        round(float(tp.get('top_p', 0.9)), 3),
    )


def prewarm_model_with_voice(model, voice_path, tts_params=None):
    """
    Pre-warm the TTS model with a voice sample to eliminate cold start quality issues.
    Uses global voice cache to skip prewarming during model reloads.

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

    # Check if we can restore from cache instead of prewarming
    if restore_voice_cache(model):
        print("✅ Model pre-warming skipped - using cached voice embeddings")
        return model

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
        dummy_text = "sixth sick sheik's sixth sheep's sick, and red leather, yellow leather."

        print(f"🎤 Generating warm-up audio: '{dummy_text}'")

        # Generate dummy audio with the voice and parameters
        # Serialize warm-up GPU generation to avoid allocator races
        with _GPU_INFER_LOCK:
            wav_np = model.generate(
                dummy_text,
                exaggeration=tts_params['exaggeration'],
                cfg_weight=tts_params['cfg_weight'],
                temperature=tts_params['temperature'],
                disable_watermark=True,
            )

        print("✅ Model pre-warming completed - first chunk quality optimized")

        # Store voice embeddings in global cache for future model reloads
        store_voice_cache(model)

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

def load_optimized_model(device, *, force_reload: bool = False):
    """Load TTS model with REAL performance optimizations.

    Priority:
    - If `config.config.CHATTERBOX_CKPT_DIR` (or env var) points to a local checkpoint folder, load from it.
    - Otherwise, fall back to `from_pretrained` (requires network access).
    - Optionally enable ONNX T3 if `ENABLE_T3_ONNX` is True and an ONNX file is present.
    """
    from src.chatterbox.tts import ChatterboxTTS
    from modules.real_tts_optimizer import optimize_chatterbox_model
    from config.config import CHATTERBOX_CKPT_DIR
    # Apply precision/runtime knobs early
    try:
        from config.config import ENABLE_TF32  # bool
    except Exception:
        ENABLE_TF32 = True
    try:
        if device == 'cuda' and torch.cuda.is_available():
            # Respect TF32 toggle
            torch.backends.cuda.matmul.allow_tf32 = bool(ENABLE_TF32)
            torch.backends.cudnn.allow_tf32 = bool(ENABLE_TF32)
            # Prefer high-precision matmul policy for speed on Ada
            torch.set_float32_matmul_precision('high' if ENABLE_TF32 else 'medium')
    except Exception:
        pass

    logging.info("🚀 Loading ChatterboxTTS with REAL performance optimizations...")



    # Global cache: reuse existing model if same device
    global _GLOBAL_TTS_MODEL, _GLOBAL_TTS_MODEL_DEVICE
    # If a prior Save requested a hard reload, honor it once
    global _FORCE_MODEL_RELOAD
    if _FORCE_MODEL_RELOAD:
        force_reload = True
        _FORCE_MODEL_RELOAD = False

    if not force_reload and _GLOBAL_TTS_MODEL is not None:
        if _GLOBAL_TTS_MODEL_DEVICE == device:
            logging.info("✅ Reusing cached TTS model (no re-load)")
            model = _GLOBAL_TTS_MODEL
            # Ensure eval and return
            try:
                model.eval()
            except Exception:
                pass
            return model

    # Load base model: prefer local if configured
    try:
        ckpt_dir = (CHATTERBOX_CKPT_DIR or "").strip()
        if ckpt_dir:
            ckpt_path = Path(ckpt_dir)
            if ckpt_path.exists():
                logging.info(f"📦 Loading local checkpoints from: {ckpt_path}")
                model = ChatterboxTTS.from_local(ckpt_path, device)
            else:
                logging.warning(f"⚠️ CHATTERBOX_CKPT_DIR set but not found: {ckpt_path}. Falling back to from_pretrained().")
                model = ChatterboxTTS.from_pretrained(device=device)
        else:
            model = ChatterboxTTS.from_pretrained(device=device)
        logging.info("✅ Base ChatterboxTTS model loaded")

    except Exception as e:
        logging.error(f"❌ Failed to load ChatterboxTTS model: {e}")
        raise

    # Apply REAL optimizations that target actual inference bottlenecks
    try:
        logging.info("⚡ Applying REAL TTS optimizations...")
        optimization_count = optimize_chatterbox_model(model)

        if optimization_count > 0:
            logging.info(f"🎯 REAL optimizations applied: {optimization_count}")
            logging.info("🚀 Model ready for HIGH-PERFORMANCE inference")
        else:
            logging.warning("⚠️ No real optimizations could be applied")

    except Exception as e:
        logging.error(f"❌ Real optimization failed: {e}")
        logging.info("📝 Using model without optimizations...")

    _GLOBAL_TTS_MODEL = model
    _GLOBAL_TTS_MODEL_DEVICE = device
    # Warm up cuBLAS handle early to avoid failing later under fragmentation
    try:
        if device == 'cuda' and torch.cuda.is_available():
            a = torch.randn(1, 32, device='cuda', dtype=torch.float32)
            b = torch.randn(32, 1, device='cuda', dtype=torch.float32)
            _ = a @ b  # triggers cublasCreate if not already created
            del a, b, _
    except Exception as e:
        logging.warning(f"cuBLAS warm-up skipped: {e}")

    # Basic model setup
    if hasattr(model, 'eval'):
        model.eval()

    if torch.backends.cudnn.is_available():
        torch.backends.cudnn.benchmark = True
        logging.info("✅ Basic CUDNN optimization enabled")

    return model

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

def process_batch(
    batch, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks,
    punc_norm, basename, log_run_func, log_path, device,
    model, asr_model, seed=0,
    enable_asr=None
):
    if seed != 0:
        set_seed(seed)
    """
    Process a batch of chunks using the batch-enabled TTS model.
    """
    from pydub import AudioSegment
    import io
    import soundfile as sf

    # 1. Prepare batch for TTS
    texts = [chunk_data['text'] for chunk_data in batch]

    # All params are the same, so we take them from the first chunk
    shared_tts_params = batch[0].get("tts_params", tts_params)
    supported_params = {"exaggeration", "cfg_weight", "temperature", "min_p", "top_p", "repetition_penalty"}
    tts_args = {k: v for k, v in shared_tts_params.items() if k in supported_params}

    # 2. Generate audio in a batch (heuristic: only if lengths are similar and group size >1)
    try_batch = True
    # Determine once per run whether the model supports a batch API
    global _BATCH_API_SUPPORTED
    if _BATCH_API_SUPPORTED is None:
        _BATCH_API_SUPPORTED = hasattr(model, 'generate_batch')
    if not _BATCH_API_SUPPORTED:
        try_batch = False
    # Honor config flag to disable micro-batching completely
    try:
        from config import config as _cfg
        if hasattr(_cfg, 'ENABLE_MICRO_BATCHING') and not _cfg.ENABLE_MICRO_BATCHING:
            try_batch = False
    except Exception:
        pass
    try:
        # Heuristic using character lengths as a proxy for token length
        lens = [len(t) for t in texts]
        if len(lens) < 2:
            try_batch = False
        else:
            min_l, max_l = min(lens), max(lens)
            ratio = (max_l / max(1, min_l)) if min_l > 0 else 999.0
            # Threshold can be tuned; start conservative
            threshold = float(os.environ.get('GENTTS_MICROBATCH_LEN_RATIO', '1.8'))
            if ratio > threshold:
                try_batch = False
    except Exception:
        try_batch = True

    if try_batch:
        try:
            with torch.no_grad():
                # Try full batch with OOM backoff
                import gc as _gc
                def gen_with_backoff(text_list):
                    size = len(text_list)
                    bs = size
                    results = []
                    while bs >= 1:
                        try:
                            if bs == size:
                                return model.generate_batch(text_list, **tts_args)
                            else:
                                results.clear()
                                for j in range(0, size, bs):
                                    subtexts = text_list[j:j+bs]
                                    subwavs = model.generate_batch(subtexts, **tts_args)
                                    results.extend(subwavs)
                                return results
                        except RuntimeError as _e:
                            msg = str(_e).lower()
                            if 'out of memory' in msg or 'cuda oom' in msg:
                                try:
                                    if torch.cuda.is_available():
                                        torch.cuda.empty_cache()
                                except Exception:
                                    pass
                                _gc.collect()
                                new_bs = max(1, bs // 2)
                                logging.warning(f"⚠️ CUDA OOM at microbatch={bs}. Retrying with {new_bs}.")
                                if new_bs == bs:
                                    # Cannot reduce further
                                    raise
                                bs = new_bs
                                continue
                            else:
                                raise
                wavs = gen_with_backoff(texts)
        except AttributeError as e:
            # Model has no batch API; disable for this run and fall back
            _BATCH_API_SUPPORTED = False
            try_batch = False
            logging.warning(f"Batch API unavailable on model; falling back to per‑chunk. Reason: {e}")
        except Exception as e:
            # Other failures: fall back this time but keep batch enabled for future groups
            try_batch = False
            logging.warning(f"Batch generation failed; using per‑chunk for this group. Reason: {e}")

    if not try_batch:
        # Fallback to individual processing for this batch
        results = []
        for chunk_data in batch:
            i = chunk_data['index']
            chunk = chunk_data['text']
            boundary_type = chunk_data.get("boundary_type", "none")
            chunk_tts_params = chunk_data.get("tts_params", tts_params)
            result = process_one_chunk(i, chunk, text_chunks_dir, audio_chunks_dir, voice_path, chunk_tts_params, start_time, total_chunks, punc_norm, basename, log_run_func, log_path, device, model, asr_model, boundary_type=boundary_type, enable_asr=enable_asr)
            results.append(result)
        return results


    # 3. Process and save each audio file from the batch
    batch_results = []
    for i, wav_tensor in enumerate(wavs):
        chunk_data = batch[i]
        chunk_index = chunk_data['index']
        boundary_type = chunk_data.get("boundary_type", "none")
        chunk_id_str = f"{chunk_index+1:05}"

        if wav_tensor.dim() == 1:
            wav_tensor = wav_tensor.unsqueeze(0)

        wav_np = wav_tensor.squeeze().cpu().numpy()
        with io.BytesIO() as wav_buffer:
            sf.write(wav_buffer, wav_np, model.sr, format='wav')
            wav_buffer.seek(0)
            audio_segment = AudioSegment.from_wav(wav_buffer)

        # Apply trimming and contextual silence
        from modules.audio_processor import process_audio_with_trimming_and_silence, trim_audio_endpoint
        if boundary_type and boundary_type != "none":
            final_audio = process_audio_with_trimming_and_silence(audio_segment, boundary_type)
        elif ENABLE_AUDIO_TRIMMING:
            final_audio = trim_audio_endpoint(audio_segment)
        else:
            final_audio = audio_segment

        # Final save
        final_path = audio_chunks_dir / f"chunk_{chunk_id_str}.wav"
        final_audio.export(final_path, format="wav")
        logging.info(f"✅ Saved final chunk from batch: {final_path.name}")

        batch_results.append((chunk_index, final_path))

    return batch_results

def process_one_chunk(
    i, chunk, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks,
    punc_norm, basename, log_run_func, log_path, device,
    model, asr_model, seed=0, boundary_type="none",
    enable_asr=None
):
    if seed != 0:
        set_seed(seed)
    """Enhanced chunk processing with quality control, contextual silence, and deep cleanup"""
    import difflib
    from pydub import AudioSegment

    chunk_id_str = f"{i+1:05}"
    chunk_path = text_chunks_dir / f"chunk_{chunk_id_str}.txt"
    with open(chunk_path, 'w', encoding='utf-8') as cf:
        cf.write(chunk)

    chunk_audio_path = audio_chunks_dir / f"chunk_{chunk_id_str}.wav"

    # Spider dry-run: generate a short silent chunk and return quickly to map code paths
    try:
        import os as _os
        if _os.getenv('SPIDER_DRY_RUN', '0') == '1':
            silent = AudioSegment.silent(duration=500)  # 0.5s
            silent.export(chunk_audio_path, format='wav')
            return i, chunk_audio_path
    except Exception:
        pass

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
        
        wav = None
        audio_segment = None
        try:
            # Filter to only supported ChatterboxTTS parameters
            supported_params = {"exaggeration", "cfg_weight", "temperature", "min_p", "top_p", "repetition_penalty"}
            tts_args = {k: v for k, v in current_tts_params.items() if k in supported_params}

            chunk_start_time = time.time()
            try:
                with torch.no_grad():
                    # Serialize GPU inference to prevent CUDA allocator internal asserts under multithreading
                    with _GPU_INFER_LOCK:
                        wav = model.generate(chunk, **tts_args, disable_watermark=True).detach().cpu()
            except RuntimeError as e:
                if "probability tensor contains either" in str(e):
                    logging.warning(f"⚠️ Chunk {chunk_id_str} failed in mixed precision. Retrying in FP32...")
                    from modules.real_tts_optimizer import get_tts_optimizer
                    optimizer = get_tts_optimizer()
                    with optimizer.fp32_fallback_mode():
                        with torch.no_grad():
                            with _GPU_INFER_LOCK:
                                wav = model.generate(chunk, **tts_args, disable_watermark=True).detach().cpu()
                    logging.info(f"✅ Chunk {chunk_id_str} successfully generated in FP32 fallback mode.")
                else:
                    raise # Re-raise other runtime errors
            
            chunk_processing_time = time.time() - chunk_start_time
            with open("performance.log", "a") as perf_log:
                perf_log.write(f"{i},{len(chunk)},{chunk_processing_time:.4f}\n")

            if wav is None:
                raise RuntimeError("Waveform is None after generation attempt.")

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
        # Log silence addition to file only to avoid console noise
        try:
            from modules.terminal_logger import log_only
            log_only(f"🔇 Added {boundary_type} silence to chunk {i+1:05}")
        except Exception:
            pass
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

    # Emit one per-chunk sampling summary to console
    try:
        from modules.terminal_logger import emit_chunk_summary
        emit_chunk_summary()
    except Exception:
        pass

    # Progress updates with accurate realtime are handled by batch/micro-batch code
    # which passes measured total_audio_duration. Avoid printing extra partial lines here.

    # No intermediate file cleanup needed - all processing done in memory

    # Avoid duplicate progress updates here as well.

    # Log details - only log ASR failures
    if asr_enabled and best_sim < 0.8:
        log_run_func(f"ASR VALIDATION FAILED - Chunk {chunk_id_str}:\nExpected:\n{chunk}\nActual:\n{best_asr_text}\nSimilarity: {best_sim:.3f}\n" + "="*50, log_path)
    elif not asr_enabled:
        log_run_func(f"Chunk {chunk_id_str}: Original text: {chunk}", log_path)

    # Silence already added in memory above - no disk processing needed

    # Enhanced regular cleanup (every chunk)
    del wav
    optimize_memory_usage()

    # Additional per-chunk cleanup for long runs
    if (i + 1) % 50 == 0:
        torch.cuda.empty_cache()
        gc.collect()

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
    # Allow GUI/runtime overrides for chunk sizing via config_params
    try:
        max_words_override = None
        min_words_override = None
        if config_params:
            max_words_override = int(config_params.get('max_chunk_words', MAX_CHUNK_WORDS))
            min_words_override = int(config_params.get('min_chunk_words', MIN_CHUNK_WORDS))
        chunks = sentence_chunk_text(
            cleaned,
            max_words=max_words_override if max_words_override is not None else MAX_CHUNK_WORDS,
            min_words=min_words_override if min_words_override is not None else MIN_CHUNK_WORDS,
        )
    except Exception:
        # Fallback to config defaults if overrides invalid
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

def create_parameter_microbatches(chunks):
    """Group chunks by their rounded TTS parameters for micro-batching efficiency."""
    from collections import defaultdict

    # Group chunks by their TTS parameter combination
    parameter_groups = defaultdict(list)

    for chunk in chunks:
        if isinstance(chunk, dict) and 'tts_params' in chunk:
            tts_params = chunk['tts_params']

            # Create parameter key from rounded values
            param_key = (
                tts_params.get('exaggeration', 0.5),
                tts_params.get('cfg_weight', 0.5),
                tts_params.get('temperature', 0.85)
            )
        else:
            # Default parameters for chunks without specific TTS params
            param_key = (0.5, 0.5, 0.85)

        parameter_groups[param_key].append(chunk)

    # Convert groups to list of batches
    chunk_batches = []
    for param_key, chunks_in_group in parameter_groups.items():
        exag, cfg, temp = param_key
        print(f"  📦 Micro-batch: {len(chunks_in_group)} chunks with params (exag={exag}, cfg={cfg}, temp={temp})")

        # SORT BY LENGTH - THE MISSING PIECE
        chunks_in_group.sort(key=lambda c: len(c.get('text', '')))

        # Split large groups into smaller batches to avoid memory issues
        # Use smaller microbatch when CFG is enabled (effective 2×B)
        max_microbatch_size = 4 if (float(cfg) > 0.0) else 8
        for i in range(0, len(chunks_in_group), max_microbatch_size):
            batch = chunks_in_group[i:i + max_microbatch_size]
            chunk_batches.append(batch)

    return chunk_batches

def process_book_folder(book_dir, voice_path, tts_params, device, skip_cleanup=False, enable_asr=None, quality_params=None, config_params=None, specific_text_file=None):
    """Enhanced book processing with batch processing to prevent hangs"""

    # Hard reset barrier at conversion start: behave like a fresh launch
    # 1) Release any cached model and voice conditionals
    try:
        clear_voice_cache()
        _release_global_tts_model()
    except Exception:
        pass

    # 2) Aggressive CUDA + host cleanup (no extra console noise)
    try:
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            if hasattr(torch.cuda, 'reset_peak_memory_stats'):
                torch.cuda.reset_peak_memory_stats()
            if hasattr(torch._C, '_cuda_clearCublasWorkspaces'):
                torch._C._cuda_clearCublasWorkspaces()
    except Exception:
        pass
    try:
        import gc
        gc.collect(); gc.collect()
    except Exception:
        pass

    # Start terminal logging to capture all output
    start_terminal_logging("term.log")

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

    # Apply GUI config parameters that impact runtime without editing file
    if config_params:
        try:
            # Global worker and batching overrides
            global MAX_WORKERS, BATCH_SIZE, ENABLE_MID_DROP_CHECK, ENABLE_HUM_DETECTION
            if 'max_workers' in config_params:
                MAX_WORKERS = int(config_params['max_workers'])
            if 'batch_size' in config_params:
                BATCH_SIZE = int(config_params['batch_size'])
            if 'enable_mid_drop_check' in config_params:
                ENABLE_MID_DROP_CHECK = bool(config_params['enable_mid_drop_check'])
            if 'enable_hum_detection' in config_params:
                ENABLE_HUM_DETECTION = bool(config_params['enable_hum_detection'])

            # Apply overrides to dependent modules
            try:
                from modules import file_manager as fm
                if 'enable_normalization' in config_params:
                    fm.ENABLE_NORMALIZATION = bool(config_params['enable_normalization'])
                if 'normalization_type' in config_params:
                    fm.NORMALIZATION_TYPE = str(config_params['normalization_type'])
                if 'target_lufs' in config_params:
                    fm.TARGET_LUFS = float(config_params['target_lufs'])
                if 'target_peak_db' in config_params:
                    fm.TARGET_PEAK_DB = float(config_params['target_peak_db'])
                if 'm4b_sample_rate' in config_params:
                    fm.M4B_SAMPLE_RATE = int(config_params['m4b_sample_rate'])
                if 'playback_speed' in config_params:
                    fm.ATEMPO_SPEED = float(config_params['playback_speed'])
            except Exception as _e:
                print(f"⚠️ Failed to apply file_manager overrides: {_e}")

            try:
                from modules import audio_processor as ap
                if 'enable_audio_trimming' in config_params:
                    ap.ENABLE_AUDIO_TRIMMING = bool(config_params['enable_audio_trimming'])
                if 'speech_threshold' in config_params:
                    ap.SPEECH_ENDPOINT_THRESHOLD = float(config_params['speech_threshold'])
                if 'trimming_buffer' in config_params:
                    ap.TRIMMING_BUFFER_MS = int(config_params['trimming_buffer'])
                if 'silence_chapter_start' in config_params:
                    ap.SILENCE_CHAPTER_START = int(config_params['silence_chapter_start'])
                if 'silence_chapter_end' in config_params:
                    ap.SILENCE_CHAPTER_END = int(config_params['silence_chapter_end'])
                if 'silence_section' in config_params:
                    ap.SILENCE_SECTION_BREAK = int(config_params['silence_section'])
                if 'silence_paragraph' in config_params:
                    ap.SILENCE_PARAGRAPH_END = int(config_params['silence_paragraph'])
                if 'silence_comma' in config_params:
                    ap.SILENCE_COMMA = int(config_params['silence_comma'])
                if 'silence_period' in config_params:
                    ap.SILENCE_PERIOD = int(config_params['silence_period'])
                if 'silence_question' in config_params:
                    ap.SILENCE_QUESTION_MARK = int(config_params['silence_question'])
                if 'silence_exclamation' in config_params:
                    ap.SILENCE_EXCLAMATION = int(config_params['silence_exclamation'])
                if 'enable_chunk_silence' in config_params:
                    ap.ENABLE_CHUNK_END_SILENCE = bool(config_params['enable_chunk_silence'])
                if 'chunk_silence_duration' in config_params:
                    ap.CHUNK_END_SILENCE_MS = int(config_params['chunk_silence_duration'])
            except Exception as _e:
                print(f"⚠️ Failed to apply audio_processor overrides: {_e}")

            # Blunt micro-batching switch (propagate to config module for consistency)
            if 'enable_micro_batching' in config_params:
                emb = bool(config_params['enable_micro_batching'])
                from config import config as _cfg
                _cfg.ENABLE_MICRO_BATCHING = emb
                _cfg.ENABLE_VADER_MICRO_BATCHING = emb
                print(f"🧩 Micro-batching globally {'ENABLED' if emb else 'DISABLED'} via GUI")
        except Exception as _e:
            print(f"⚠️ Failed to apply GUI runtime overrides: {_e}")

    from src.chatterbox.tts import punc_norm
    print(f"🔍 DEBUG: Successfully imported punc_norm")

    # Setup directories
    print(f"🔍 DEBUG: Calling setup_book_directories...")
    output_root, tts_dir, text_chunks_dir, audio_chunks_dir = setup_book_directories(book_dir)
    print(f"🔍 DEBUG: Directory setup complete")

    # ============================================================================
    # CLEAN PROCESSING - REAL OPTIMIZATIONS ONLY
    # ============================================================================
    print("🚀 Using optimized TTS model with REAL performance improvements")

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

    print(f"🎯 Processing {len(all_chunks)} chunks with REAL optimized inference")

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

    # Process isolation pipeline has been removed; proceed with standard processing.

    # Standard batch processing (fallback or when isolation disabled)
    print(f"📊 Processing {total_chunks} chunks with intelligent reload decisions")

    # Reset smart reload manager for new session
    if ENABLE_SMART_RELOAD:
        reset_reload_manager()
        print(f"🧠 Smart reload manager initialized")

    all_results = []

    # Detect changes that require model reload using EFFECTIVE values (runtime overrides first)
    try:
        from config import config as _cfg
        eff_workers = int((config_params or {}).get('max_workers', getattr(_cfg, 'MAX_WORKERS', 0)))
        eff_batch = int((config_params or {}).get('batch_size', getattr(_cfg, 'BATCH_SIZE', 0)))
        eff_tts_batch = int((config_params or {}).get('tts_batch_size', getattr(_cfg, 'TTS_BATCH_SIZE', 16)))
        eff_micro = bool((config_params or {}).get('enable_micro_batching', getattr(_cfg, 'ENABLE_MICRO_BATCHING', True)))
        run_sig = (device, eff_workers, eff_batch, eff_tts_batch, eff_micro)
    except Exception:
        run_sig = (device, 0, 0, 0, True)

    global _LAST_RUN_SIGNATURE
    if _LAST_RUN_SIGNATURE is not None and run_sig != _LAST_RUN_SIGNATURE:
        print("🧹 Config change detected. Releasing cached model.")
        _release_global_tts_model()
    _LAST_RUN_SIGNATURE = run_sig

    # Prepare voice sample compatibility once; reload model per-batch below
    compatible_voice = ensure_voice_sample_compatibility(voice_path, output_dir=tts_dir)

    for batch_start in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_chunks)
        batch_chunks = all_chunks[batch_start:batch_end]

        # Smart reload decision logic
        if ENABLE_SMART_RELOAD and batch_start > 0:
            remaining_chunks = total_chunks - batch_start
            reload_decision = should_reload_model(remaining_chunks)

            if reload_decision['should_reload']:
                print(f"\n🧠 Smart reload triggered: {reload_decision['reason']}")
                print(f"   📊 Performance degradation: {reload_decision['degradation_pct']:.1f}%")
                print(f"   💰 Economics: {reload_decision['economics']['roi']:.1f}x ROI")
                record_model_reload(batch_start)
            else:
                print(f"\n🧠 Smart reload analysis: {reload_decision['reason']}")

        print(f"\n🔄 Processing batch: chunks {batch_start+1}-{batch_end}")
        # Inform logger about current batch size for per-chunk summaries
        try:
            from modules.terminal_logger import set_batch_size
            set_batch_size(len(batch_chunks))
        except Exception:
            pass

        # Optional light cleanup between batches without destroying caches (disabled by default)
        if batch_start > 0 and os.environ.get("GENTTS_LIGHT_BATCH_CLEANUP", "0") == "1":
            print(f"🧹 Light cleanup before batch {batch_start+1}-{batch_end}")
            try:
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                gc.collect()
            except Exception:
                pass

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

        # Reload TTS model at the top of each batch (honor BATCH_SIZE semantics)
        model = load_optimized_model(device, force_reload=True)
        # Pre-warm model for selected voice
        model = prewarm_model_with_voice(model, compatible_voice, tts_params)

        futures = []
        batch_results = []

        # Dynamic worker allocation
        optimal_workers = get_optimal_workers()
        print(f"🔧 Using {optimal_workers} workers for batch {batch_start+1}-{batch_end}")

        use_vader = tts_params.get('use_vader', True)

        # ============================================================================
        # CLEAN PROCESSING WITH REAL OPTIMIZATIONS
        # ============================================================================
        batch_start_time = time.time()
        print(f"🚀 Processing with REAL TTS optimizations (mixed precision, torch.compile)")

        # MEASURE BATCH-BINNING EFFECTIVENESS
        from config.config import ENABLE_BATCH_BINNING
        if ENABLE_BATCH_BINNING:
            print("📊 PERFORMANCE MEASUREMENT: Batch-binning enabled - measuring actual speed impact")

        batch_timing_start = time.time()

        if not use_vader:
            # --- BATCH MODE ---
            print(f"🚀 VADER disabled. Running in high-performance batch mode.")

            # Check if batch-binning is enabled for micro-batching by parameters
            from config.config import ENABLE_BATCH_BINNING
            if ENABLE_BATCH_BINNING:
                try:
                    from modules.terminal_logger import log_only
                    log_only("🔗 BATCH-BINNING: Grouping chunks by rounded TTS parameters for micro-batching")
                except Exception:
                    pass
                chunk_batches = create_parameter_microbatches(batch_chunks)
                try:
                    from modules.terminal_logger import log_only
                    log_only(f"📊 Processing {len(batch_chunks)} chunks in {len(chunk_batches)} parameter-grouped micro-batches")
                except Exception:
                    pass
            else:
                # Standard fixed-size batching
                tts_batch_size = config_params.get('tts_batch_size', 16)
                chunk_batches = [batch_chunks[i:i + tts_batch_size] for i in range(0, len(batch_chunks), tts_batch_size)]
                print(f"📊 Processing {len(batch_chunks)} chunks in {len(chunk_batches)} fixed batches of size {tts_batch_size}")

            with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
                for batch in chunk_batches:
                    if shutdown_requested:
                        break
                    futures.append(executor.submit(
                        process_batch,
                        batch, text_chunks_dir, audio_chunks_dir,
                        voice_path, tts_params, start_time, total_chunks,
                        punc_norm, book_dir.name, log_run, log_path, device,
                        model, asr_model, 0, asr_enabled
                    ))

                # Wait for batches to complete
                for fut in as_completed(futures):
                    try:
                        # process_batch returns a list of (idx, wav_path) tuples
                        results_list = fut.result()
                        for idx, wav_path in results_list:
                            if wav_path and wav_path.exists():
                                chunk_duration = get_chunk_audio_duration(wav_path)
                                total_audio_duration += chunk_duration
                                batch_results.append((idx, wav_path))
                        # Throttle ETA printing to avoid console spam; status layer still receives updates
                        if len(batch_results) == 1 or (len(batch_results) % 5) == 0 or len(batch_results) == len(batch_chunks):
                            log_chunk_progress(batch_start + len(batch_results) - 1, total_chunks, start_time, total_audio_duration)
                    except Exception as e:
                        logging.error(f"Future failed in batch: {e}")

            # Calculate performance with DETAILED debugging
            batch_end_time = time.time()
            total_batch_time = batch_end_time - batch_start_time
            actual_processing_time = batch_end_time - batch_timing_start

            print(f"🔍 PERFORMANCE CALCULATION DEBUG:")
            print(f"   Batch start time: {batch_start_time}")
            print(f"   Batch end time: {batch_end_time}")
            print(f"   Total batch time: {total_batch_time:.2f} seconds")
            print(f"   Actual processing time: {actual_processing_time:.2f} seconds")
            print(f"   Chunks processed: {len(batch_chunks)}")
            print(f"   Batch range: {batch_start+1}-{batch_end}")

            # BATCH-BINNING PERFORMANCE MEASUREMENT
            from config.config import ENABLE_BATCH_BINNING
            if ENABLE_BATCH_BINNING:
                chunks_per_sec = len(batch_chunks) / actual_processing_time if actual_processing_time > 0 else 0
                print(f"📊 BATCH-BINNING PERFORMANCE: {chunks_per_sec:.2f} chunks/sec with parameter rounding")

            if total_batch_time > 0:
                its_performance = len(batch_chunks) / total_batch_time
                print(f"📊 CALCULATED PERFORMANCE: {its_performance:.2f} it/s")
                print(f"   Formula: {len(batch_chunks)} chunks ÷ {total_batch_time:.2f} seconds = {its_performance:.2f} it/s")
            else:
                print("⚠️ Zero or negative processing time detected")

        else:
            # --- VADER-ENABLED MODE ---
            from config.config import ENABLE_VADER_MICRO_BATCHING
            if ENABLE_VADER_MICRO_BATCHING:
                try:
                    from modules.terminal_logger import log_only
                    log_only("🎨 VADER enabled. Running in nuanced mode with micro-batching.")
                except Exception:
                    pass
            else:
                try:
                    from modules.terminal_logger import log_only
                    log_only("🎨 VADER enabled. Micro-batching disabled by config; processing per-chunk.")
                except Exception:
                    pass

            # Apply parameter rounding for micro-batching
            rounded_chunks = []
            for chunk_data in batch_chunks:
                if isinstance(chunk_data, dict):
                    rounded_chunk = chunk_data.copy()
                    if 'tts_params' in rounded_chunk and rounded_chunk['tts_params']:
                        tts_params_copy = rounded_chunk['tts_params'].copy()
                        # Round VADER-influenced parameters to enable groupings
                        for param in ['exaggeration', 'cfg_weight', 'temperature']:
                            if param in tts_params_copy:
                                original_value = tts_params_copy[param]
                                steps = round(original_value / BATCH_BIN_PRECISION)
                                binned_value = steps * BATCH_BIN_PRECISION
                                tts_params_copy[param] = round(binned_value, 3)
                        rounded_chunk['tts_params'] = tts_params_copy
                    rounded_chunks.append(rounded_chunk)
                else:
                    rounded_chunks.append(chunk_data)

            # Create micro-batches by parameter groupings, or force per-chunk
            if ENABLE_VADER_MICRO_BATCHING:
                micro_batches = create_parameter_microbatches(rounded_chunks)
                try:
                    from modules.terminal_logger import log_only
                    log_only(f"🔗 VADER MICRO-BATCHING: Created {len(micro_batches)} micro-batches from {len(rounded_chunks)} chunks")
                except Exception:
                    pass
            else:
                micro_batches = [[ch] for ch in rounded_chunks]

            with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
                for microbatch_idx, microbatch in enumerate(micro_batches):
                    if ENABLE_VADER_MICRO_BATCHING:
                        try:
                            from modules.terminal_logger import log_only
                            log_only(f"🎯 Processing micro-batch {microbatch_idx+1}/{len(micro_batches)} ({len(microbatch)} chunks)")
                        except Exception:
                            pass

                    # Process all chunks in this micro-batch
                    microbatch_futures = []
                    for i, chunk_data in enumerate(microbatch):
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
                            # Use the chunk's original index from JSON instead of calculated position
                            global_chunk_index = chunk_data.get("index", batch_start + sum(len(mb) for mb in micro_batches[:microbatch_idx]) + i)
                        else:
                            # Handle old tuple format (text, is_para_end) - convert to boundary_type
                            chunk = chunk_data[0] if len(chunk_data) > 0 else str(chunk_data)
                            # Convert old is_paragraph_end to boundary_type
                            is_old_para_end = chunk_data[1] if len(chunk_data) > 1 else False
                            boundary_type = "paragraph_end" if is_old_para_end else "none"
                            chunk_tts_params = tts_params # Fallback for old format
                            # Fallback calculation for old tuple format
                            global_chunk_index = batch_start + sum(len(mb) for mb in micro_batches[:microbatch_idx]) + i

                        microbatch_futures.append(executor.submit(
                            process_one_chunk,
                            global_chunk_index, chunk, text_chunks_dir, audio_chunks_dir,
                            voice_path, chunk_tts_params, start_time, total_chunks,
                            punc_norm, book_dir.name, log_run, log_path, device,
                            model, asr_model, boundary_type=boundary_type,
                            enable_asr=asr_enabled
                        ))

                    # Wait for micro-batch to complete
                    try:
                        from modules.terminal_logger import log_only
                        log_only(f"🔄 Waiting for micro-batch {microbatch_idx+1} to complete...")
                    except Exception:
                        pass
                    completed_count = 0

                    for fut in as_completed(microbatch_futures):
                        try:
                            idx, wav_path = fut.result()
                            if wav_path and wav_path.exists():
                                # Measure actual audio duration for this chunk
                                chunk_duration = get_chunk_audio_duration(wav_path)
                                total_audio_duration += chunk_duration
                                batch_results.append((idx, wav_path))

                                # Track chunk performance for smart reload
                                if ENABLE_SMART_RELOAD:
                                    chunk_idx = batch_start + sum(len(mb) for mb in micro_batches[:microbatch_idx]) + completed_count
                                    elapsed_time = time.time() - start_time
                                    processing_time_per_chunk = elapsed_time / chunk_idx if chunk_idx > 0 else 1.0
                                    estimated_tokens = estimate_tokens_in_text(chunk.get('text', ''))
                                    track_chunk_performance(chunk_idx, processing_time_per_chunk, estimated_tokens)

                                # Update progress on every completed chunk; terminal logger throttles display
                                completed_count += 1
                                log_chunk_progress(
                                    batch_start
                                    + sum(len(mb) for mb in micro_batches[:microbatch_idx])
                                    + completed_count - 1,
                                    total_chunks,
                                    start_time,
                                    total_audio_duration,
                                )

                        except Exception as e:
                            logging.error(f"Future failed in micro-batch: {e}")

                    futures.extend(microbatch_futures)

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

def process_single_batch(
    batch_chunks, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks,
    basename, log_path, device, enable_asr, seed=0,
    asr_config=None
):
    """
    Loads models and processes a single batch of chunks.
    Designed to be called from a separate worker process.
    """
    import torch
    import gc
    from pathlib import Path
    from src.chatterbox.tts import punc_norm
    from modules.file_manager import ensure_voice_sample_compatibility
    from modules.asr_manager import load_asr_model_adaptive, cleanup_asr_model

    # A simple logger function to satisfy the dependency of process_one_chunk (fallback)
    def log_run(message, path):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    # Prepare voice
    compatible_voice = ensure_voice_sample_compatibility(voice_path)

    # Load models
    model = load_optimized_model(device, force_reload=True)
    model = prewarm_model_with_voice(model, compatible_voice, tts_params)
    
    asr_model = None
    if enable_asr:
        asr_model, _ = load_asr_model_adaptive(asr_config or {})

    # Get the punc_norm function - assuming 'en'
    punc_normalizer = punc_norm('en')

    # Call the existing process_batch function
    results = process_batch(
        batch=batch_chunks,
        text_chunks_dir=Path(text_chunks_dir),
        audio_chunks_dir=Path(audio_chunks_dir),
        voice_path=Path(voice_path),
        tts_params=tts_params,
        start_time=start_time,
        total_chunks=total_chunks,
        punc_norm=punc_normalizer,
        basename=basename,
        log_run_func=log_run,
        log_path=Path(log_path),
        device=device,
        model=model,
        asr_model=asr_model,
        seed=seed,
        enable_asr=enable_asr
    )

    # Cleanup
    del model
    if asr_model:
        cleanup_asr_model(asr_model)
    
    torch.cuda.empty_cache()
    gc.collect()
    
    print(f"✅ Worker process finished batch. Results: {len(results)} chunks processed.")
    
    return results
