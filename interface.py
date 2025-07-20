"""
==============================================================================
ENHANCED GENTTS AUDIOBOOK GENERATOR - MODULAR VERSION
==============================================================================
A high-performance, enterprise-grade TTS audiobook production system built on
ChatterboxTTS with advanced quality control, memory management, and performance
optimization features.

This is the main orchestration module that coordinates all the modular components:
- Text processing (modules/text_processor.py)
- Audio processing (modules/audio_processor.py) 
- TTS engine management (modules/tts_engine.py)
- File operations (modules/file_manager.py)
- Progress tracking (modules/progress_tracker.py)
- Resume functionality (modules/resume_handler.py)

USAGE MODES:
1. Interactive book selection with voice and parameter configuration
2. Batch processing queue for multiple books
3. Combine-only mode for re-assembling existing chunks
4. Single chunk testing for parameter optimization

AUTHOR: Enhanced by Claude (Anthropic) for optimized audiobook production
VERSION: 3.0 Modular - Clean Architecture Edition
LICENSE: Open source - Use responsibly for legal content only
==============================================================================
"""

import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="LlamaModel is using LlamaSdpaAttention")
warnings.filterwarnings("ignore", message="We detected that you are passing `past_key_values`")
warnings.filterwarnings("ignore")

# Import core libraries
import os
import sys
import signal
import torch
import argparse
from pathlib import Path
from chatterbox.tts import ChatterboxTTS

# Set environment and suppress warnings
sys.stdout.flush()
os.environ["TORCH_HUB_DIR"] = "/tmp/torch_hub_silent"

# Import modular components
from config.config import *
from modules.text_processor import (
    sentence_chunk_text, smart_punctuate, detect_content_boundaries
)
from chatterbox.tts import punc_norm
from modules.audio_processor import (
    smart_audio_validation, add_contextual_silence, pause_for_chunk_review
)
from modules.tts_engine import (
    monitor_gpu_activity, optimize_memory_usage, load_optimized_model,
    patch_alignment_layer, process_one_chunk, process_book_folder
)
from modules.file_manager import (
    list_voice_samples, ensure_voice_sample_compatibility, chunk_sort_key,
    convert_to_m4b, add_metadata_to_m4b, combine_audio_chunks, find_book_files,
    save_chunk_info
)
from modules.progress_tracker import log_chunk_progress, log_console, log_run, setup_logging
from modules.resume_handler import process_book_folder_resume, resume_book_from_chunk
from modules.batch_processor import pipeline_book_processing
from tools.combine_only import run_combine_only_mode

# ============================================================================
# GLOBAL SHUTDOWN HANDLING
# ============================================================================

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    print(f"\n⚠️ {YELLOW}Shutdown requested. Finishing current chunk...{RESET}")
    shutdown_requested = True

signal.signal(signal.SIGINT, signal_handler)

# ============================================================================
# BOOK SELECTION AND PARAMETER PROMPTS
# ============================================================================

def prompt_book_selection(book_dirs, already_selected):
    """Interactive book selection from available directories"""
    available = [d for d in book_dirs if d not in already_selected]
    if not available:
        print("No more books available.")
        return None
    
    print("\nAvailable books:")
    for i, book_dir in enumerate(available, 1):
        print(f" [{i}] {book_dir.name}")
    
    while True:
        try:
            choice = input("Select book number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(available):
                    return available[idx]
            print("Invalid selection. Try again.")
        except (ValueError, KeyboardInterrupt):
            return None

def prompt_voice_selection(voice_files):
    """Interactive voice selection from available samples"""
    print("\nAvailable voices:")
    for i, voice_file in enumerate(voice_files, 1):
        print(f" [{i}] {voice_file.stem}")
    
    while True:
        try:
            choice = input("Select voice number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(voice_files):
                    return voice_files[idx]
            print("Invalid selection. Try again.")
        except (ValueError, KeyboardInterrupt):
            return None

def prompt_tts_params():
    """Interactive TTS parameter configuration"""
    print("\nTTS Parameters:")
    
    def get_float_input(prompt, default):
        while True:
            try:
                value = input(f"{prompt} [{default}]: ").strip() or str(default)
                return float(value)
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid number.")
    
    exaggeration = get_float_input("Exaggeration", DEFAULT_EXAGGERATION)
    cfg_weight = get_float_input("CFG Weight", DEFAULT_CFG_WEIGHT)
    temperature = get_float_input("Temperature", DEFAULT_TEMPERATURE)
    
    return {
        'exaggeration': exaggeration,
        'cfg_weight': cfg_weight,
        'temperature': temperature
    }

# ============================================================================
# MAIN BOOK PROCESSING FUNCTIONS
# ============================================================================

# process_book_folder() now imported from modules.tts_engine

# ============================================================================
# PIPELINE AND UTILITY FUNCTIONS
# ============================================================================

# pipeline_book_processing() now imported from modules.batch_processor

# run_combine_only_mode() now imported from tools.combine_only

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for GenTTS processing"""
    log_console("Enhanced GenTTS v3.0 Modular - Convert text to audiobook", "GREEN")
    
    # Get available books and voices
    book_dirs = [d for d in TEXT_INPUT_ROOT.iterdir() if d.is_dir()]
    voice_files = list_voice_samples()
    
    if not book_dirs:
        print(f"❌ No book directories found in {TEXT_INPUT_ROOT}")
        return
    
    if not voice_files:
        print(f"❌ No voice samples found in {VOICE_SAMPLES_DIR}")
        return
    
    # Interactive selection
    selected_books = []
    while True:
        book_dir = prompt_book_selection(book_dirs, selected_books)
        if not book_dir:
            break
        
        voice_path = prompt_voice_selection(voice_files)
        if not voice_path:
            break
        
        # Ensure voice compatibility
        voice_path = ensure_voice_sample_compatibility(voice_path)
        
        tts_params = prompt_tts_params()
        
        selected_books.append({
            'book_dir': book_dir,
            'voice_path': voice_path,
            'tts_params': tts_params
        })
        
        if input("\nAdd another book? [y/N]: ").lower() != 'y':
            break
    
    if not selected_books:
        print("No books selected.")
        return
    
    # Display configuration
    print(f"\n📋 Processing Queue:")
    for i, book_info in enumerate(selected_books, 1):
        voice_path = book_info['voice_path']
        if voice_path:
            voice_name = Path(voice_path).stem if isinstance(voice_path, str) else voice_path.stem
        else:
            voice_name = "Unknown"
        print(f"  {i}. {book_info['book_dir'].name} -> {voice_name}")
    
    print(f"  Workers: {MAX_WORKERS}")
    print(f"  VRAM Threshold: {VRAM_SAFETY_THRESHOLD}GB")
    print(f"  ASR Enabled: {ENABLE_ASR}")
    print(f"  Hum Detection: {ENABLE_HUM_DETECTION}")
    
    # Process queue
    completed_books = pipeline_book_processing(selected_books)
    
    print(f"\n{GREEN}Processing complete: {len(completed_books)}/{len(selected_books)} books{RESET}")

def main_with_resume():
    """Main entry point with resume option"""
    print(f"{RED}Enhanced ChatterboxTTS Batch Audiobook Generator\n{RESET}")
    
    print("Select an action:")
    print(" 1. Convert a book (normal processing)")
    print(" 2. Resume a book from specific chunk")
    print(" 3. Re-concatenate audio_chunks into audiobook (combine only)")
    
    mode = input("Enter option number [1/2/3]: ").strip()
    
    if mode == "2":
        start_chunk = int(input("Enter chunk number to resume from: "))
        return resume_book_from_chunk(start_chunk)
    elif mode == "3":
        return run_combine_only_mode()
    else:
        return main()

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--enable-asr', action='store_true', help="Enable ASR validation")
    parser.add_argument('--resume', type=int, help="Resume processing from specific chunk number")
    args, unknown = parser.parse_known_args()
    
    # Override ASR setting if specified via command line
    if args.enable_asr:
        ENABLE_ASR = True
    
    if args.resume:
        print(f"Resuming from chunk {args.resume}")
        resume_book_from_chunk(args.resume)
    else:
        main()