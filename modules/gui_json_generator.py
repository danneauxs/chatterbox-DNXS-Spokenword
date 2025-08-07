#!/usr/bin/env python3
"""
GUI JSON Audio Generation Module

This module provides JSON-to-audiobook generation specifically for GUI use.
It's based on utils/generate_from_json.py but adapted for GUI integration.
"""

import torch
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import timedelta

# Add project root to path to allow module imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.config import *
from modules.tts_engine import load_optimized_model, process_one_chunk, prewarm_model_with_voice
from modules.file_manager import setup_book_directories, list_voice_samples, ensure_voice_sample_compatibility
from wrapper.chunk_loader import load_chunks
from src.chatterbox.tts import punc_norm
from modules.progress_tracker import log_chunk_progress, log_run
from tools.combine_only import combine_audio_for_book


def generate_audiobook_from_json(json_path, voice_name, temp_setting=None):
    """
    Generate complete audiobook from JSON chunks file.
    
    Args:
        json_path (str): Path to the JSON chunks file
        voice_name (str): Name of the voice to use (without .wav extension)
        temp_setting (float, optional): Temperature override for TTS
        
    Returns:
        tuple: (success: bool, message: str, audiobook_path: str or None)
    """
    try:
        print(f"🎵 GUI JSON Generator: Starting audiobook generation")
        print(f"📄 JSON file: {json_path}")
        print(f"🎤 Voice: {voice_name}")
        if temp_setting:
            print(f"🌡️ Temperature override: {temp_setting}")
        
        # Determine book name from JSON path
        json_file = Path(json_path)
        
        # Try to extract book name from path structure
        if 'Audiobook' in json_file.parts:
            audiobook_index = json_file.parts.index('Audiobook')
            if audiobook_index + 1 < len(json_file.parts):
                book_name = json_file.parts[audiobook_index + 1]
                print(f"📚 Detected book name from path: {book_name}")
            else:
                raise Exception("Cannot determine book name from Audiobook path")
        elif json_file.stem.endswith('_chunks'):
            book_name = json_file.stem.replace('_chunks', '')
            print(f"📚 Detected book name from filename: {book_name}")
        else:
            book_name = json_file.stem
            print(f"📚 Using filename as book name: {book_name}")

        # Load JSON chunks (READ ONLY - never modify the original)
        print(f"📖 Loading chunks from: {json_path}")
        all_chunks = load_chunks(str(json_path))
        print(f"✅ Found {len(all_chunks)} chunks.")

        # Find voice file
        voice_files = list_voice_samples()
        voice_path = None
        for voice_file in voice_files:
            if voice_file.stem == voice_name:
                voice_path = voice_file
                break
        
        if not voice_path:
            available_voices = [vf.stem for vf in voice_files]
            return False, f"Voice '{voice_name}' not found. Available: {available_voices}", None

        # Ensure voice compatibility
        voice_path = ensure_voice_sample_compatibility(voice_path)
        if isinstance(voice_path, str):
            voice_path = Path(voice_path)
        
        print(f"🎤 Using voice: {voice_path.name}")

        # Setup device
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
        
        print(f"🚀 Using device: {device}")

        # Setup basic TTS parameters for model pre-warming only
        user_tts_params = {
            'exaggeration': DEFAULT_EXAGGERATION,
            'cfg_weight': DEFAULT_CFG_WEIGHT,
            'temperature': DEFAULT_TEMPERATURE
        }
        print(f"🎛️ Pre-warming TTS params: {user_tts_params}")

        # Load TTS model
        print(f"🤖 Loading TTS model...")
        model = load_optimized_model(device)
        
        # Pre-warm model to eliminate first chunk quality variations
        print(f"🔥 Pre-warming model with voice sample...")
        compatible_voice = ensure_voice_sample_compatibility(voice_path)
        model = prewarm_model_with_voice(model, compatible_voice, user_tts_params)

        # Setup output directories
        output_root = AUDIOBOOK_ROOT / book_name
        tts_dir = output_root / "TTS"
        text_chunks_dir = tts_dir / "text_chunks"
        audio_chunks_dir = tts_dir / "audio_chunks"
        
        # Create directories
        for dir_path in [output_root, tts_dir, text_chunks_dir, audio_chunks_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Clean existing audio chunks
        print("🧹 Clearing old audio chunks...")
        for wav_file in audio_chunks_dir.glob("*.wav"):
            wav_file.unlink()

        # Process chunks
        start_time = time.time()
        total_chunks = len(all_chunks)
        log_path = output_root / "gui_json_generation.log"
        
        print(f"🔄 Generating {total_chunks} audio chunks...")

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for i, chunk_data in enumerate(all_chunks):
                # Use ONLY the chunk's TTS params from JSON - no config defaults
                chunk_tts_params = chunk_data.get("tts_params", {})
                
                # If no TTS params in JSON, cannot generate audio
                if not chunk_tts_params or not all(key in chunk_tts_params for key in ['exaggeration', 'cfg_weight', 'temperature']):
                    missing_params = [key for key in ['exaggeration', 'cfg_weight', 'temperature'] if key not in chunk_tts_params]
                    raise ValueError(f"Chunk {i+1} missing required TTS parameters: {missing_params}. Cannot generate audio without complete JSON parameters.")

                future = executor.submit(
                    process_one_chunk,
                    i, chunk_data['text'], text_chunks_dir, audio_chunks_dir,
                    voice_path, chunk_tts_params, start_time, total_chunks,
                    punc_norm, book_name, log_run, log_path, device,
                    model, None, all_chunks, chunk_data.get('boundary_type', 'none')
                )
                futures.append(future)

            # Wait for all chunks to complete
            completed_chunks = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        idx, _ = result
                        completed_chunks += 1
                        log_chunk_progress(idx, total_chunks, start_time, 0)
                        print(f"✅ Completed chunk {completed_chunks}/{total_chunks}")
                except Exception as e:
                    print(f"❌ Error processing chunk: {e}")

        elapsed_time = time.time() - start_time
        print(f"✅ Audio generation complete in {timedelta(seconds=int(elapsed_time))}")
        print(f"🔊 Audio chunks generated in: {audio_chunks_dir}")

        # Combine chunks into final audiobook
        print("🔗 Combining audio chunks into final audiobook...")
        try:
            success = combine_audio_for_book(str(output_root), voice_name)
            if success:
                # Look for the created audiobook file with voice name
                final_m4b = output_root / f"{book_name} [{voice_name}].m4b"
                if final_m4b.exists():
                    print(f"🎉 Audiobook created: {final_m4b.name}")
                    return True, "Audiobook generation completed successfully", str(final_m4b)
                else:
                    return False, "Combine succeeded but final audiobook file not found", None
            else:
                return False, "Failed to combine audio chunks", None
        except Exception as e:
            return False, f"Error combining audio chunks: {e}", None

    except Exception as e:
        error_msg = f"JSON generation error: {e}"
        print(f"❌ {error_msg}")
        return False, error_msg, None


def get_book_name_from_json_path(json_path):
    """
    Extract book name from JSON file path.
    
    Args:
        json_path (str): Path to JSON file
        
    Returns:
        str: Detected book name
    """
    json_file = Path(json_path)
    
    if 'Audiobook' in json_file.parts:
        audiobook_index = json_file.parts.index('Audiobook')
        if audiobook_index + 1 < len(json_file.parts):
            return json_file.parts[audiobook_index + 1]
    
    if json_file.stem.endswith('_chunks'):
        return json_file.stem.replace('_chunks', '')
    
    return json_file.stem


if __name__ == "__main__":
    # CLI compatibility for testing
    print("GUI JSON Generator - use from GUI or import as module")