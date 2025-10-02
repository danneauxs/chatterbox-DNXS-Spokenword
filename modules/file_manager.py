"""
ChatterboxTTS File Management & Media Processing Module
======================================================

OVERVIEW:
This module handles all file system operations, media format conversions, and
metadata management for ChatterboxTTS. It manages the complex directory structure
for audiobook production and handles conversion to final distribution formats.

MAIN COMPONENTS:
1. DIRECTORY MANAGEMENT: Creates and maintains audiobook processing directories
2. AUDIO DISCOVERY: Locates and validates audio files across directory structures
3. M4B CONVERSION: Converts WAV chunks to M4B audiobook format using FFmpeg
4. METADATA HANDLING: Adds cover art, chapters, and book information to audiobooks
5. FILE VALIDATION: Ensures audio file compatibility and format requirements
6. VOICE SAMPLE MANAGEMENT: Handles voice sample discovery and validation

KEY OPERATIONS:
- Directory structure setup for new audiobooks
- Audio chunk discovery and organization
- WAV to M4B conversion with chapter markers
- Cover art integration and metadata embedding
- File compatibility checking (24kHz requirement for voice samples)
- Final audiobook packaging and organization

DIRECTORY STRUCTURE MANAGED:
```
Audiobook/[book_name]/
├── TTS/
│   ├── text_chunks/     # Individual text chunk files
│   └── audio_chunks/    # Generated WAV audio chunks
├── [book_name].m4b      # Final audiobook file
├── processing.log       # Processing logs
└── metadata files       # Cover art, chapter info
```

TECHNICAL FEATURES:
- FFmpeg integration for media processing
- Automatic cover art detection and integration
- Chapter marker generation from chunk structure
- Metadata preservation across format conversions
- File system safety with validation and error handling
- Cross-platform file operations (Windows/Linux/Mac)

PERFORMANCE CONSIDERATIONS:
Handles large audio files efficiently with streaming processing
and manages disk space through temporary file cleanup.
"""

import subprocess
import soundfile as sf
import os
import re
import time
import logging
from pathlib import Path
from config.config import *

# FFmpeg availability check
def is_ffmpeg_available():
    """Check if FFmpeg is available in system PATH"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def ffmpeg_error_message():
    """Standard error message for missing FFmpeg"""
    return ("FFmpeg is not installed or not found in system PATH.\n"
            "M4B audiobook creation requires FFmpeg.\n\n"
            "To install FFmpeg:\n"
            "• Windows: Download from https://ffmpeg.org/download.html\n"
            "• Or re-run the installation script\n\n"
            "WAV audio generation will continue to work normally.")

# ============================================================================
# VOICE SAMPLE MANAGEMENT
# ============================================================================

def list_voice_samples():
    """List available voice samples"""
    return sorted(VOICE_SAMPLES_DIR.glob("*.wav"), key=lambda x: x.stem.lower())

def ensure_voice_sample_compatibility(input_path, output_dir=None):
    """Ensure voice sample is compatible with TTS (24kHz mono)"""
    input_path = str(input_path)
    ext = os.path.splitext(input_path)[1].lower()
    basename = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = output_dir or os.path.dirname(input_path)
    output_path = os.path.join(output_dir, basename + "_ttsready.wav")

    try:
        info = sf.info(input_path)
        if (ext == '.wav' and info.samplerate == 24000 and info.channels == 1):
            return input_path
    except Exception:
        pass

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "24000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

# ============================================================================
# FFMPEG OPERATIONS
# ============================================================================

def run_ffmpeg(cmd):
    """Run FFmpeg command with error handling"""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg command failed: {' '.join(cmd)}")
        logging.error(f"Exit code: {e.returncode}")
        logging.error(f"stdout: {e.stdout}")
        logging.error(f"stderr: {e.stderr}")
        
        # Common FFmpeg error solutions
        if e.returncode == 254:
            logging.error("FFmpeg exit code 254 - Usually indicates file I/O or format issues")
            logging.error("Possible causes:")
            logging.error("- Input files don't exist or are corrupted")
            logging.error("- Output directory doesn't exist or lacks write permissions")
            logging.error("- Concat file format issues")
            
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}: {e.stderr}")

# ============================================================================
# M4B CONVERSION WITH NORMALIZATION
# ============================================================================

def convert_to_m4b_with_peak_normalization(wav_path, temp_m4b_path, target_db=-3.0, custom_speed=None, custom_sample_rate=None):
    """Convert WAV to M4B with peak normalization"""
    if not is_ffmpeg_available():
        error_msg = ffmpeg_error_message()
        print(f"❌ Cannot convert to M4B: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    print("🚀 Converting to m4b with peak normalization...")

    # Build audio filter chain
    speed_to_use = custom_speed if custom_speed is not None else ATEMPO_SPEED
    sample_rate_to_use = custom_sample_rate if custom_sample_rate is not None else M4B_SAMPLE_RATE
    audio_filters = [f"loudnorm=I=-16:TP={target_db}:LRA=11"]
    if speed_to_use != 1.0:
        audio_filters.append(f"atempo={speed_to_use}")
    
    print(f"🚀 Converting to m4b with peak normalization and speed {speed_to_use}x...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-af", ",".join(audio_filters),
        "-ar", str(M4B_SAMPLE_RATE),
        "-c:a", "aac",
        str(temp_m4b_path)
    ]

    start_time = time.time()
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    audio_secs = 0.0
    for line in process.stderr:
        match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if match:
            h, m, s, ms = map(int, match.groups())
            audio_secs = h * 3600 + m * 60 + s + ms / 100
            elapsed = time.time() - start_time
            factor = audio_secs / elapsed if elapsed > 0 else 0.0
            print(f"📼 FFmpeg (normalizing): {match.group(0)} | {factor:.2f}x realtime", end='\r')

    process.wait()
    print("\n✅ Conversion with normalization complete.")

def convert_to_m4b_with_loudness_normalization(wav_path, temp_m4b_path, custom_speed=None, custom_sample_rate=None):
    """Convert WAV to M4B with two-pass loudness normalization"""
    if not is_ffmpeg_available():
        error_msg = ffmpeg_error_message()
        print(f"❌ Cannot convert to M4B: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    import json

    print("🚀 Converting to m4b with loudness normalization...")

    # Step 1: Analyze audio loudness
    print("📊 Analyzing audio loudness...")
    analyze_cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-"
    ]

    result = subprocess.run(analyze_cmd, capture_output=True, text=True)

    # Extract loudness measurements from stderr
    loudness_data = None
    for line in result.stderr.split('\n'):
        if line.strip().startswith('{'):
            try:
                loudness_data = json.loads(line.strip())
                break
            except:
                continue

    if not loudness_data:
        print("⚠️ Could not analyze loudness, falling back to single-pass...")
        return convert_to_m4b_with_peak_normalization(wav_path, temp_m4b_path)

    # Step 2: Apply normalization with measured values
    print("🔧 Applying normalization...")
    
    # Build audio filter chain  
    speed_to_use = custom_speed if custom_speed is not None else ATEMPO_SPEED
    sample_rate_to_use = custom_sample_rate if custom_sample_rate is not None else M4B_SAMPLE_RATE
    audio_filters = [f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={loudness_data['input_i']}:measured_LRA={loudness_data['input_lra']}:measured_TP={loudness_data['input_tp']}:measured_thresh={loudness_data['input_thresh']}:offset={loudness_data['target_offset']}:linear=true:print_format=summary"]
    if speed_to_use != 1.0:
        audio_filters.append(f"atempo={speed_to_use}")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-af", ",".join(audio_filters),
        "-ar", str(M4B_SAMPLE_RATE),
        "-c:a", "aac",
        str(temp_m4b_path)
    ]

    start_time = time.time()
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    audio_secs = 0.0
    for line in process.stderr:
        match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if match:
            h, m, s, ms = map(int, match.groups())
            audio_secs = h * 3600 + m * 60 + s + ms / 100
            elapsed = time.time() - start_time
            factor = audio_secs / elapsed if elapsed > 0 else 0.0
            print(f"📼 FFmpeg (normalizing): {match.group(0)} | {factor:.2f}x realtime", end='\r')

    process.wait()
    print("\n✅ Two-pass normalization complete.")

def convert_to_m4b_with_simple_normalization(wav_path, temp_m4b_path, target_db=-6.0, custom_speed=None, custom_sample_rate=None):
    """Convert WAV to M4B with simple peak normalization"""
    if not is_ffmpeg_available():
        error_msg = ffmpeg_error_message()
        print(f"❌ Cannot convert to M4B: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    print("🚀 Converting to m4b with simple normalization...")

    # Build audio filter chain
    speed_to_use = custom_speed if custom_speed is not None else ATEMPO_SPEED
    sample_rate_to_use = custom_sample_rate if custom_sample_rate is not None else M4B_SAMPLE_RATE
    audio_filters = [f"volume={target_db}dB"]
    if speed_to_use != 1.0:
        audio_filters.append(f"atempo={speed_to_use}")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-af", ",".join(audio_filters),
        "-ar", str(M4B_SAMPLE_RATE),
        "-c:a", "aac",
        str(temp_m4b_path)
    ]

    start_time = time.time()
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    audio_secs = 0.0
    for line in process.stderr:
        match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if match:
            h, m, s, ms = map(int, match.groups())
            audio_secs = h * 3600 + m * 60 + s + ms / 100
            elapsed = time.time() - start_time
            factor = audio_secs / elapsed if elapsed > 0 else 0.0
            print(f"📼 FFmpeg (normalizing): {match.group(0)} | {factor:.2f}x realtime", end='\r')

    process.wait()
    print("\n✅ Simple normalization complete.")

def convert_to_m4b(wav_path, temp_m4b_path, custom_speed=None, custom_sample_rate=None):
    """Convert WAV to M4B with configurable normalization and optional custom speed/sample rate"""
    if not is_ffmpeg_available():
        error_msg = ffmpeg_error_message()
        print(f"❌ Cannot convert to M4B: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    # Determine speed to use (custom speed overrides config)
    speed_to_use = custom_speed if custom_speed is not None else ATEMPO_SPEED
    # Determine sample rate to use (custom sample rate overrides config)
    sample_rate_to_use = custom_sample_rate if custom_sample_rate is not None else M4B_SAMPLE_RATE
    
    if not ENABLE_NORMALIZATION or NORMALIZATION_TYPE == "none":
        # Original function without normalization
        print(f"🚀 Converting to m4b with speed {speed_to_use}x...")

        # Build audio filter for atempo if needed
        audio_filter = []
        if speed_to_use != 1.0:
            audio_filter = ["-filter:a", f"atempo={speed_to_use}"]

        cmd = [
            "ffmpeg", "-y",
            "-i", str(wav_path)
        ] + audio_filter + [
            "-ar", str(sample_rate_to_use),
            "-c:a", "aac",
            str(temp_m4b_path)
        ]

    elif NORMALIZATION_TYPE == "loudness":
        # EBU R128 loudness normalization (recommended for audiobooks)
        return convert_to_m4b_with_loudness_normalization(wav_path, temp_m4b_path, custom_speed, custom_sample_rate)

    elif NORMALIZATION_TYPE == "peak":
        # Peak normalization
        return convert_to_m4b_with_peak_normalization(wav_path, temp_m4b_path, TARGET_PEAK_DB, custom_speed, custom_sample_rate)

    elif NORMALIZATION_TYPE == "simple":
        # Simple volume adjustment
        return convert_to_m4b_with_simple_normalization(wav_path, temp_m4b_path, TARGET_PEAK_DB, custom_speed, custom_sample_rate)

    else:
        # Fallback to no normalization
        # Build audio filter for atempo if needed
        audio_filter = []
        if speed_to_use != 1.0:
            audio_filter = ["-filter:a", f"atempo={speed_to_use}"]

        cmd = [
            "ffmpeg", "-y",
            "-i", str(wav_path)
        ] + audio_filter + [
            "-ar", str(sample_rate_to_use),
            "-c:a", "aac",
            str(temp_m4b_path)
        ]

    # Run the conversion (if not handled by specialized functions above)
    start_time = time.time()
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    audio_secs = 0.0
    for line in process.stderr:
        match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
        if match:
            h, m, s, ms = map(int, match.groups())
            audio_secs = h * 3600 + m * 60 + s + ms / 100
            elapsed = time.time() - start_time
            factor = audio_secs / elapsed if elapsed > 0 else 0.0
            print(f"📼 FFmpeg: {match.group(0)} | {factor:.2f}x realtime", end='\r')

    process.wait()
    print("\n✅ Conversion complete.")

def add_metadata_to_m4b(temp_m4b_path, final_m4b_path, cover_path=None, nfo_path=None):
    """Add metadata and cover to M4B"""
    if not is_ffmpeg_available():
        error_msg = ffmpeg_error_message()
        print(f"❌ Cannot add metadata to M4B: {error_msg}")
        raise FileNotFoundError(error_msg)
        
    cmd = ["ffmpeg", "-y", "-i", str(temp_m4b_path)]

    if cover_path and cover_path.exists():
        cmd.extend(["-i", str(cover_path), "-map", "0", "-map", "1", "-c", "copy", "-disposition:v:0", "attached_pic"])
    else:
        cmd.extend(["-map", "0", "-c", "copy"])

    if nfo_path and nfo_path.exists():
        with open(nfo_path, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, val = line.strip().split(':', 1)
                    cmd.extend(["-metadata", f"{key.strip()}={val.strip()}"])

    cmd.append(str(final_m4b_path))
    run_ffmpeg(cmd)
    temp_m4b_path.unlink(missing_ok=True)

# ============================================================================
# FILE UTILITIES
# ============================================================================

def chunk_sort_key(f):
    """Extracts the chunk number for natural sorting"""
    m = re.match(r"chunk_(\d+)\.wav", f.name)
    return int(m.group(1)) if m else 0

def create_concat_file(chunk_paths, output_path):
    """Create FFmpeg concat file for audio chunks"""
    with open(output_path, 'w') as f:
        for p in chunk_paths:
            # Use absolute path and escape spaces and special chars for FFmpeg concat
            path_str = str(p.resolve())
            # Escape spaces, single quotes, and backslashes for FFmpeg concat format
            escaped_path = path_str.replace('\\', '\\\\').replace(' ', '\\ ').replace("'", "\\'")
            f.write(f'file {escaped_path}\n')

    logging.info(f"concat.txt written with {len(chunk_paths)} chunks.")
    return output_path

def cleanup_temp_files(directory, patterns):
    """Clean up temporary files matching patterns"""
    files_cleaned = 0
    for pattern in patterns:
        for temp_file in directory.glob(pattern):
            temp_file.unlink(missing_ok=True)
            files_cleaned += 1

    return files_cleaned

# ============================================================================
# DIRECTORY MANAGEMENT
# ============================================================================

def sanitize_filename(name):
    """Sanitize filename for cross-platform compatibility"""
    import re
    # Replace problematic characters with safe alternatives
    # Parentheses, brackets, quotes, and other special chars
    sanitized = re.sub(r'[()[\]{}\'"`<>|?*]', '_', name)
    # Replace multiple consecutive underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized

def setup_book_directories(book_dir):
    """Set up directory structure for book processing"""
    original_basename = book_dir.name
    # Sanitize the basename for filesystem compatibility
    basename = sanitize_filename(original_basename)
    
    # Log if sanitization changed the name
    if basename != original_basename:
        logging.info(f"Sanitized directory name: '{original_basename}' -> '{basename}'")
    
    output_root = AUDIOBOOK_ROOT / basename
    tts_dir = output_root / "TTS"
    text_chunks_dir = tts_dir / "text_chunks"
    audio_chunks_dir = tts_dir / "audio_chunks"

    # Create directories
    for d in [output_root, tts_dir, text_chunks_dir, audio_chunks_dir]:
        d.mkdir(parents=True, exist_ok=True)

    return output_root, tts_dir, text_chunks_dir, audio_chunks_dir

def find_book_files(book_dir):
    """Find text files, cover, and metadata for a book"""
    text_files = sorted(book_dir.glob("*.txt"))
    nfo_file = book_dir / "book.nfo"
    cover_jpg = book_dir / "cover.jpg"
    cover_png = book_dir / "cover.png"
    cover_file = cover_jpg if cover_jpg.exists() else cover_png if cover_png.exists() else None

    return {
        'text': text_files[0] if text_files else None,
        'cover': cover_file,
        'nfo': nfo_file if nfo_file.exists() else None
    }

# ============================================================================
# AUDIO FILE OPERATIONS
# ============================================================================

def combine_audio_chunks(chunk_paths, output_path):
    """Combine audio chunks into single file using FFmpeg"""
    logging.info(f"Combining {len(chunk_paths)} audio chunks into {output_path}")
    
    # Validate input files exist
    missing_files = []
    for chunk_path in chunk_paths:
        if not chunk_path.exists():
            missing_files.append(str(chunk_path))
    
    if missing_files:
        error_msg = f"Missing chunk files: {missing_files[:5]}"  # Show first 5
        if len(missing_files) > 5:
            error_msg += f" ... and {len(missing_files)-5} more"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create concat file
    concat_list_path = output_path.parent / "concat.txt"
    create_concat_file(chunk_paths, concat_list_path)
    
    # Verify concat file was created
    if not concat_list_path.exists():
        raise FileNotFoundError(f"Failed to create concat file: {concat_list_path}")
    
    logging.info(f"Created concat file: {concat_list_path}")
    
    try:
        run_ffmpeg([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path.resolve()),
            "-c", "copy", str(output_path.resolve())
        ])
        
        # Verify output file was created
        if not output_path.exists():
            raise RuntimeError(f"FFmpeg completed but output file not found: {output_path}")
        
        logging.info(f"Successfully combined audio chunks: {output_path}")
        
    except Exception as e:
        # Log concat file contents for debugging
        try:
            with open(concat_list_path, 'r') as f:
                concat_contents = f.read()
            logging.error(f"Concat file contents:\n{concat_contents}")
        except:
            logging.error("Could not read concat file for debugging")
        raise

    return output_path

def get_audio_files_in_directory(directory, pattern="chunk_*.wav"):
    """Get sorted list of audio files matching pattern"""
    chunk_paths = sorted([f for f in directory.glob(pattern)
                         if re.fullmatch(r'chunk_\d{3,}\.wav', f.name)],
                        key=chunk_sort_key)
    return chunk_paths

# ============================================================================
# VALIDATION AND VERIFICATION
# ============================================================================

def verify_audio_file(wav_path):
    """Verify audio file is valid and readable"""
    try:
        info = sf.info(str(wav_path))
        return info.frames > 0 and info.samplerate > 0
    except Exception as e:
        logging.error(f"Invalid audio file {wav_path}: {e}")
        return False

def verify_chunk_completeness(audio_chunks_dir, expected_count):
    """Verify all expected chunks exist and are valid"""
    missing_chunks = []
    invalid_chunks = []

    for i in range(1, expected_count + 1):
        chunk_path = audio_chunks_dir / f"chunk_{i:05}.wav"

        if not chunk_path.exists():
            missing_chunks.append(i)
        elif not verify_audio_file(chunk_path):
            invalid_chunks.append(i)

    return missing_chunks, invalid_chunks

# ============================================================================
# EXPORT AND IMPORT FUNCTIONS
# ============================================================================

def export_processing_log(output_dir, processing_info):
    """Export comprehensive processing log"""
    log_path = output_dir / "processing_complete.log"

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("GenTTS Processing Complete\n")
        f.write("=" * 50 + "\n\n")

        for key, value in processing_info.items():
            f.write(f"{key}: {value}\n")

    return log_path

def save_chunk_info(text_chunks_dir, chunks_info):
    """Save chunk information for debugging/resume"""
    info_path = text_chunks_dir / "chunks_info.json"

    import json
    
    # Apply batch-binning if enabled
    if ENABLE_BATCH_BINNING:
        chunks_info = apply_batch_binning(chunks_info)

    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_info, f, indent=2, ensure_ascii=False)

    return info_path

def apply_batch_binning(chunks_info):
    """Round VADER parameters to nearest bin for better microbatching"""
    print(f"📦 BATCH-BINNING: Processing {len(chunks_info)} chunks with precision {BATCH_BIN_PRECISION}")
    binned_chunks = []
    param_changes = {'exaggeration': [], 'cfg_weight': [], 'temperature': []}
    
    for chunk in chunks_info:
        # Create a copy of the chunk to avoid modifying the original
        binned_chunk = chunk.copy()
        
        # Apply binning to tts_params if they exist
        if 'tts_params' in binned_chunk and binned_chunk['tts_params']:
            tts_params = binned_chunk['tts_params'].copy()
            
            # Round key VADER-influenced parameters to nearest BATCH_BIN_PRECISION
            for param in ['exaggeration', 'cfg_weight', 'temperature']:
                if param in tts_params:
                    original_value = tts_params[param]
                    # Round to nearest BATCH_BIN_PRECISION (e.g., 0.05)
                    # Use proper rounding: divide by precision, round, multiply back
                    steps = round(original_value / BATCH_BIN_PRECISION)
                    binned_value = steps * BATCH_BIN_PRECISION
                    binned_final = round(binned_value, 3)  # Keep 3 decimal places for precision
                    
                    # Track changes for measurement
                    if abs(original_value - binned_final) > 0.001:  # Significant change
                        param_changes[param].append((original_value, binned_final))
                    
                    tts_params[param] = binned_final
            
            binned_chunk['tts_params'] = tts_params
        
        binned_chunks.append(binned_chunk)
    
    # Report batch-binning effectiveness
    total_changes = sum(len(changes) for changes in param_changes.values())
    if total_changes > 0:
        print(f"📦 BATCH-BINNING RESULTS:")
        for param, changes in param_changes.items():
            if changes:
                unique_original = len(set(orig for orig, _ in changes))
                unique_binned = len(set(binned for _, binned in changes))
                print(f"   {param}: {len(changes)} chunks changed, {unique_original}→{unique_binned} unique values")
        print(f"📦 Total parameter changes: {total_changes}")
        
        # Calculate batching potential
        original_combinations = set()
        binned_combinations = set()
        for chunk in chunks_info:
            if 'tts_params' in chunk and chunk['tts_params']:
                tp = chunk['tts_params']
                orig_combo = (tp.get('exaggeration', 0.5), tp.get('cfg_weight', 0.5), tp.get('temperature', 0.85))
                original_combinations.add(orig_combo)
        
        for chunk in binned_chunks:
            if 'tts_params' in chunk and chunk['tts_params']:
                tp = chunk['tts_params']
                binned_combo = (tp.get('exaggeration', 0.5), tp.get('cfg_weight', 0.5), tp.get('temperature', 0.85))
                binned_combinations.add(binned_combo)
        
        print(f"📦 MICRO-BATCH IMPROVEMENT: {len(original_combinations)}→{len(binned_combinations)} parameter combinations")
        improvement = (len(original_combinations) - len(binned_combinations)) / len(original_combinations) * 100 if original_combinations else 0
        print(f"📦 Batch consolidation: {improvement:.1f}% reduction in unique parameter sets")
    else:
        print("📦 BATCH-BINNING: No parameter changes needed - values already binned")
    
    return binned_chunks

def load_chunk_info(text_chunks_dir):
    """Load chunk information if available"""
    info_path = text_chunks_dir / "chunks_info.json"

    if not info_path.exists():
        return None

    import json
    try:
        with open(info_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"Could not load chunk info: {e}")
        return None
