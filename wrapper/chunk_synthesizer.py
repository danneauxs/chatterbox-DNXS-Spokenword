from pathlib import Path
import torch
import time
from pydub import AudioSegment

from modules.tts_engine import load_optimized_model
from modules.file_manager import ensure_voice_sample_compatibility, list_voice_samples
from modules.audio_processor import apply_smart_fade_memory, smart_audio_validation_memory, process_audio_with_trimming_and_silence
from config.config import *

def synthesize_chunk(chunk, index, book_name, audio_dir, revision=False):
    """Generate audio for a single chunk using simplified TTS process"""
    filename = f"chunk_{index+1:05d}_rev.wav" if revision else f"chunk_{index+1:05d}.wav"
    out_path = Path(audio_dir) / filename
    
    try:
        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load TTS model
        print(f"🤖 Loading TTS model for chunk synthesis...")
        model = load_optimized_model(device)
        
        # Get voice sample - use first available voice for now
        voice_files = list_voice_samples()
        if not voice_files:
            print("❌ No voice samples found")
            return None
            
        voice_path = voice_files[0]  # Use first available voice
        compatible_voice = ensure_voice_sample_compatibility(voice_path)
        
        # Prepare model with voice
        model.prepare_conditionals(compatible_voice, exaggeration=1.0)
        
        # Get chunk text
        chunk_text = chunk.get('text', '')
        if not chunk_text:
            print("❌ No text found in chunk")
            return None
            
        print(f"🎤 Synthesizing: {chunk_text[:50]}...")
        
        # Generate audio
        with torch.no_grad():
            wav = model.generate(chunk_text, 
                               exaggeration=1.0,
                               cfg_weight=0.7, 
                               temperature=0.7).detach().cpu()
        
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
