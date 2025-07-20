"""
Audio Processing Module
Handles audio validation, effects, cleanup, and quality control
"""

import numpy as np
import soundfile as sf
import logging
import shutil
import re
import time
from pathlib import Path
from pydub import AudioSegment, silence
from config.config import *

# ============================================================================
# AUDIO QUALITY DETECTION
# ============================================================================

def check_audio_health(wav_path):
    """Enhanced audio health checking"""
    data, samplerate = sf.read(str(wav_path))
    if len(data.shape) > 1:
        data = data[:, 0]  # mono only

    clipping = np.mean(np.abs(data) > 0.98)
    silence_ratio = np.mean(np.abs(data) < 1e-4)
    rms = np.sqrt(np.mean(data**2))
    mean_abs = np.mean(np.abs(data))
    flatness = mean_abs / (rms + 1e-8)

    return {
        "clipping_ratio": round(clipping, 4),
        "silence_ratio": round(silence_ratio, 4),
        "flatness": round(flatness, 4),
    }

def detect_tts_hum_artifact(wav_path):
    """
    Detect low-frequency TTS confusion hum using configurable parameters
    """
    if not ENABLE_HUM_DETECTION:
        return False, {}

    data, sr = sf.read(str(wav_path))
    if data.ndim > 1:
        data = data[:, 0]  # Mono

    # FFT analysis for frequency content
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1/sr)

    # Focus on hum frequency range (configurable at top of file)
    hum_mask = (freqs >= HUM_FREQ_MIN) & (freqs <= HUM_FREQ_MAX)
    hum_energy = np.sum(np.abs(fft[hum_mask]))
    total_energy = np.sum(np.abs(fft))

    # Check for sustained low-level amplitude (steady hum characteristic)
    segment_size = sr // 4  # 250ms segments
    segments = [data[i:i+segment_size] for i in range(0, len(data)-segment_size, segment_size)]

    steady_segments = 0
    for segment in segments:
        rms = np.sqrt(np.mean(segment**2))
        if HUM_AMPLITUDE_MIN < rms < HUM_AMPLITUDE_MAX:
            steady_segments += 1

    # Calculate hum indicators using configurable thresholds
    hum_ratio = hum_energy / (total_energy + 1e-10)
    steady_ratio = steady_segments / len(segments) if segments else 0

    # Detection logic using configurable thresholds
    has_hum = (hum_ratio > HUM_ENERGY_THRESHOLD) and (steady_ratio > HUM_STEADY_THRESHOLD)

    if has_hum:
        logging.info(f"🔍 TTS hum detected: {wav_path.name}")
        logging.info(f"   Frequency range: {HUM_FREQ_MIN}-{HUM_FREQ_MAX}Hz")
        logging.info(f"   Hum energy ratio: {hum_ratio:.3f} (threshold: {HUM_ENERGY_THRESHOLD})")
        logging.info(f"   Steady segments: {steady_ratio:.3f} (threshold: {HUM_STEADY_THRESHOLD})")

    return has_hum, {
        "hum_ratio": hum_ratio,
        "steady_ratio": steady_ratio,
        "freq_range": f"{HUM_FREQ_MIN}-{HUM_FREQ_MAX}Hz"
    }

def smart_audio_validation(wav_path):
    """Comprehensive audio validation with intelligent responses"""
    # Standard health check
    health = check_audio_health(wav_path)

    # TTS hum detection (if enabled)
    has_hum, hum_metrics = detect_tts_hum_artifact(wav_path)

    # Decision matrix
    if health["clipping_ratio"] > 0.05:
        return handle_problematic_chunks(wav_path, "clipping", health)
    elif health["flatness"] > 0.9:
        return handle_problematic_chunks(wav_path, "corrupted", health)
    elif has_hum:
        return handle_problematic_chunks(wav_path, "tts_hum", hum_metrics)
    else:
        return wav_path  # Passed all checks

def has_mid_energy_drop(wav_tensor, sr, window_ms=250, threshold_ratio=None):
    """Detect mid-chunk energy drops"""
    wav = wav_tensor.squeeze().numpy()
    win_samples = int(sr * window_ms / 1000)
    segments = [wav[i:i+win_samples] for i in range(0, len(wav) - win_samples, win_samples)]

    rms_vals = [np.sqrt(np.mean(seg**2)) for seg in segments]
    rms_avg = np.mean(rms_vals)
    dynamic_thresh = threshold_ratio or max(0.02, 0.1 if rms_avg < 0.01 else 0.2)

    drop_sequence = 0
    consecutive_required = 2

    for i, rms in enumerate(rms_vals):
        if i < 3:
            continue
        if rms < rms_avg * dynamic_thresh:
            drop_sequence += 1
            if drop_sequence >= consecutive_required:
                return True
        else:
            drop_sequence = 0

    return False

# ============================================================================
# PROBLEMATIC CHUNK HANDLING
# ============================================================================

def handle_problematic_chunks(wav_path, issue_type, metrics):
    """Handle chunks with audio issues - quarantine for review"""
    quarantine_dir = wav_path.parent / "quarantine"
    quarantine_dir.mkdir(exist_ok=True)

    # Move to quarantine with descriptive name
    quarantine_path = quarantine_dir / f"{wav_path.stem}_{issue_type}.wav"
    shutil.move(str(wav_path), str(quarantine_path))

    # Log for user review
    logging.warning(f"🚨 Quarantined {issue_type}: {wav_path.name} → {quarantine_path.name}")
    logging.warning(f"   Metrics: {metrics}")

    return quarantine_path

def pause_for_chunk_review(quarantine_dir):
    """Pause processing to allow manual chunk review/editing with proper workflow"""
    quarantined_files = list(quarantine_dir.glob("*.wav"))

    if not quarantined_files:
        return  # No quarantined files, continue normally

    print(f"\n⚠️ {len(quarantined_files)} chunks quarantined in: {quarantine_dir}")
    print("\nQuarantined chunks:")
    for qfile in quarantined_files:
        print(f"   📁 {qfile.name}")

    print("\n🔧 Options:")
    print("1. Continue processing (use quarantined chunks as-is)")
    print("2. Pause to manually review/edit chunks")

    while True:
        choice = input("\nEnter choice [1/2]: ").strip()
        if choice in ['1', '2']:
            break
        print("❌ Invalid choice. Please enter 1 or 2.")

    if choice == "2":
        print(f"\n🛑 Processing paused for manual review.")
        print(f"📂 Quarantined chunks are in: {quarantine_dir}")
        print("\n📝 Instructions:")
        print("   1. Edit the audio files in the quarantine folder")
        print("   2. Keep the original filenames (chunk numbering intact)")
        print("   3. Leave edited files IN the quarantine folder")
        print("   4. Press Enter below to continue processing")

        input("\n⏸️  Press Enter when you've finished editing...")

        # Verify files still exist after user editing
        edited_files = list(quarantine_dir.glob("*.wav"))
        if not edited_files:
            print("⚠️ No files found in quarantine folder after editing!")
            return

        print(f"✅ Found {len(edited_files)} edited files, continuing...")

    # Move all chunks back to main audio folder (whether edited or not)
    moved_count = 0
    for qfile in quarantine_dir.glob("*.wav"):
        # Extract original chunk name from quarantine filename - FIXED LINE:
        original_name = re.sub(r'_(clipping|corrupted|tts_hum)$', '', qfile.stem) + ".wav"
        main_path = qfile.parent.parent / original_name

        try:
            shutil.move(str(qfile), str(main_path))
            moved_count += 1
            print(f"↩️ Restored: {original_name}")
        except Exception as e:
            logging.error(f"❌ Failed to restore {qfile.name}: {e}")

    print(f"\n✅ Restored {moved_count} chunks to main audio folder")

    # Clean up empty quarantine directory
    if not any(quarantine_dir.iterdir()):
        quarantine_dir.rmdir()

    return moved_count

# ============================================================================
# AUDIO EFFECTS AND PROCESSING
# ============================================================================

def detect_end_artifact(wav_path, window_ms=100):
    """Enhanced artifact detection"""
    data, sr = sf.read(str(wav_path))
    if data.ndim > 1:
        data = data[:, 0]

    win_samples = int(window_ms / 1000 * sr)
    if len(data) < win_samples * 2:
        return False

    end = data[-win_samples:]
    middle = data[len(data)//2 : len(data)//2 + win_samples]

    rms_end = np.sqrt(np.mean(end**2))
    rms_mid = np.sqrt(np.mean(middle**2)) + 1e-10
    rms_ratio = rms_end / rms_mid

    zcr = np.mean(np.diff(np.sign(end)) != 0)

    fft = np.fft.rfft(end)
    freqs = np.fft.rfftfreq(len(end), 1/sr)
    low_band = fft[freqs < 150]
    low_energy = np.sum(np.abs(low_band)) / (np.sum(np.abs(fft)) + 1e-10)

    logging.info(f"{GREEN}[DEBUG]{RESET} Artifact metrics - {YELLOW}RMS ratio: {rms_ratio:.3f}{RESET}, "
                f"{GREEN}ZCR: {zcr:.3f}{RESET}, {CYAN}LowEnergy: {low_energy:.3f}{RESET}")

    return rms_ratio > 0.6 or zcr > 0.2 or low_energy > 0.4

def find_end_of_speech(wav_path, sr=16000):
    """Find end of speech using Silero VAD"""
    import torch
    import os

    # Set environment variables to suppress PyTorch Hub verbosity
    old_vars = {}
    suppress_vars = {
        'TORCH_HUB_VERBOSE': '0',
        'PYTHONWARNINGS': 'ignore',
        'TF_CPP_MIN_LOG_LEVEL': '3'
    }

    # Save old values and set new ones
    for key, value in suppress_vars.items():
        old_vars[key] = os.environ.get(key)
        os.environ[key] = value

    # Temporarily disable logging for this operation
    old_level = logging.getLogger().level
    logging.getLogger().setLevel(logging.ERROR)

    try:
        model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            verbose=False
        )
        (get_speech_timestamps, _, read_audio, _, _) = utils

        wav = read_audio(str(wav_path), sampling_rate=sr)
        speech_segments = get_speech_timestamps(wav, model, sampling_rate=sr)

        if not speech_segments:
            return None

        last_seg_end = speech_segments[-1]['end']
        return int(last_seg_end * 1000 / sr)

    finally:
        # Restore everything
        logging.getLogger().setLevel(old_level)
        for key, old_value in old_vars.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value

def fade_out_wav(wav_path, output_path=None, fade_ms=20):
    """Apply fade-out to audio"""
    data, sr = sf.read(str(wav_path))
    if data.ndim > 1:
        data = data[:, 0]

    fade_samples = int(sr * fade_ms / 1000)
    if len(data) < fade_samples:
        return

    debug_path = wav_path.parent / f"{wav_path.stem}_pre_fade.wav"
    sf.write(str(debug_path), data, sr)

    fade_curve = np.linspace(1.0, 0.0, fade_samples)
    data[-fade_samples:] *= fade_curve

    sf.write(str(output_path or wav_path), data, sr)

def apply_smart_fade(wav_path):
    """Apply smart fade with artifact detection"""
    eos_ms = find_end_of_speech(wav_path)

    if detect_end_artifact(wav_path):
        fade_out_wav(wav_path)

def apply_smart_fade_memory(audio_segment):
    """Apply smart fade with artifact detection - in memory version"""
    # For now, apply a gentle fade to all audio to prevent clicks
    # TODO: Add proper artifact detection for memory processing
    return audio_segment.fade_out(50)  # 50ms fade out

def smart_audio_validation_memory(audio_segment, sample_rate):
    """Enhanced audio validation in memory - returns (audio, is_quarantined)"""
    # Basic validation - can be enhanced with hum detection later
    # For now, just return the audio as-is
    is_quarantined = False
    
    # Could add memory-based hum detection here
    # is_quarantined = detect_hum_memory(audio_segment, sample_rate)
    
    return audio_segment, is_quarantined

def add_contextual_silence_memory(audio_segment, boundary_type):
    """Add appropriate silence based on content boundary type - in memory"""
    from pydub import AudioSegment
    from config.config import (
        SILENCE_CHAPTER_START, SILENCE_CHAPTER_END, SILENCE_SECTION_BREAK, SILENCE_PARAGRAPH_END,
        SILENCE_COMMA, SILENCE_SEMICOLON, SILENCE_COLON, SILENCE_PERIOD, SILENCE_QUESTION_MARK,
        SILENCE_EXCLAMATION, SILENCE_DASH, SILENCE_ELLIPSIS, SILENCE_QUOTE_END
    )
    
    silence_durations = {
        # Structural boundaries
        "chapter_start": SILENCE_CHAPTER_START,
        "chapter_end": SILENCE_CHAPTER_END,
        "section_break": SILENCE_SECTION_BREAK,
        "paragraph_end": SILENCE_PARAGRAPH_END,
        # Punctuation boundaries
        "comma": SILENCE_COMMA,
        "semicolon": SILENCE_SEMICOLON,
        "colon": SILENCE_COLON,
        "period": SILENCE_PERIOD,
        "question_mark": SILENCE_QUESTION_MARK,
        "exclamation": SILENCE_EXCLAMATION,
        "dash": SILENCE_DASH,
        "ellipsis": SILENCE_ELLIPSIS,
        "quote_end": SILENCE_QUOTE_END,
    }
    
    if boundary_type in silence_durations:
        duration = silence_durations[boundary_type]
        silence_segment = AudioSegment.silent(duration=duration)
        return audio_segment + silence_segment
    
    return audio_segment

def smart_fade_out(wav_path, silence_thresh_db=-40, min_silence_len=300):
    """Smart fade-out for natural audio endings"""
    audio = AudioSegment.from_wav(wav_path)
    tail_window_ms = 2000

    if len(audio) < tail_window_ms:
        logging.info(f"⚠️ {YELLOW}Skipping fade: {wav_path.name} too short ({len(audio)}ms < {tail_window_ms}ms){RESET}")
        return

    tail = audio[-tail_window_ms:]
    silent_ranges = silence.detect_silence(tail, min_silence_len=min_silence_len, silence_thresh=silence_thresh_db)

    min_tail_energy = max(tail.get_array_of_samples())
    if not silent_ranges or min_tail_energy > audio.max_possible_amplitude * 0.1:
        logging.info(f"✅ {GREEN}No fade needed for {wav_path.name} (no valid trailing silence){RESET}")
        return

    fade_start_ms = silent_ranges[0][0]
    fade_length_ms = tail_window_ms - fade_start_ms

    if fade_length_ms < 100:
        logging.info(f"✅ {GREEN}No fade needed for {wav_path.name} (fade too short: {fade_length_ms}ms){RESET}")
        return

    fade_start_point = silent_ranges[0][0]
    logging.info(f"⚠️ {RED}Fading tail of {wav_path.name} from {fade_start_point}ms to end{RESET}")
    faded = audio[:fade_start_point] + audio[fade_start_point:].fade_out(duration=fade_length_ms)
    faded.export(wav_path, format="wav")

# ============================================================================
# AUDIO TRIMMING
# ============================================================================

def trim_audio_endpoint(audio_segment, threshold=None, buffer_ms=None):
    """
    Trim audio to the detected end of speech using RMS energy analysis.
    
    Args:
        audio_segment: pydub AudioSegment object
        threshold: RMS threshold for speech detection (from config if None)
        buffer_ms: Buffer to add after detected endpoint (from config if None)
    
    Returns:
        Trimmed AudioSegment
    """
    if threshold is None:
        threshold = SPEECH_ENDPOINT_THRESHOLD
    if buffer_ms is None:
        buffer_ms = TRIMMING_BUFFER_MS
    
    # Convert to numpy array for analysis
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)
    
    # Normalize samples
    samples = samples.astype(np.float32) / audio_segment.max_possible_amplitude
    
    # Calculate RMS in sliding windows (50ms windows)
    window_size = int(0.05 * audio_segment.frame_rate)  # 50ms
    rms_values = []
    
    for i in range(0, len(samples) - window_size, window_size // 2):
        window = samples[i:i + window_size]
        rms = np.sqrt(np.mean(window ** 2))
        rms_values.append(rms)
    
    # Find actual end of speech using energy decay detection
    speech_end_idx = 0  # Default to beginning if no speech found
    
    # Look for a significant and sustained drop in energy
    # Scan backwards to find where energy consistently stays above a higher threshold
    strong_speech_threshold = threshold * 3  # 3x threshold for "real" speech
    
    for i in range(len(rms_values) - 1, -1, -1):
        if rms_values[i] > strong_speech_threshold:
            # Found strong speech, check if it's sustained
            # Look forward to see if energy drops and stays low
            sustained_speech = True
            windows_ahead = min(10, len(rms_values) - i)  # Look ahead up to 10 windows (250ms)
            
            # Check if most of the next windows have reasonable speech levels
            speech_count = 0
            for j in range(i, min(i + windows_ahead, len(rms_values))):
                if rms_values[j] > threshold:
                    speech_count += 1
            
            # If this looks like the end of sustained speech content
            if speech_count >= max(1, windows_ahead * 0.3):  # At least 30% speech in next windows
                speech_end_idx = i
                break
    
    # If no strong speech found, fall back to simple threshold method but be conservative
    if speech_end_idx == 0:
        for i in range(len(rms_values) - 1, -1, -1):
            if rms_values[i] > threshold * 2:  # Use 2x threshold for fallback
                speech_end_idx = i
                break
    
    # Convert back to milliseconds and add buffer
    # Convert window index to sample position, then to milliseconds
    sample_position = speech_end_idx * (window_size // 2)
    speech_end_ms = int(sample_position * 1000 / audio_segment.frame_rate)
    trim_point_ms = min(speech_end_ms + buffer_ms, len(audio_segment))
    
    return audio_segment[:trim_point_ms]

def process_audio_with_trimming_and_silence(audio_segment, boundary_type, enable_trimming=None):
    """
    Complete audio processing: trim to speech endpoint + add punctuation-based silence.
    
    Args:
        audio_segment: pydub AudioSegment object
        boundary_type: Boundary type from text processing
        enable_trimming: Whether to trim audio (from config if None)
    
    Returns:
        Processed AudioSegment with trimming and appropriate silence
    """
    if enable_trimming is None:
        enable_trimming = ENABLE_AUDIO_TRIMMING
    
    processed_audio = audio_segment
    
    # Step 1: Trim to speech endpoint if enabled
    if enable_trimming:
        processed_audio = trim_audio_endpoint(processed_audio)
    
    # Step 2: Add punctuation-appropriate silence
    processed_audio = add_contextual_silence_memory(processed_audio, boundary_type)
    
    return processed_audio

# ============================================================================
# SILENCE AND CONTEXTUAL AUDIO
# ============================================================================

def add_contextual_silence(wav_path, boundary_type):
    """Add appropriate silence based on content boundary type"""
    silence_durations = {
        # Structural boundaries
        "chapter_start": SILENCE_CHAPTER_START,
        "chapter_end": SILENCE_CHAPTER_END,
        "section_break": SILENCE_SECTION_BREAK,
        "paragraph_end": SILENCE_PARAGRAPH_END,
        # Punctuation boundaries
        "comma": SILENCE_COMMA,
        "semicolon": SILENCE_SEMICOLON,
        "colon": SILENCE_COLON,
        "period": SILENCE_PERIOD,
        "question_mark": SILENCE_QUESTION_MARK,
        "exclamation": SILENCE_EXCLAMATION,
        "dash": SILENCE_DASH,
        "ellipsis": SILENCE_ELLIPSIS,
        "quote_end": SILENCE_QUOTE_END,
    }

    if boundary_type in silence_durations:
        duration = silence_durations[boundary_type]
        audio = AudioSegment.from_wav(wav_path)
        silence_segment = AudioSegment.silent(duration=duration)
        extended_audio = audio + silence_segment
        extended_audio.export(wav_path, format="wav")

        logging.info(f"🔇 Added {duration}ms silence for {boundary_type}: {wav_path.name}")

def add_chunk_end_silence(wav_path):
    """Add configurable silence to end of chunk if enabled"""
    if not ENABLE_CHUNK_END_SILENCE or CHUNK_END_SILENCE_MS <= 0:
        return

    try:
        audio = AudioSegment.from_wav(wav_path)
        silence_segment = AudioSegment.silent(duration=CHUNK_END_SILENCE_MS)
        audio_with_silence = audio + silence_segment
        audio_with_silence.export(wav_path, format="wav")
        logging.info(f"➕ Added {CHUNK_END_SILENCE_MS}ms end silence to {wav_path.name}")
    except Exception as e:
        logging.warning(f"⚠️ Failed to add end silence to {wav_path.name}: {e}")

# ============================================================================
# AUDIO UTILITY FUNCTIONS
# ============================================================================

def get_wav_duration(wav_path):
    """Get WAV file duration"""
    import wave
    with wave.open(str(wav_path), 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

def get_chunk_audio_duration(wav_path):
    """Get actual audio duration from WAV file"""
    try:
        data, sr = sf.read(str(wav_path))
        return len(data) / sr
    except:
        # Fallback to wave module
        return get_wav_duration(wav_path)
