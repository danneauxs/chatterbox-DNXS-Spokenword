#!/usr/bin/env python3
"""
Direct Audio Generation from JSON Tool

This script allows for generating audiobook chunks directly from a pre-existing
`chunks_info.json` file. It is intended for debugging and testing purposes,
allowing a user to manually edit the TTS parameters in the JSON file and
hear the results without the VADER analysis step.
"""

import torch
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import timedelta

# Add project root to path to allow module imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config.config import *
from modules.tts_engine import load_optimized_model, process_one_chunk
from modules.file_manager import setup_book_directories, list_voice_samples, ensure_voice_sample_compatibility
from wrapper.chunk_loader import load_chunks
from chatterbox.tts import punc_norm
from modules.progress_tracker import log_chunk_progress, log_run

def main():
    """Main function to drive the generation process."""
    print(f"{BOLD}{CYAN}--- Direct Audio Generation from JSON Tool ---\{RESET}")
    
    # 1. Get Book Name
    book_name = input("Enter the book name (e.g., 'london'): ").strip()
    if not book_name:
        print("❌ Book name cannot be empty.")
        return

    # 2. Locate and Load JSON
    book_audio_dir = AUDIOBOOK_ROOT / book_name
    json_path = book_audio_dir / "TTS" / "text_chunks" / "chunks_info.json"

    if not json_path.exists():
        print(f"❌ Error: JSON file not found at {json_path}")
        print("Please ensure you have run the 'Prepare text file' option for this book first.")
        return

    print(f"📖 Loading chunks from: {json_path}")
    all_chunks = load_chunks(str(json_path))
    print(f"✅ Found {len(all_chunks)} chunks.")

    # 3. Select Voice
    voice_files = list_voice_samples()
    if not voice_files:
        print(f"❌ No voice samples found in {VOICE_SAMPLES_DIR}")
        return

    print("\nAvailable voices:")
    for i, voice_file in enumerate(voice_files, 1):
        print(f" [{i}] {voice_file.stem}")
    
    while True:
        try:
            choice = input("Select voice number: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(voice_files):
                voice_path = voice_files[idx]
                break
            print("Invalid selection.")
        except (ValueError, IndexError):
            print("Invalid selection.")
    
    # Ensure voice compatibility
    voice_path = ensure_voice_sample_compatibility(voice_path)

    # 4. Setup Environment
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    
    print(f"\n🚀 Using device: {device}")
    print(f"🎤 Using voice: {Path(voice_path).name}")

    # 5. Load Model
    model = load_optimized_model(device)
    
    # 6. Prepare voice conditionals (THIS WAS MISSING!)
    print(f"🎤 Preparing voice conditionals with: {Path(voice_path).name}")
    model.prepare_conditionals(voice_path)

    # 7. Process Chunks
    output_root, tts_dir, text_chunks_dir, audio_chunks_dir = setup_book_directories(Path(TEXT_INPUT_ROOT) / book_name)
    
    # Clean existing audio chunks
    print("🧹 Clearing old audio chunks...")
    for wav_file in audio_chunks_dir.glob("*.wav"):
        wav_file.unlink()

    start_time = time.time()
    total_chunks = len(all_chunks)
    log_path = output_root / "debug_generation.log"
    
    print(f"\n🔄 Generating {total_chunks} chunks...")

    with ThreadPoolExecutor(max_workers=2) as executor: # Test parallel processing
        futures = []
        for i, chunk_data in enumerate(all_chunks):
            # Extract exaggeration from JSON, force others to default
            chunk_tts_params = {
                "exaggeration": chunk_data.get("tts_params", {}).get("exaggeration", DEFAULT_EXAGGERATION),
                "cfg_weight": DEFAULT_CFG_WEIGHT,
                "temperature": DEFAULT_TEMPERATURE
            }

            future = executor.submit(
                process_one_chunk,
                i, chunk_data['text'], text_chunks_dir, audio_chunks_dir,
                voice_path, chunk_tts_params, start_time, total_chunks,
                punc_norm, book_name, log_run, log_path, device,
                model, None, all_chunks, chunk_data['boundary_type']
            )
            futures.append(future)

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    idx, _ = result
                    log_chunk_progress(idx, total_chunks, start_time, 0)
            except Exception as e:
                print(f"\n❌ An error occurred while processing a chunk: {e}")

    elapsed_time = time.time() - start_time
    print(f"\n{GREEN}✅ Generation Complete!{RESET}")
    print(f"⏱️ Total time: {timedelta(seconds=int(elapsed_time))}")
    print(f"🔊 Audio chunks are in: {audio_chunks_dir}")
    print("You can now use Option 3 from the main menu to combine them.")

if __name__ == "__main__":
    main()
