from pathlib import Path
import torch
import time
import re
from pydub import AudioSegment

from modules.tts_engine import load_optimized_model
from modules.file_manager import ensure_voice_sample_compatibility, list_voice_samples
from modules.audio_processor import apply_smart_fade_memory, smart_audio_validation_memory, process_audio_with_trimming_and_silence
from config.config import *

def get_original_voice_from_log(book_name):
    """Extract original voice name from run log"""
    audiobook_root = Path(AUDIOBOOK_ROOT)
    log_file = audiobook_root / book_name / "run.log"
    
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Voice: ") or line.startswith("Voice used: "):
                        voice_name = line.split(": ", 1)[1].strip()
                        print(f"📄 Found original voice in log: {voice_name}")
                        return voice_name
        except Exception as e:
            print(f"⚠️ Error reading run log: {e}")
    
    return None

def get_original_voice_from_filename(book_name):
    """Extract voice name from existing audiobook filename"""
    audiobook_root = Path(AUDIOBOOK_ROOT)
    book_dir = audiobook_root / book_name
    
    # Look for WAV files with voice pattern: BookName [VoiceName].wav
    for wav_file in book_dir.glob("*.wav"):
        match = re.search(r'\[([^\]]+)\]\.wav$', wav_file.name)
        if match:
            voice_name = match.group(1)
            print(f"📁 Found original voice in filename: {voice_name}")
            return voice_name
    
    # Look for M4B files with voice pattern: BookName[VoiceName].m4b
    for m4b_file in book_dir.glob("*.m4b"):
        match = re.search(r'\[([^\]]+)\]\.m4b$', m4b_file.name)
        if match:
            voice_name = match.group(1)
            print(f"📁 Found original voice in M4B filename: {voice_name}")
            return voice_name
    
    return None

def find_voice_file_by_name(voice_name):
    """Find voice file by name in Voice_Samples directory"""
    voice_files = list_voice_samples()
    
    # Exact match first
    for voice_file in voice_files:
        if voice_file.stem == voice_name:
            print(f"✅ Found exact voice match: {voice_file.name}")
            return voice_file
    
    # Partial match (case insensitive)
    voice_name_lower = voice_name.lower()
    for voice_file in voice_files:
        if voice_name_lower in voice_file.stem.lower():
            print(f"✅ Found partial voice match: {voice_file.name}")
            return voice_file
    
    return None

def get_tts_params_for_chunk(chunk):
    """Extract TTS parameters from chunk data or prompt user"""
    # Check if chunk has TTS params stored
    if 'tts_params' in chunk:
        tts_params = chunk['tts_params']
        print(f"📊 Using stored TTS params: exag={tts_params.get('exaggeration', 1.0)}, cfg={tts_params.get('cfg_weight', 0.7)}, temp={tts_params.get('temperature', 0.7)}")
        return tts_params
    
    # Prompt user for TTS parameters
    print(f"\n⚙️ TTS Parameters for chunk synthesis:")
    
    def get_float_input(prompt, default):
        while True:
            try:
                value = input(f"{prompt} [{default}]: ").strip()
                if not value:
                    return default
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

def synthesize_chunk(chunk, index, book_name, audio_dir, revision=False, chunks_json_path=None, override_voice_name=None):
    """Generate audio for a single chunk using specified or detected voice and TTS parameters"""
    filename = f"chunk_{index+1:05d}_rev.wav" if revision else f"chunk_{index+1:05d}.wav"
    out_path = Path(audio_dir) / filename
    
    try:
        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load TTS model
        print(f"🤖 Loading TTS model for chunk synthesis...")
        model = load_optimized_model(device)
        
        # Determine voice to use
        if override_voice_name:
            # Use explicitly provided voice
            print(f"🎤 Using explicitly selected voice: {override_voice_name}")
            voice_path = find_voice_file_by_name(override_voice_name)
            voice_name = override_voice_name
            detection_method = "user_selected"
        else:
            # Use enhanced voice detection
            print(f"🔍 Detecting original voice for book: {book_name}")
            from modules.voice_detector import detect_voice_for_book
            
            voice_name, voice_path, detection_method = detect_voice_for_book(book_name, chunks_json_path)
        
        # Fallback to first available voice if detection failed
        if not voice_path:
            print(f"⚠️ Voice not found, using first available voice")
            voice_files = list_voice_samples()
            if not voice_files:
                print("❌ No voice samples found")
                return None
            voice_path = voice_files[0]
            voice_name = voice_path.stem
            detection_method = "fallback_first_available"
        
        print(f"🎤 Using voice: {voice_name} (method: {detection_method})")
        compatible_voice = ensure_voice_sample_compatibility(voice_path)
        
        # Get TTS parameters for this chunk
        tts_params = get_tts_params_for_chunk(chunk)
        
        # Pre-warm model to eliminate first chunk quality variations
        from modules.tts_engine import prewarm_model_with_voice
        model = prewarm_model_with_voice(model, compatible_voice, tts_params)
        
        # Get chunk text
        chunk_text = chunk.get('text', '')
        if not chunk_text:
            print("❌ No text found in chunk")
            return None
            
        print(f"🎤 Synthesizing: {chunk_text[:50]}...")
        print(f"📊 TTS params: exag={tts_params['exaggeration']}, cfg={tts_params['cfg_weight']}, temp={tts_params['temperature']}")
        
        # Generate audio with specified parameters
        with torch.no_grad():
            wav = model.generate(chunk_text, 
                               exaggeration=tts_params['exaggeration'],
                               cfg_weight=tts_params['cfg_weight'], 
                               temperature=tts_params['temperature']).detach().cpu()
        
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
            
        # Convert tensor to AudioSegment for processing
        import io
        import soundfile as sf
        
        wav_np = wav.squeeze().numpy()
        with io.BytesIO() as wav_buffer:
            sf.write(wav_buffer, wav_np, model.sr, format='wav')
            wav_buffer.seek(0)
            audio_segment = AudioSegment.from_wav(wav_buffer)
        
        # Apply audio processing
        audio_segment = apply_smart_fade_memory(audio_segment)
        audio_segment, is_quarantined = smart_audio_validation_memory(audio_segment, model.sr)
        
        # Apply trimming and contextual silence based on boundary type
        boundary_type = chunk.get('boundary_type', 'none')
        if boundary_type and boundary_type != "none":
            audio_segment = process_audio_with_trimming_and_silence(audio_segment, boundary_type)
        else:
            # Apply trimming even without boundary type if enabled
            if ENABLE_AUDIO_TRIMMING:
                from modules.audio_processor import trim_audio_endpoint
                audio_segment = trim_audio_endpoint(audio_segment)
            
        # Save final audio
        audio_segment.export(out_path, format="wav")
        print(f"✅ Saved synthesized chunk: {out_path.name}")
        
        # Clean up model
        del model
        torch.cuda.empty_cache()
        
        return str(out_path)
        
    except Exception as e:
        print(f"❌ Failed to synthesize chunk: {e}")
        import traceback
        traceback.print_exc()
        return None
