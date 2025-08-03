#!/usr/bin/env python3
"""
GenTTS Wrapper Launcher
Unified CLI tool for synthesis, chunking, and audio revision
"""

import sys
import logging
from modules.text_processor import sentence_chunk_text, smart_punctuate, test_chunking, detect_content_boundaries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wrapper.chunk_loader import save_chunks, load_chunks
from wrapper.chunk_tool import run_chunk_repair_tool
from modules.resume_handler import resume_book_from_chunk, find_incomplete_books
from tools.combine_only import run_combine_only_mode
from pathlib import Path
from interface import main
from config.config import *

def prompt_menu(options):
    print("\nSelect an option:")
    for idx, label in enumerate(options, 1):
        print(f" [{idx}] {label}")
    print(" [0] Exit")

    while True:
        try:
            choice = input("Enter number: ").strip()
            if choice.isdigit():
                idx = int(choice)
                if idx == 0:
                    print("Exiting. See you next time.")
                    return None
                if 1 <= idx <= len(options):
                    return idx
            print("Invalid input. Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print(f"\n❌ Input error - unable to read selection.")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

from modules.tts_engine import generate_enriched_chunks

def prepare_chunk_file():
    """Unified chunk prep that calls the centralized chunk generation function."""
    print("\n📝 Prepare Text File for Chunking")
    print("=" * 40)

    # Show available books from Text_Input directory
    text_input_dir = Path(TEXT_INPUT_ROOT)
    if not text_input_dir.exists():
        print(f"❌ Text_Input directory not found: {TEXT_INPUT_ROOT}")
        return

    book_dirs = [d for d in text_input_dir.iterdir() if d.is_dir()]
    if not book_dirs:
        print(f"❌ No book directories found in {TEXT_INPUT_ROOT}")
        return

    print("\n📚 Available books:")
    for i, book_dir in enumerate(book_dirs):
        txt_files = list(book_dir.glob("*.txt"))
        print(f"  [{i}] {book_dir.name} ({len(txt_files)} .txt file(s))")

    # Select book
    while True:
        try:
            choice = input(f"\nSelect book [0-{len(book_dirs)-1}]: ").strip()
            book_idx = int(choice)
            if 0 <= book_idx < len(book_dirs):
                selected_book_dir = book_dirs[book_idx]
                break
            else:
                print(f"❌ Please enter a number between 0 and {len(book_dirs)-1}")
        except (ValueError, EOFError, KeyboardInterrupt):
            print("❌ Invalid selection or cancelled")
            return

    # Find text files in selected book
    txt_files = list(selected_book_dir.glob("*.txt"))
    if not txt_files:
        print(f"❌ No .txt files found in {selected_book_dir.name}")
        return

    # Select text file if multiple exist
    if len(txt_files) == 1:
        selected_txt_file = txt_files[0]
        print(f"📄 Using: {selected_txt_file.name}")
    else:
        print(f"\n📄 Multiple .txt files found in {selected_book_dir.name}:")
        for i, txt_file in enumerate(txt_files):
            print(f"  [{i}] {txt_file.name}")

        while True:
            try:
                choice = input(f"\nSelect text file [0-{len(txt_files)-1}]: ").strip()
                file_idx = int(choice)
                if 0 <= file_idx < len(txt_files):
                    selected_txt_file = txt_files[file_idx]
                    break
                else:
                    print(f"❌ Please enter a number between 0 and {len(txt_files)-1}")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("❌ Invalid selection or cancelled")
                return

    # Get TTS parameters for JSON generation (optional - uses config defaults if skipped)
    print(f"\n⚙️ TTS Parameters (for VADER sentiment analysis base values)")
    print(f"Press Enter to use config defaults, or enter custom values:")

    def get_float_input(prompt, default):
        while True:
            try:
                value = input(f"{prompt} [{default}]: ").strip()
                if not value:
                    return default
                return float(value)
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid number.")

    def get_yes_no_input(prompt, default=True):
        while True:
            default_str = "Y/n" if default else "y/N"
            value = input(f"{prompt} [{default_str}]: ").strip().lower()
            if not value:
                return default
            if value in ['y', 'yes']:
                return True
            elif value in ['n', 'no']:
                return False
            else:
                print(f"❌ Please enter 'y' for yes or 'n' for no.")

    # VADER sentiment analysis option
    use_vader = get_yes_no_input("🎭 Use VADER sentiment analysis to adjust TTS params per chunk?", True)

    if use_vader:
        print("✅ VADER enabled - TTS params will be adjusted based on chunk sentiment")
    else:
        print("❌ VADER disabled - TTS params will be fixed for all chunks")

    user_tts_params = {
        'exaggeration': get_float_input("Exaggeration", DEFAULT_EXAGGERATION),
        'cfg_weight': get_float_input("CFG Weight", DEFAULT_CFG_WEIGHT),
        'temperature': get_float_input("Temperature", DEFAULT_TEMPERATURE),
        'use_vader': use_vader
    }

    # Process the selected file
    book_name = selected_book_dir.name
    text_output_dir = AUDIOBOOK_ROOT / book_name / "TTS" / "text_chunks"
    text_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔄 Processing: {selected_txt_file}")
    enriched_chunks = generate_enriched_chunks(selected_txt_file, text_output_dir, user_tts_params)

    print(f"\n✅ Processing Complete!")
    print(f"📊 Generated {len(enriched_chunks)} chunks from: {selected_txt_file.name}")
    print(f"💾 Saved to:")
    print(f"  📁 JSON metadata: {text_output_dir / 'chunks_info.json'}")
    print(f"\n💡 You can now:")
    print(f"   • Use Option 1 to convert {book_name} to audiobook")
    print(f"   • Use Option 6 to repair/edit chunks if needed")


def main_with_resume():
    """Modified main function that includes resume option"""
    print(f"{RED}DNXS-Spokenword []ChatterboxTTS] Batch Audiobook Generator\n{RESET}")

    print("Select an action:")
    print(" 1. Convert a book (normal processing)")
    print(" 2. Resume a book from specific chunk")
    print(" 3. Re-concatenate audio_chunks into audiobook (combine only)")

    try:
        mode = input("Enter option number [1/2/3]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("❌ Input cancelled")
        return

    if mode == "2":
        try:
            start_chunk = int(input("Enter chunk number to resume from: "))
            return resume_book_from_chunk(start_chunk)
        except (EOFError, KeyboardInterrupt):
            print("❌ Input cancelled")
            return
    elif mode == "3":
        return run_combine_only_mode()
    else:
        return main()  # Your existing main function


def wrapper_main():
    options = [
        "Convert a book (GenTTS)",
        "Resume from specific chunk",
        "Combine audio chunks into audiobook",
        "Prepare text file for chunking",
        "Test chunking logic",
        "Launch Chunk Repair / Revision Tool",
        "Generate audio from edited JSON"
    ]

    while True:
        selected = prompt_menu(options)
        if selected is None:
            break
        elif selected == 1:
            main()
        elif selected == 2:
            try:
                print("\n🔄 Resume Processing from Specific Chunk")
                print("📋 The system will guide you through:")
                print("   1. Book selection")
                print("   2. Existing chunk analysis")
                print("   3. Resume point suggestion")
                print("   4. Voice and parameter selection")
                print()

                # Call the interactive resume function - it handles everything
                result = resume_book_from_chunk(0)  # Will be overridden by interactive selection
                if result:
                    print("✅ Resume operation completed successfully")
                else:
                    print("❌ Resume operation was cancelled or failed")

            except (EOFError, KeyboardInterrupt):
                print("❌ Resume operation cancelled.")
        elif selected == 3:
            run_combine_only_mode()
        elif selected == 4:
            prepare_chunk_file()
        elif selected == 5:
            try:
                test_text = input("Enter test text (or press Enter to use default): ").strip()
                max_words = int(input("Max words per chunk [30]: ") or "30")
                min_words = int(input("Min words per chunk [4]: ") or "4")
                test_chunking(test_text if test_text else None, max_words, min_words)
            except (EOFError, KeyboardInterrupt):
                print("❌ Input cancelled")
        elif selected == 6:
            run_chunk_repair_tool()
        elif selected == 7:
            from utils.generate_from_json import main as generate_from_json_main
            generate_from_json_main()

if __name__ == "__main__":
    wrapper_main()
main = wrapper_main
