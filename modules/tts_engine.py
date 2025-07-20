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
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import torchaudio as ta

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

def load_optimized_model(device):
    """Load TTS model with memory optimizations"""
    from chatterbox.tts import ChatterboxTTS

    try:
        # Try to load with FP16 if supported
        model = ChatterboxTTS.from_pretrained(device=device, torch_dtype=torch.float16)
        logging.info("✅ Loaded model in FP16 mode (halved VRAM usage)")
    except:
        # Fallback to default loading
        model = ChatterboxTTS.from_pretrained(device=device)
        logging.info("⚠️ Using FP32 mode (FP16 not supported)")

    # Only apply eval() and benchmark if the model has these attributes
    if hasattr(model, 'eval'):
        model.eval()

    # Set CUDNN benchmark for performance (if available)
    if torch.backends.cudnn.is_available():
        torch.backends.cudnn.benchmark = True

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

def process_one_chunk(
    i, chunk, text_chunks_dir, audio_chunks_dir,
    voice_path, tts_params, start_time, total_chunks,
    punc_norm, basename, log_run_func, log_path, device,
    model, asr_model, all_chunks, boundary_type="none"
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

    for attempt_num in range(1, 3):
        logging.info(f"🔁 Starting TTS for chunk {chunk_id_str}, attempt {attempt_num}")
        try:
            tts_args = {k: v for k, v in tts_params.items() if k != "max_workers"}

            # monitor_gpu_activity(f"Before TTS chunk_{chunk_id_str}")  # Disabled for speed
            with torch.no_grad():
                wav = model.generate(chunk, **tts_args).detach().cpu()
            # monitor_gpu_activity(f"After TTS chunk_{chunk_id_str}")  # Disabled for speed

            if wav.dim() == 1:
                wav = wav.unsqueeze(0)

            # Retry if mid-energy drop is enabled and detected (check in memory)
            if ENABLE_MID_DROP_CHECK and has_mid_energy_drop(wav, model.sr):
                mid_drop_retries += 1
                if mid_drop_retries >= max_mid_drop_retries:
                    logging.info(f"⚠️ Mid-drop retry limit reached for {chunk_id_str}. Accepting audio.")
                else:
                    logging.info(f"⚠️ Mid-chunk noise detected in {chunk_id_str}. Retrying...")
                    continue

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
            
            # Smart fade removed - replaced by precise audio trimming
            # Audio health validation disabled for speed
            
            # Note: Audio trimming will handle end-of-speech cleanup more precisely

            # ASR validation (memory-based processing)
            if ENABLE_ASR and asr_model is not None:
                from modules.audio_processor import asr_f1_score
                import io
                import soundfile as sf
                # monitor_gpu_activity(f"Before ASR chunk_{chunk_id_str}")  # Disabled for speed
                try:
                    # Process ASR completely in memory - no disk writes
                    # Convert AudioSegment to numpy array for ASR
                    samples = np.array(audio_segment.get_array_of_samples())
                    if audio_segment.channels == 2:
                        samples = samples.reshape((-1, 2)).mean(axis=1)
                    
                    # Normalize to float32 for ASR model
                    audio_np = samples.astype(np.float32) / audio_segment.max_possible_amplitude
                    
                    # Use ASR model directly on numpy array (if supported)
                    # Note: This depends on the ASR model's input capabilities
                    result = asr_model.transcribe(audio_np)
                    
                    if not isinstance(result, dict) or "text" not in result:
                        raise ValueError(f"Invalid ASR result type: {type(result)}")

                    asr_text = result.get("text", "").strip()
                    sim_ratio = asr_f1_score(punc_norm(chunk), asr_text)

                except Exception as e:
                    print(f"❌ ASR failed for {chunk_id_str}: {e}")
                    log_run_func(f"ASR VALIDATION FAILED - Chunk {chunk_id_str}:\nExpected:\n{chunk}\nActual:\n<ASR Failure: {e}>\nSimilarity: -1.000\n" + "="*50, log_path)
                    sim_ratio = -1.0
                    continue

                logging.info(f"ASR similarity for chunk {chunk_id_str}: {sim_ratio:.3f}")
                if sim_ratio < 0.7:
                    continue

                # Track best valid match
                best_sim = sim_ratio
                best_asr_text = asr_text
                # monitor_gpu_activity(f"After ASR chunk_{chunk_id_str}")  # Disabled for speed

            # Success - we have processed audio in memory
            final_audio = audio_segment
            break

        except Exception as e:
            import traceback
            logging.error(f"Exception during TTS attempt {attempt_num} for chunk {chunk_id_str}: {e}")
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
    if ENABLE_ASR and best_sim < 0.8:
        log_run_func(f"ASR VALIDATION FAILED - Chunk {chunk_id_str}:\nExpected:\n{chunk}\nActual:\n{best_asr_text}\nSimilarity: {best_sim:.3f}\n" + "="*50, log_path)
    elif not ENABLE_ASR:
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

def generate_enriched_chunks(text_file, output_dir, user_tts_params=None):
    """Reads a text file, performs VADER sentiment analysis, and returns enriched chunks."""
    analyzer = SentimentIntensityAnalyzer()
    
    raw_text = text_file.read_text(encoding='utf-8')
    cleaned = smart_punctuate(raw_text)
    chunks = sentence_chunk_text(cleaned)

    # Use user-provided parameters as base, or fall back to config defaults
    if user_tts_params:
        base_exaggeration = user_tts_params.get('exaggeration', BASE_EXAGGERATION)
        base_cfg_weight = user_tts_params.get('cfg_weight', BASE_CFG_WEIGHT)
        base_temperature = user_tts_params.get('temperature', BASE_TEMPERATURE)
    else:
        base_exaggeration = BASE_EXAGGERATION
        base_cfg_weight = BASE_CFG_WEIGHT
        base_temperature = BASE_TEMPERATURE

    enriched = []
    chunk_texts = [chunk_text for chunk_text, _ in chunks]
    
    for i, (chunk_text, is_para_end) in enumerate(chunks):
        sentiment_scores = analyzer.polarity_scores(chunk_text)
        compound_score = sentiment_scores['compound']

        exaggeration = base_exaggeration + (compound_score * VADER_EXAGGERATION_SENSITIVITY)
        cfg_weight = base_cfg_weight + (compound_score * VADER_CFG_WEIGHT_SENSITIVITY)
        temperature = base_temperature + (compound_score * VADER_TEMPERATURE_SENSITIVITY)

        # Clamp values to defined min/max
        exaggeration = round(max(TTS_PARAM_MIN_EXAGGERATION, min(exaggeration, TTS_PARAM_MAX_EXAGGERATION)), 2)
        cfg_weight = round(max(TTS_PARAM_MIN_CFG_WEIGHT, min(cfg_weight, TTS_PARAM_MAX_CFG_WEIGHT)), 2)
        temperature = round(max(TTS_PARAM_MIN_TEMPERATURE, min(temperature, TTS_PARAM_MAX_TEMPERATURE)), 2)

        boundary_type = detect_content_boundaries(chunk_text, i, chunk_texts, is_para_end)
        
        enriched.append({
            "index": i,
            "text": chunk_text,
            "word_count": len(chunk_text.split()),
            "boundary_type": boundary_type if boundary_type else "none",
            "sentiment_compound": compound_score,
            "tts_params": {
                "exaggeration": exaggeration,
                "cfg_weight": cfg_weight,
                "temperature": temperature
            }
        })

    output_json_path = output_dir / "chunks_info.json"
    save_chunks(output_json_path, enriched)
    return enriched

def process_book_folder(book_dir, voice_path, tts_params, device, skip_cleanup=False):
    """Enhanced book processing with batch processing to prevent hangs"""
    print(f"🔍 DEBUG: Entering process_book_folder with book_dir='{book_dir}', voice_path='{voice_path}'")
    
    from chatterbox.tts import punc_norm
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
    text_files = [book_files['text']] if book_files['text'] else []
    cover_file = book_files['cover']
    nfo_file = book_files['nfo']
    print(f"🔍 DEBUG: Found text files: {text_files}")

    if not text_files:
        logging.info(f"[{book_dir.name}] ERROR: No .txt files found in the book folder.")
        return None, None, []

    setup_logging(output_root)

    # Generate enriched chunks with VADER analysis using user parameters
    all_chunks = generate_enriched_chunks(text_files[0], text_chunks_dir, tts_params)

    # Create run_log_lines
    print(f"🔍 DEBUG: Creating run_log_lines...")
    print(f"🔍 DEBUG: voice_path type: {type(voice_path)}, value: {voice_path}")
    
    # Extract voice name for logging
    voice_name_for_log = voice_path.stem if hasattr(voice_path, 'stem') else Path(voice_path).stem
    
    run_log_lines = [
        f"\n===== Processing: {book_dir.name} =====",
        f"Voice: {voice_name_for_log}",
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Text files processed: {len(text_files)}",
        f"Total chunks generated: {len(all_chunks)}"
    ]

    start_time = time.time()
    total_chunks = len(all_chunks)
    log_path = output_root / "chunk_validation.log"
    total_audio_duration = 0.0

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
        model.prepare_conditionals(compatible_voice)

        # Load ASR model once per batch if needed
        asr_model = None
        if ENABLE_ASR:
            import whisper
            print(f"🎤 Loading Whisper ASR model for batch...")
            asr_model = whisper.load_model("base", device="cuda")

        futures = []
        batch_results = []

        # Dynamic worker allocation
        optimal_workers = get_optimal_workers()
        print(f"🔧 Using {optimal_workers} workers for batch {batch_start+1}-{batch_end}")

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
                    model, asr_model, all_chunk_texts, boundary_type
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

                        # Update progress every 10 chunks within batch
                        completed_count += 1
                        if completed_count % 10 == 0:
                            log_chunk_progress(batch_start + completed_count - 1, total_chunks, start_time, total_audio_duration)

                except Exception as e:
                    logging.error(f"Future failed in batch: {e}")

        # Clean up model after batch
        print(f"🧹 Cleaning up after batch {batch_start+1}-{batch_end}")
        del model
        if asr_model:
            del asr_model
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
