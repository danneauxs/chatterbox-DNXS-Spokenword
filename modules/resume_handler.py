"""
Resume Handler Module
Handles resume functionality for interrupted processing
"""

import torch
import time
import logging
from datetime import timedelta
from pathlib import Path

from config.config import *
from modules.text_processor import smart_punctuate, sentence_chunk_text
from modules.file_manager import (
    setup_book_directories, find_book_files, list_voice_samples,
    ensure_voice_sample_compatibility, get_audio_files_in_directory,
    combine_audio_chunks, convert_to_m4b, add_metadata_to_m4b
)
from modules.audio_processor import get_chunk_audio_duration, pause_for_chunk_review
from modules.progress_tracker import setup_logging, log_chunk_progress, log_run

def analyze_existing_chunks(audio_chunks_dir):
    """Analyze existing chunks to determine resume point"""
    if not audio_chunks_dir.exists():
        return 0, []

    chunk_paths = get_audio_files_in_directory(audio_chunks_dir)

    if not chunk_paths:
        return 0, []

    # Find the highest chunk number
    chunk_numbers = []
    for chunk_path in chunk_paths:
        import re
        match = re.match(r"chunk_(\d+)\.wav", chunk_path.name)
        if match:
            chunk_numbers.append(int(match.group(1)))

    if not chunk_numbers:
        return 0, []

    chunk_numbers.sort()
    last_chunk_number = max(chunk_numbers)

    # Check for gaps in sequence
    missing_chunks = []
    for i in range(1, last_chunk_number + 1):
        if i not in chunk_numbers:
            missing_chunks.append(i)

    print(f"📊 Existing chunks analysis:")
    print(f"   Total chunks found: {GREEN}{len(chunk_numbers)}{RESET}")
    print(f"   Highest chunk number: {GREEN}{last_chunk_number}{RESET}")
    if missing_chunks:
        print(f"   Missing chunks: {YELLOW}{len(missing_chunks)}{RESET}")
        if len(missing_chunks) <= 10:
            print(f"   Missing: {missing_chunks}")
        else:
            print(f"   Missing: {missing_chunks[:10]}... (+{len(missing_chunks)-10} more)")

    return last_chunk_number, missing_chunks

def suggest_resume_point(last_chunk, missing_chunks):
    """Suggest optimal resume point based on existing chunks"""
    if not missing_chunks:
        # No gaps, can resume from next chunk
        return last_chunk + 1

    # If there are missing chunks, suggest resuming from first missing
    first_missing = min(missing_chunks)

    print(f"\n💡 Resume suggestions:")
    print(f"   Resume from chunk {GREEN}{last_chunk + 1}{RESET} (continue from last)")
    print(f"   Resume from chunk {YELLOW}{first_missing}{RESET} (fill gaps first)")

    return first_missing

def validate_resume_point(start_chunk, total_expected_chunks):
    """Validate that resume point makes sense"""
    if start_chunk < 1:
        print(f"{RED}❌ Invalid resume point: {start_chunk}. Must be >= 1{RESET}")
        return False

    if start_chunk > total_expected_chunks:
        print(f"{RED}❌ Resume point {start_chunk} exceeds expected total chunks {total_expected_chunks}{RESET}")
        return False

    return True

def process_book_folder_resume(book_dir, voice_path, tts_params, device, start_chunk=1):
    """Enhanced book processing with resume capability"""
    from modules.tts_engine import process_one_chunk, load_optimized_model, get_optimal_workers
    from src.chatterbox.tts import punc_norm
    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Setup directories
    output_root, tts_dir, text_chunks_dir, audio_chunks_dir = setup_book_directories(book_dir)

    # Find book files
    book_files = find_book_files(book_dir)
    text_file = book_files['text']
    cover_file = book_files['cover']
    nfo_file = book_files['nfo']

    if not text_file:
        logging.info(f"[{book_dir.name}] ERROR: No .txt files found in the book folder.")
        return None, None, []
    
    text_files = [text_file]  # Convert to list for compatibility

    # IMPORTANT: Don't delete existing directories if resuming
    print(f"🔍 DEBUG: start_chunk = {start_chunk}")
    if start_chunk == 1:
        print(f"⚠️ WARNING: start_chunk is 1 - this will clear existing chunks!")
        print(f"📁 About to clear: {audio_chunks_dir}")
        
        # Only clear on fresh start
        import shutil
        for d in [text_chunks_dir, audio_chunks_dir]:
            if d.exists() and d.is_dir():
                print(f"🗑️ CLEARING DIRECTORY: {d}")
                shutil.rmtree(d)

        for d in [output_root, tts_dir, text_chunks_dir, audio_chunks_dir]:
            d.mkdir(parents=True, exist_ok=True)
    else:
        print(f"✅ RESUME MODE: Preserving existing chunks in {audio_chunks_dir}")
        # Ensure directories exist for resume
        for d in [output_root, tts_dir, text_chunks_dir, audio_chunks_dir]:
            d.mkdir(parents=True, exist_ok=True)

    setup_logging(output_root)

    # Load existing chunks from JSON (resume should use preprocessed data)
    from modules.tts_engine import find_chunks_json_file
    
    json_file = find_chunks_json_file(book_dir.name)
    if json_file:
        print(f"📖 Loading preprocessed chunks from: {json_file.name}")
        from wrapper.chunk_loader import load_chunks
        all_chunks = load_chunks(str(json_file))
        print(f"✅ Loaded {len(all_chunks)} chunks with metadata")
    else:
        print(f"❌ No preprocessed chunks found for {book_dir.name}")
        print(f"💡 Use Option 1 to process this book from the beginning first.")
        return None, None, []

    # Validate resume point
    if not validate_resume_point(start_chunk, len(all_chunks)):
        return None, None, []

    # Filter chunks to process (resume logic)
    if start_chunk > 1:
        print(f"🔄 Resuming from chunk {start_chunk}")
        print(f"📊 Skipping chunks 1-{start_chunk-1} (already completed)")

        # Check which chunks already exist
        existing_chunks = []
        for i in range(start_chunk-1):
            chunk_path = audio_chunks_dir / f"chunk_{i+1:05}.wav"
            if chunk_path.exists():
                existing_chunks.append(i+1)

        print(f"✅ Found {len(existing_chunks)} existing chunks")

        # Only process remaining chunks
        chunks_to_process = all_chunks[start_chunk-1:]
        chunk_offset = start_chunk - 1
    else:
        chunks_to_process = all_chunks
        chunk_offset = 0

    run_log_lines = [
        f"\n===== RESUME Processing: {book_dir.name} =====",
        f"Voice: {voice_path.name}",
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Resume from chunk: {start_chunk}",
        f"Text files processed: {len(text_files)}",
        f"Total chunks generated: {len(all_chunks)}",
        f"Chunks to process: {len(chunks_to_process)}"
    ]

    # Write initial run info immediately
    initial_log = run_log_lines + [
        f"--- Generation Settings ---",
        f"Batch Processing: Enabled ({BATCH_SIZE} chunks per batch)",
        f"ASR Enabled: {ENABLE_ASR}",
        f"Hum Detection: {ENABLE_HUM_DETECTION}",
        f"Dynamic Workers: {USE_DYNAMIC_WORKERS}",
        f"Voice used: {voice_path.name}",
        f"Exaggeration: {tts_params['exaggeration']}",
        f"CFG weight: {tts_params['cfg_weight']}",
        f"Temperature: {tts_params['temperature']}",
        f"Processing Status: IN PROGRESS...",
        f"="*50
    ]

    log_run("\n".join(initial_log), output_root / "run.log")
    print(f"📝 Initial run info written to: {output_root / 'run.log'}")

    start_time = time.time()
    total_chunks = len(all_chunks)
    remaining_chunks = len(chunks_to_process)
    log_path = output_root / "chunk_validation.log"

    # Calculate existing audio duration for accurate progress
    total_audio_duration = 0.0
    if start_chunk > 1:
        print("📊 Calculating existing audio duration...")
        for i in range(start_chunk-1):
            chunk_path = audio_chunks_dir / f"chunk_{i+1:05}.wav"
            if chunk_path.exists():
                total_audio_duration += get_chunk_audio_duration(chunk_path)
        print(f"📊 Existing audio: {timedelta(seconds=int(total_audio_duration))}")

    # Batch processing for remaining chunks
    print(f"📊 Processing {remaining_chunks} remaining chunks in batches of {BATCH_SIZE}")

    all_results = []

    for batch_start in range(0, remaining_chunks, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, remaining_chunks)
        batch_chunks = chunks_to_process[batch_start:batch_end]

        actual_start_chunk = chunk_offset + batch_start + 1
        actual_end_chunk = chunk_offset + batch_end

        print(f"\n🔄 Processing batch: chunks {actual_start_chunk}-{actual_end_chunk}")

        # Fresh model for each batch
        model = load_optimized_model(device)
        compatible_voice = ensure_voice_sample_compatibility(voice_path, output_dir=tts_dir)
        model.prepare_conditionals(compatible_voice, exaggeration=tts_params['exaggeration'])

        # Load ASR model once per batch if needed using adaptive manager
        asr_model = None
        asr_device_used = None
        if ENABLE_ASR:
            from modules.asr_manager import load_asr_model_adaptive
            print(f"🎤 Loading ASR model for resume mode...")
            # Resume mode uses fallback config (no intelligent selection)
            asr_model, asr_device_used = load_asr_model_adaptive()

        futures = []
        batch_results = []

        # Dynamic worker allocation
        optimal_workers = get_optimal_workers()
        print(f"🔧 Using {optimal_workers} workers for batch {actual_start_chunk}-{actual_end_chunk}")

        with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
            for i, chunk_data in enumerate(batch_chunks):
                global_chunk_index = chunk_offset + batch_start + i

                # Check for shutdown request
                if shutdown_requested:
                    print(f"\n⏹️ {YELLOW}Stopping submission of new chunks...{RESET}")
                    break

                chunk = chunk_data["text"]
                all_chunk_texts = [cd["text"] for cd in all_chunks]
                boundary_type = chunk_data.get("boundary_type", "none")

                futures.append(executor.submit(
                    process_one_chunk,
                    global_chunk_index, chunk, text_chunks_dir, audio_chunks_dir,
                    voice_path, tts_params, start_time, total_chunks,
                    punc_norm, book_dir.name, log_run, log_path, device,
                    model, asr_model, all_chunk_texts, boundary_type
                ))

            # Wait for batch to complete
            print(f"🔄 {CYAN}Waiting for batch {actual_start_chunk}-{actual_end_chunk} to complete...{RESET}")
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
                            current_chunk = chunk_offset + batch_start + completed_count
                            log_chunk_progress(current_chunk - 1, total_chunks, start_time, total_audio_duration)

                except Exception as e:
                    logging.error(f"Future failed in batch: {e}")

        # Clean up model after batch
        print(f"🧹 Cleaning up after batch {actual_start_chunk}-{actual_end_chunk}")
        del model
        if asr_model:
            from modules.asr_manager import cleanup_asr_model
            cleanup_asr_model(asr_model)
        torch.cuda.empty_cache()
        import gc
        gc.collect()
        time.sleep(2)

        all_results.extend(batch_results)
        print(f"✅ Batch {actual_start_chunk}-{actual_end_chunk} completed ({len(batch_results)} chunks)")

    # Final processing - combine ALL chunks (existing + new)
    quarantine_dir = audio_chunks_dir / "quarantine"
    pause_for_chunk_review(quarantine_dir)

    # Collect ALL chunk paths (both existing and newly created)
    chunk_paths = []
    for i in range(total_chunks):
        chunk_path = audio_chunks_dir / f"chunk_{i+1:05}.wav"
        if chunk_path.exists():
            chunk_paths.append(chunk_path)
        else:
            logging.warning(f"Missing chunk file: chunk_{i+1:05}.wav")

    if not chunk_paths:
        logging.info(f"{RED}❌ No valid audio chunks found. Skipping concatenation and conversion.{RESET}")
        return None, None, []

    print(f"📊 Found {len(chunk_paths)} total chunks for final audiobook")

    # Calculate timing
    elapsed_total = time.time() - start_time
    elapsed_td = timedelta(seconds=int(elapsed_total))

    # Get total audio duration from ALL chunks
    total_audio_duration_final = sum(get_chunk_audio_duration(chunk_path) for chunk_path in chunk_paths)
    audio_duration_td = timedelta(seconds=int(total_audio_duration_final))
    realtime_factor = total_audio_duration_final / elapsed_total if elapsed_total > 0 else 0.0

    print(f"\n⏱️ Resume Processing Complete:")
    print(f"   Elapsed Time: {CYAN}{str(elapsed_td)}{RESET}")
    print(f"   Audio Duration: {GREEN}{str(audio_duration_td)}{RESET}")
    print(f"   Realtime Factor: {YELLOW}{realtime_factor:.2f}x{RESET}")

    # Combine audio
    combined_wav_path = output_root / f"{book_dir.name} [{voice_path.stem}].wav"
    print("\n💾 Saving WAV file...")
    combine_audio_chunks(chunk_paths, combined_wav_path)

    # M4B conversion
    temp_m4b_path = output_root / "output.m4b"
    final_m4b_path = output_root / f"{book_dir.name}[{voice_path.stem}].m4b"
    convert_to_m4b(combined_wav_path, temp_m4b_path)
    add_metadata_to_m4b(temp_m4b_path, final_m4b_path, cover_file, nfo_file)

    logging.info(f"Audiobook created: {final_m4b_path}")

    # Append final completion info
    completion_log = [
        f"\n--- Resume Processing Complete ---",
        f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Processing Time: {str(elapsed_td)}",
        f"Audio Duration: {str(audio_duration_td)}",
        f"Realtime Factor: {realtime_factor:.2f}x",
        f"Total Chunks: {len(chunk_paths)}",
        f"Combined WAV: {combined_wav_path}",
        f"Final M4B: {final_m4b_path}"
    ]

    # Append to existing log
    log_run("\n".join(completion_log), output_root / "run.log")
    print(f"📝 Final completion info appended to: {output_root / 'run.log'}")

    return final_m4b_path, combined_wav_path, run_log_lines

def resume_book_from_chunk(start_chunk):
    """Interactive resume function for stuck book"""
    print(f"\n🔄 Resume Book Processing from Chunk {start_chunk}")
    print("=" * 50)

    # Show available books from Audiobook directory (books that have started processing)
    audiobook_root = Path(AUDIOBOOK_ROOT)
    if not audiobook_root.exists():
        print(f"{RED}No audiobook directory found at {AUDIOBOOK_ROOT}.{RESET}")
        return None
        
    book_dirs = sorted([d for d in audiobook_root.iterdir() if d.is_dir() and d.name != "Audio_Revisions"])
    if not book_dirs:
        print(f"{RED}No books found in {AUDIOBOOK_ROOT}/ - no books have started processing.{RESET}")
        print(f"💡 Use Option 1 to start processing a new book first.")
        return None

    print("Available books (in progress or completed):")
    for i, book_dir in enumerate(book_dirs):
        # All books in Audiobook/ should have processing data
        audio_chunks_dir = book_dir / "TTS" / "audio_chunks"
        if audio_chunks_dir.exists():
            last_chunk, missing = analyze_existing_chunks(audio_chunks_dir)
            if missing:
                status = f"(last chunk: {last_chunk}, {len(missing)} missing)"
            else:
                status = f"(completed: {last_chunk} chunks)"
        else:
            status = "(processing started but no chunks yet)"

        print(f"  [{i}] {book_dir.name} {status}")

    while True:
        try:
            book_idx = int(input("Select book index: "))
            if 0 <= book_idx < len(book_dirs):
                audiobook_dir = book_dirs[book_idx]
                # Find corresponding Text_Input directory
                text_input_book_dir = TEXT_INPUT_ROOT / audiobook_dir.name
                if text_input_book_dir.exists():
                    book_dir = text_input_book_dir
                else:
                    print(f"❌ Text_Input directory not found for {audiobook_dir.name}")
                    print(f"💡 The original book files may have been moved or deleted.")
                    continue
                break
        except Exception:
            pass
        print("Invalid selection. Try again.")

    # Analyze existing chunks for selected book
    audiobook_dir = AUDIOBOOK_ROOT / book_dir.name
    if audiobook_dir.exists():
        audio_chunks_dir = audiobook_dir / "TTS" / "audio_chunks"
        if audio_chunks_dir.exists():
            last_chunk, missing = analyze_existing_chunks(audio_chunks_dir)
            suggested_resume = suggest_resume_point(last_chunk, missing)

            print(f"\nSuggested resume point: {GREEN}{suggested_resume}{RESET}")

            # Allow user to override
            user_input = input(f"Resume from chunk [{suggested_resume}]: ").strip()
            if user_input:
                try:
                    start_chunk = int(user_input)
                except ValueError:
                    print(f"Invalid input, using suggested: {suggested_resume}")
                    start_chunk = suggested_resume
            else:
                start_chunk = suggested_resume

    # Show available voices
    voice_files = list_voice_samples()
    if not voice_files:
        print(f"{RED}No voice samples found.{RESET}")
        return None

    print("\nAvailable voices:")
    for i, voice in enumerate(voice_files):
        print(f"  [{i}] {voice.name}")

    while True:
        try:
            voice_idx = int(input("Select voice index: "))
            if 0 <= voice_idx < len(voice_files):
                voice_path = voice_files[voice_idx]
                break
        except Exception:
            pass
        print("Invalid selection. Try again.")

    # Get TTS parameters
    def prompt_float(prompt, default):
        val = input(f"{prompt} [{default}]: ").strip()
        return float(val) if val else default

    exaggeration = prompt_float("Enter exaggeration (emotion intensity)", DEFAULT_EXAGGERATION)
    cfg_weight = prompt_float("Enter cfg_weight (faithfulness to text)", DEFAULT_CFG_WEIGHT)
    temperature = prompt_float("Enter temperature (randomness)", DEFAULT_TEMPERATURE)

    tts_params = dict(exaggeration=exaggeration, cfg_weight=cfg_weight, temperature=temperature)

    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"\n🚀 Resuming {book_dir.name} from chunk {start_chunk}")
    print(f"🎤 Voice: {voice_path.name}")
    print(f"⚙️ Parameters: {tts_params}")

    # Process with resume
    return process_book_folder_resume(book_dir, voice_path, tts_params, device, start_chunk)

def find_incomplete_books():
    """Find books that appear to be incomplete"""
    incomplete_books = []

    for book_dir in TEXT_INPUT_ROOT.iterdir():
        if not book_dir.is_dir():
            continue

        audiobook_dir = AUDIOBOOK_ROOT / book_dir.name
        if not audiobook_dir.exists():
            continue

        audio_chunks_dir = audiobook_dir / "TTS" / "audio_chunks"
        if not audio_chunks_dir.exists():
            continue

        # Check if there's a final M4B
        m4b_files = list(audiobook_dir.glob("*.m4b"))
        wav_files = list(audiobook_dir.glob("*.wav"))

        if not m4b_files and not wav_files:
            # No final output, likely incomplete
            last_chunk, missing = analyze_existing_chunks(audio_chunks_dir)
            if last_chunk > 0:
                incomplete_books.append({
                    "name": book_dir.name,
                    "last_chunk": last_chunk,
                    "missing_chunks": len(missing),
                    "path": book_dir
                })

    return incomplete_books

def auto_resume_incomplete():
    """Automatically suggest resume for incomplete books"""
    incomplete = find_incomplete_books()

    if not incomplete:
        print(f"{GREEN}✅ No incomplete books found!{RESET}")
        return

    print(f"{YELLOW}📋 Found {len(incomplete)} incomplete books:{RESET}")
    for i, book in enumerate(incomplete):
        print(f"  [{i}] {book['name']} (last chunk: {book['last_chunk']}, missing: {book['missing_chunks']})")

    choice = input(f"\nSelect book to resume [0-{len(incomplete)-1}] or 'q' to quit: ").strip()

    if choice.lower() == 'q':
        return

    try:
        idx = int(choice)
        if 0 <= idx < len(incomplete):
            selected_book = incomplete[idx]
            suggested_resume = selected_book['last_chunk'] + 1

            print(f"\n🎯 Selected: {selected_book['name']}")
            print(f"💡 Suggested resume point: chunk {suggested_resume}")

            return resume_book_from_chunk(suggested_resume)
    except ValueError:
        print("Invalid selection.")

    return None
