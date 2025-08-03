#!/usr/bin/env python3
"""
Gradio Tab 1: Convert Book
Exact replica of PyQt5 GUI Tab 1 functionality
"""

import gradio as gr
import os
import sys
import threading
import subprocess
import tempfile
import json
import warnings
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Suppress CUDA deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*torch.backends.cuda.sdp_kernel.*")
warnings.filterwarnings("ignore", category=FutureWarning, message=".*sdp_kernel.*")

# Import ChatterboxTTS modules and ensure all config variables are available
# First set defaults, then try to import from config
DEFAULT_EXAGGERATION = 0.4
DEFAULT_CFG_WEIGHT = 0.5
DEFAULT_TEMPERATURE = 0.9
TTS_PARAM_MIN_EXAGGERATION = 0.0
TTS_PARAM_MAX_EXAGGERATION = 2.0
TTS_PARAM_MIN_CFG_WEIGHT = 0.0
TTS_PARAM_MAX_CFG_WEIGHT = 1.0
TTS_PARAM_MIN_TEMPERATURE = 0.0
TTS_PARAM_MAX_TEMPERATURE = 5.0
ENABLE_REGENERATION_LOOP = True
MAX_REGENERATION_ATTEMPTS = 3
QUALITY_THRESHOLD = 0.7
ENABLE_SENTIMENT_SMOOTHING = True
SENTIMENT_SMOOTHING_WINDOW = 3
SENTIMENT_SMOOTHING_METHOD = "rolling"
ENABLE_MFCC_VALIDATION = False
ENABLE_OUTPUT_VALIDATION = False
SPECTRAL_ANOMALY_THRESHOLD = 0.8
OUTPUT_VALIDATION_THRESHOLD = 0.85

# Try to import config and override defaults if available
try:
    from config.config import *
    CONFIG_AVAILABLE = True
    print("✅ Config loaded successfully")
except ImportError:
    print("⚠️  Config not available - using defaults")
    CONFIG_AVAILABLE = False

# Import the actual conversion functions from GUI
try:
    # We need to import the actual conversion logic
    import importlib.util
    gui_spec = importlib.util.spec_from_file_location("chatterbox_gui", "chatterbox_gui.py")
    gui_module = importlib.util.module_from_spec(gui_spec)
    # We'll access the GUI's conversion methods
    GUI_AVAILABLE = True
except Exception as e:
    print(f"⚠️  GUI module not available: {e}")
    GUI_AVAILABLE = False

# Global state for conversion with enhanced stats
conversion_state = {
    'running': False,
    'progress': 0,
    'status': 'Ready',
    'thread': None,
    'realtime_factor': '--',
    'vram_usage': '-- GB',
    'current_chunk': '--',
    'eta': '--',
    'elapsed': '--'
}

def parse_progress_stats(output_line):
    """Parse progress statistics from TTS engine output"""
    # Look for progress pattern: "🌀 Chunk 2/13 | ⏱ Elapsed: 0:01:31 | ETA: 0:09:54 | Remaining: 0:08:23 | Realtime: 0.11x | VRAM: 3.3GB"
    progress_pattern = r'🌀 Chunk (\d+)/(\d+).*?Realtime: ([\d.]+)x.*?VRAM: ([\d.]+)GB'
    match = re.search(progress_pattern, output_line)

    if match:
        current_chunk = int(match.group(1))
        total_chunks = int(match.group(2))
        realtime_factor = f"{match.group(3)}x"
        vram_usage = f"{match.group(4)} GB"

        # Update global state
        conversion_state['current_chunk'] = f"{current_chunk}/{total_chunks}"
        conversion_state['realtime_factor'] = realtime_factor
        conversion_state['vram_usage'] = vram_usage
        conversion_state['progress'] = int((current_chunk / total_chunks) * 100) if total_chunks > 0 else 0

        print(f"📊 Stats Updated: Chunk {current_chunk}/{total_chunks}, {realtime_factor}, {vram_usage}")
        return True
    else:
        # Try alternative patterns in case the format is different
        alt_pattern = r'Chunk (\d+)/(\d+).*?Realtime: ([\d.]+)x.*?VRAM: ([\d.]+)GB'
        alt_match = re.search(alt_pattern, output_line)
        if alt_match:
            current_chunk = int(alt_match.group(1))
            total_chunks = int(alt_match.group(2))
            realtime_factor = f"{alt_match.group(3)}x"
            vram_usage = f"{alt_match.group(4)} GB"

            conversion_state['current_chunk'] = f"{current_chunk}/{total_chunks}"
            conversion_state['realtime_factor'] = realtime_factor
            conversion_state['vram_usage'] = vram_usage
            conversion_state['progress'] = int((current_chunk / total_chunks) * 100) if total_chunks > 0 else 0

            print(f"📊 Stats Updated: Chunk {current_chunk}/{total_chunks}, {realtime_factor}, {vram_usage}")
            return True

    return False

def get_progress_stats():
    """Get current progress statistics for UI update"""
    return (
        conversion_state['realtime_factor'],
        conversion_state['vram_usage'],
        conversion_state['current_chunk'],
        conversion_state['progress']
    )

def get_book_folders():
    """Get available book folders from Text_Input directory"""
    text_input_dir = Path("Text_Input")
    if not text_input_dir.exists():
        return []

    folders = []
    for item in text_input_dir.iterdir():
        if item.is_dir():
            folders.append(item.name)  # Show only folder name, not full path

    return sorted(folders)

def get_text_files_in_folder(folder_name):
    """Get text files in selected book folder"""
    if not folder_name:
        return []

    # Build full path from folder name
    folder = Path("Text_Input") / folder_name
    if not folder.exists():
        return []

    text_files = []
    for file in folder.glob("*.txt"):
        text_files.append(file.name)

    return sorted(text_files)

def get_voice_samples():
    """Get available voice samples from Voice_Samples directory"""
    voice_dir = Path("Voice_Samples")
    if not voice_dir.exists():
        return []

    voices = []
    for file in voice_dir.glob("*.wav"):
        voices.append(file.name)  # Show only filename, not full path

    return sorted(voices)

def find_generated_audiobook(book_folder_path, voice_sample_path):
    """Find the generated audiobook files"""
    try:
        book_folder = Path(book_folder_path)
        voice_file = Path(voice_sample_path)
        voice_name = voice_file.stem

        # Look in Output/ directory first (final audiobooks)
        output_dir = Path("Output")
        if output_dir.exists():
            # Look for M4B files with voice name
            for m4b_file in output_dir.glob(f"*[{voice_name}]*.m4b"):
                if m4b_file.exists():
                    return str(m4b_file), "M4B audiobook"

            # Look for WAV files with voice name
            for wav_file in output_dir.glob(f"*[{voice_name}]*.wav"):
                if wav_file.exists():
                    return str(wav_file), "WAV audiobook"

        # Look in Audiobook/ directory (processing output)
        audiobook_dir = Path("Audiobook") / book_folder.name
        if audiobook_dir.exists():
            # Look for M4B files
            for m4b_file in audiobook_dir.glob(f"*[{voice_name}]*.m4b"):
                if m4b_file.exists():
                    return str(m4b_file), "M4B audiobook"

            # Look for WAV files
            for wav_file in audiobook_dir.glob(f"*[{voice_name}]*.wav"):
                if wav_file.exists():
                    return str(wav_file), "WAV audiobook"

            # Look for combined files
            for combined_file in audiobook_dir.glob("*_combined.*"):
                if combined_file.suffix in ['.wav', '.m4b', '.mp3']:
                    return str(combined_file), f"{combined_file.suffix.upper()[1:]} combined audiobook"

        return None, "No audiobook found"

    except Exception as e:
        print(f"Error finding audiobook: {e}")
        return None, f"Error: {str(e)}"

def run_book_conversion(book_path, text_file_path, voice_path, tts_params, quality_params, config_params):
    """Run the actual book conversion - Direct call to TTS engine with progress monitoring"""
    try:
        # Import the real TTS engine function directly (avoid interface.py)
        from modules.tts_engine import process_book_folder

        # Extract enable_asr from tts_params (matching GUI exactly)
        enable_asr = tts_params.get('enable_asr', False)

        print(f"🚀 Starting book conversion with GUI parameters")
        print(f"📖 Book: {book_path}")
        print(f"📄 Text file: {text_file_path}")
        print(f"🎤 Voice: {voice_path}")
        print(f"🎛️ TTS Params: {tts_params}")
        print(f"🔬 Quality Params: {quality_params}")
        print(f"⚙️ Config Params: {config_params}")

        # Set up progress callback function
        def progress_callback(current_chunk, total_chunks, realtime_factor, vram_usage):
            """Callback function to update progress from TTS engine"""
            conversion_state['current_chunk'] = f"{current_chunk}/{total_chunks}"
            conversion_state['realtime_factor'] = f"{realtime_factor}x"
            conversion_state['vram_usage'] = f"{vram_usage} GB"
            conversion_state['progress'] = int((current_chunk / total_chunks) * 100) if total_chunks > 0 else 0
            print(f"📊 Progress: {current_chunk}/{total_chunks} ({conversion_state['progress']}%) - {realtime_factor}x - {vram_usage}GB")

        # Add progress callback to config params
        config_params['progress_callback'] = progress_callback

        # Convert string paths to Path objects (required by TTS engine)
        book_dir_path = Path(book_path)
        voice_path_obj = Path(voice_path)

        # Auto-detect device with fallback to CPU
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print("✅ Using CUDA GPU for processing")
        else:
            device = "cpu"
            print("💻 Using CPU for processing (no GPU available)")
        
        # Direct call to TTS engine (function only accepts: book_dir, voice_path, tts_params, device, skip_cleanup)
        result = process_book_folder(
            book_dir=book_dir_path,
            voice_path=voice_path_obj,
            tts_params=tts_params,
            device=device,
            skip_cleanup=False
        )

        print(f"✅ Conversion completed successfully")
        return {'success': True, 'result': result}

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def regenerate_m4b_file(selected_m4b, playback_speed):
    """Regenerate M4B file with new playback speed"""
    if not selected_m4b:
        return "❌ Please select an M4B file first", None

    try:
        print(f"🔄 Regenerating M4B: {selected_m4b} at {playback_speed}x speed")

        # Import M4B regeneration tools
        from tools.combine_only import apply_playback_speed_to_m4b

        # Find the M4B file path
        audiobook_root = Path("Audiobook")
        m4b_path = None

        for book_dir in audiobook_root.iterdir():
            if book_dir.is_dir():
                for m4b_file in book_dir.glob("*.m4b"):
                    if m4b_file.name == selected_m4b:
                        m4b_path = m4b_file
                        break
                if m4b_path:
                    break

        if not m4b_path:
            return "❌ M4B file not found", None

        # Create new filename with speed suffix
        speed_suffix = f"_speed{playback_speed}x".replace(".", "p")
        new_name = m4b_path.stem + speed_suffix + ".m4b"
        output_path = m4b_path.parent / new_name

        # Apply speed change
        success = apply_playback_speed_to_m4b(str(m4b_path), str(output_path), playback_speed)

        if success:
            return f"✅ Regenerated M4B at {playback_speed}x speed: {new_name}", str(output_path)
        else:
            return "❌ Failed to regenerate M4B", None

    except Exception as e:
        print(f"❌ M4B regeneration failed: {e}")
        return f"❌ Error: {str(e)}", None

def create_convert_book_tab():
    """Create Tab 1: Convert Book with all GUI functionality"""

    with gr.Column():
        gr.Markdown("# 🚀 Convert Book")
        gr.Markdown("*Main TTS conversion functionality - matches GUI Tab 1*")

        # Main Content Layout
        with gr.Row():
            # Left Column - File Uploads
            with gr.Column(scale=2):
                gr.Markdown("### 📚 Book Selection")

                # Book text file upload only
                text_file_upload = gr.File(
                    label="📚 Upload Book Text File",
                    file_types=[".txt"],
                    file_count="single",
                    interactive=True
                )

                gr.Markdown("### 🎤 Voice Selection")

                # Single voice upload with integrated playback
                voice_file_upload = gr.File(
                    label="🎤 Upload Voice Sample",
                    file_types=[".wav", ".mp3", ".m4a"],
                    file_count="single",
                    interactive=True
                )

                # Voice sample player (becomes active after upload)
                voice_audio = gr.Audio(
                    label="Voice Sample Preview",
                    interactive=False,
                    show_download_button=False,
                    visible=False
                )

            # Right Column - All Settings
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Quick Settings")

                # VADER and ASR
                vader_enabled = gr.Checkbox(
                    label="Use VADER sentiment analysis",
                    value=True,
                    info="Adjust TTS params per chunk based on emotion"
                )

                # ASR System with intelligent model selection
                with gr.Row():
                    asr_enabled = gr.Checkbox(
                        label="🎤 Enable ASR validation",
                        value=False,
                        info="Smart quality control with automatic model selection"
                    )

                # ASR Configuration (initially hidden)
                with gr.Column(visible=False) as asr_config_group:
                    gr.Markdown("#### 🔍 ASR Configuration")

                    # System analysis display
                    system_analysis = gr.Textbox(
                        label="System Analysis",
                        value="Click 'Analyze System' to detect capabilities",
                        lines=3,
                        interactive=False
                    )

                    analyze_system_btn = gr.Button(
                        "🔍 Analyze System",
                        size="sm",
                        variant="secondary"
                    )

                    # ASR Level Selection
                    asr_level = gr.Radio(
                        label="ASR Quality Level",
                        choices=[
                            ("🟢 SAFE - Fast processing, basic accuracy", "safe"),
                            ("🟡 MODERATE - Balanced speed/accuracy (recommended)", "moderate"),
                            ("🔴 INSANE - Best accuracy, may stress system", "insane")
                        ],
                        value="moderate",
                        info="Automatically selects best models for your system"
                    )

                    # Selected models display
                    selected_models = gr.Textbox(
                        label="Selected ASR Models",
                        value="Select level to see model configuration",
                        lines=2,
                        interactive=False
                    )

                # Batch processing
                add_to_batch = gr.Checkbox(
                    label="📦 Add to batch queue",
                    value=False,
                    info="Queue for batch processing"
                )

                gr.Markdown("### 🔄 Regeneration Settings")

                regeneration_enabled = gr.Checkbox(
                    label="Enable automatic chunk regeneration",
                    value=ENABLE_REGENERATION_LOOP,
                    info="Retry failed chunks automatically"
                )

                max_attempts = gr.Slider(
                    label="Max Attempts",
                    minimum=1, maximum=10, step=1,
                    value=MAX_REGENERATION_ATTEMPTS
                )

                quality_threshold = gr.Slider(
                    label="Quality Threshold",
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=QUALITY_THRESHOLD
                )

                gr.Markdown("### 📊 Sentiment Smoothing")

                sentiment_smoothing = gr.Checkbox(
                    label="Enable sentiment smoothing",
                    value=ENABLE_SENTIMENT_SMOOTHING,
                    info="Smooth emotional transitions"
                )

                smoothing_window = gr.Slider(
                    label="Window Size",
                    minimum=1, maximum=10, step=1,
                    value=SENTIMENT_SMOOTHING_WINDOW
                )

                smoothing_method = gr.Dropdown(
                    label="Smoothing Method",
                    choices=["rolling", "exp_decay"],
                    value=SENTIMENT_SMOOTHING_METHOD
                )

                gr.Markdown("### 🔍 Advanced Detection")

                mfcc_validation = gr.Checkbox(
                    label="MFCC spectral analysis",
                    value=ENABLE_MFCC_VALIDATION,
                    info="Advanced audio quality detection"
                )

                output_validation = gr.Checkbox(
                    label="Output validation",
                    value=ENABLE_OUTPUT_VALIDATION,
                    info="Quality control clearinghouse for enabled checks"
                )

                spectral_threshold = gr.Slider(
                    label="Spectral Threshold",
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=SPECTRAL_ANOMALY_THRESHOLD
                )

                output_threshold = gr.Slider(
                    label="Output Threshold",
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=OUTPUT_VALIDATION_THRESHOLD
                )


        # TTS Parameters
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎛️ TTS Parameters")

                exaggeration = gr.Slider(
                    label="Exaggeration",
                    minimum=TTS_PARAM_MIN_EXAGGERATION,
                    maximum=TTS_PARAM_MAX_EXAGGERATION,
                    step=0.1,
                    value=DEFAULT_EXAGGERATION,
                    info="Emotional intensity"
                )

                cfg_weight = gr.Slider(
                    label="CFG Weight",
                    minimum=TTS_PARAM_MIN_CFG_WEIGHT,
                    maximum=TTS_PARAM_MAX_CFG_WEIGHT,
                    step=0.1,
                    value=DEFAULT_CFG_WEIGHT,
                    info="Text faithfulness"
                )

                temperature = gr.Slider(
                    label="Temperature",
                    minimum=TTS_PARAM_MIN_TEMPERATURE,
                    maximum=TTS_PARAM_MAX_TEMPERATURE,
                    step=0.1,
                    value=DEFAULT_TEMPERATURE,
                    info="Creativity/randomness"
                )

            with gr.Column():
                gr.Markdown("### ⚡ Advanced Sampling")

                min_p = gr.Slider(
                    label="Min-P",
                    minimum=0.0, maximum=0.5, step=0.01,
                    value=0.05,
                    info="Minimum probability threshold"
                )

                top_p = gr.Slider(
                    label="Top-P",
                    minimum=0.5, maximum=1.0, step=0.1,
                    value=1.0,
                    info="Nucleus sampling"
                )

                repetition_penalty = gr.Slider(
                    label="Repetition Penalty",
                    minimum=1.0, maximum=3.0, step=0.1,
                    value=2.0,
                    info="Reduce repetition"
                )

                gr.Markdown("### ⚙️ Performance Settings")
                
                max_workers = gr.Number(
                    label="Max Workers",
                    minimum=1, maximum=8, step=1,
                    value=2,
                    info="⚠️ Only increase above 2 if CPU/GPU utilization < 70%"
                )

        # Action Buttons and Status
        with gr.Row():
            with gr.Column(scale=2):
                convert_btn = gr.Button(
                    "🚀 Start Conversion",
                    variant="primary",
                    size="lg",
                    interactive=True
                )

                # Status Display
                status_display = gr.Textbox(
                    label="Status",
                    value="⏸ Ready",
                    interactive=False,
                    lines=1
                )

                progress_display = gr.Number(
                    label="Progress %",
                    value=0,
                    interactive=False,
                    precision=0
                )

            with gr.Column(scale=1):
                gr.Markdown("### 📊 Processing Stats")

                realtime_factor = gr.Textbox(
                    label="Realtime Factor",
                    value="--",
                    interactive=False
                )

                vram_usage = gr.Textbox(
                    label="VRAM Usage",
                    value="-- GB",
                    interactive=False
                )

                current_chunk = gr.Textbox(
                    label="Current Chunk",
                    value="--",
                    interactive=False
                )

        # Regenerate M4B Section (moved above audiobook player)
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔄 Regenerate M4B")

                with gr.Row():
                    with gr.Column(scale=2):
                        m4b_file_selector = gr.Dropdown(
                            label="Select M4B File to Regenerate",
                            choices=[],
                            value=None,
                            interactive=True,
                            info="Choose from generated audiobook files"
                        )

                    with gr.Column(scale=1):
                        playback_speed = gr.Slider(
                            label="Playback Speed",
                            minimum=0.5,
                            maximum=2.0,
                            step=0.1,
                            value=1.0,
                            info="Speed adjustment for regeneration"
                        )

                regenerate_m4b_btn = gr.Button(
                    "🔄 Regenerate M4B",
                    variant="secondary",
                    size="lg"
                )

        # Generated Audiobook Player (simplified, play-only)
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎧 Generated Audiobook Player")

                # Audiobook file selector dropdown
                audiobook_selector = gr.Dropdown(
                    label="Select Audiobook",
                    choices=[],
                    value=None,
                    interactive=True,
                    info="Choose from session audiobooks"
                )

                # Main audio player - play only, no upload
                audio_player = gr.Audio(
                    label="Audiobook Player",
                    value=None,
                    interactive=False,
                    show_download_button=True,
                    show_share_button=False,
                    waveform_options=gr.WaveformOptions(
                        show_controls=True,
                        show_recording_waveform=False,
                        skip_length=10
                    )
                )

    # Event Handlers
    def handle_voice_upload(voice_file):
        """Handle voice file upload and show player"""
        if voice_file is None:
            return gr.update(value=None, visible=False)

        # Show the voice player with uploaded file
        return gr.update(value=voice_file, visible=True)

    def get_session_audiobooks():
        """Get list of M4B files from current session, sorted by creation time (newest first)"""
        audiobooks = []

        # Look in Audiobook directory for M4B files
        audiobook_root = Path("Audiobook")
        if audiobook_root.exists():
            for book_dir in audiobook_root.iterdir():
                if book_dir.is_dir():
                    # Look for M4B files in book directory
                    for m4b_file in book_dir.glob("*.m4b"):
                        # Get creation time for sorting
                        creation_time = m4b_file.stat().st_mtime
                        audiobooks.append((str(m4b_file), m4b_file.name, creation_time))

        # Also check Output directory
        output_root = Path("Output")
        if output_root.exists():
            for m4b_file in output_root.glob("*.m4b"):
                creation_time = m4b_file.stat().st_mtime
                audiobooks.append((str(m4b_file), m4b_file.name, creation_time))

        # Sort by creation time (newest first)
        audiobooks.sort(key=lambda x: x[2], reverse=True)

        # Return just path and name (drop creation time)
        return [(ab[0], ab[1]) for ab in audiobooks]

    def update_audiobook_dropdowns(latest_file=None):
        """Update audiobook dropdowns - after conversion both show latest, after regeneration only playback updates"""
        audiobooks = get_session_audiobooks()
        choices = [ab[1] for ab in audiobooks]  # Just filenames for display

        # Determine what to set as selected
        if latest_file:
            # Use specific file if provided
            selected_file = latest_file
        elif choices:
            # Default to newest file (first in sorted list)
            selected_file = choices[0]
        else:
            selected_file = None

        return (
            gr.update(choices=choices, value=selected_file),  # audiobook_selector (playback)
            gr.update(choices=choices, value=selected_file)   # m4b_file_selector (regeneration source)
        )

    def update_audiobook_dropdowns_after_conversion():
        """Update both dropdowns to show the newest generated file after conversion"""
        return update_audiobook_dropdowns()

    def update_playback_only(new_file_name):
        """Update only the playback dropdown after regeneration"""
        audiobooks = get_session_audiobooks()
        choices = [ab[1] for ab in audiobooks]

        return (
            gr.update(choices=choices, value=new_file_name),  # audiobook_selector (playback) - new file
            gr.update()  # m4b_file_selector (regeneration) - no change
        )

    def load_selected_audiobook(selected_audiobook):
        """Load selected audiobook into player"""
        if not selected_audiobook:
            return None

        # Find the full path for the selected audiobook
        audiobooks = get_session_audiobooks()
        for full_path, filename in audiobooks:
            if filename == selected_audiobook:
                return full_path

        return None

    def handle_asr_toggle(asr_enabled_val):
        """Show/hide ASR configuration when ASR is toggled"""
        return gr.update(visible=asr_enabled_val)

    def analyze_system():
        """Analyze system capabilities and return summary"""
        try:
            from modules.system_detector import get_system_profile, print_system_summary, categorize_system

            profile = get_system_profile()
            categories = categorize_system(profile)

            summary = f"🖥️ System Profile:\n"
            summary += f"VRAM: {profile['gpu']['total_mb']:,}MB total, {profile['available_vram_after_tts']:,}MB available after TTS ({categories['vram']} class)\n"
            summary += f"RAM: {profile['ram']['total_mb']:,}MB total, {profile['ram']['available_mb']:,}MB available ({categories['ram']} class)\n"
            summary += f"CPU: {profile['cpu_cores']} cores ({categories['cpu']} class)"

            if not profile['has_gpu']:
                summary += f"\n⚠️ No CUDA GPU detected - ASR will run on CPU only"

            return summary

        except Exception as e:
            return f"❌ Error analyzing system: {str(e)}"

    def update_asr_models(asr_level_val):
        """Update ASR model display based on selected level"""
        try:
            from modules.system_detector import get_system_profile, recommend_asr_models

            profile = get_system_profile()
            recommendations = recommend_asr_models(profile)

            if asr_level_val not in recommendations:
                return "❌ Invalid ASR level selected"

            config = recommendations[asr_level_val]
            primary = config['primary']
            fallback = config['fallback']

            result = f"Primary: {primary['model']} on {primary['device'].upper()}\n"
            result += f"Fallback: {fallback['model']} on {fallback['device'].upper()}"

            if asr_level_val == 'insane':
                result += f"\n⚠️ WARNING: INSANE mode may cause memory pressure"

            return result

        except Exception as e:
            return f"❌ Error getting models: {str(e)}"

    def start_conversion(text_file_upload, voice_file_upload,
                        vader_val, asr_val, asr_level_val, add_to_batch_val,
                        regen_enabled_val, max_attempts_val, quality_thresh_val,
                        sentiment_smooth_val, smooth_window_val, smooth_method_val,
                        mfcc_val, output_val, spectral_thresh_val, output_thresh_val,
                        exag_val, cfg_val, temp_val, min_p_val, top_p_val, rep_penalty_val,
                        max_workers_val):
        """Start the actual book conversion - file upload version"""

        # Validation
        if not text_file_upload:
            return "❌ Please upload a text file", 0, None, None
        if not voice_file_upload:
            return "❌ Please upload a voice sample", 0, None, None

        # Check if already running
        if conversion_state['running']:
            return "⚠️ Conversion already in progress", conversion_state['progress'], None, None

        try:
            # Create temporary book structure from uploads
            import tempfile
            import shutil
            from datetime import datetime

            # Generate unique book name from text file
            text_filename = Path(text_file_upload).name
            book_name = text_filename.replace('.txt', '').replace(' ', '_')
            timestamp = datetime.now().strftime("%H%M%S")
            unique_book_name = f"{book_name}_{timestamp}"

            # Create directory structure
            text_input_dir = Path("Text_Input")
            text_input_dir.mkdir(exist_ok=True)

            book_dir = text_input_dir / unique_book_name
            book_dir.mkdir(exist_ok=True)

            # Copy uploaded files to expected locations
            text_dest = book_dir / f"{unique_book_name}.txt"
            shutil.copy2(text_file_upload, text_dest)

            voice_samples_dir = Path("Voice_Samples")
            voice_samples_dir.mkdir(exist_ok=True)

            voice_filename = Path(voice_file_upload).name
            voice_dest = voice_samples_dir / voice_filename
            shutil.copy2(voice_file_upload, voice_dest)

            print(f"📁 Created book structure: {book_dir}")
            print(f"📄 Text file: {text_dest}")
            print(f"🎤 Voice file: {voice_dest}")

        except Exception as e:
            return f"❌ Error setting up files: {e}", 0, None, None

        # Build ASR configuration first
        asr_config = {'enabled': False}
        if asr_val:
            try:
                from modules.system_detector import get_system_profile, recommend_asr_models
                profile = get_system_profile()
                recommendations = recommend_asr_models(profile)

                if asr_level_val in recommendations:
                    selected_config = recommendations[asr_level_val]
                    primary = selected_config['primary']
                    fallback = selected_config['fallback']

                    asr_config = {
                        'enabled': True,
                        'level': asr_level_val,
                        'primary_model': primary['model'],
                        'primary_device': primary['device'],
                        'fallback_model': fallback['model'],
                        'fallback_device': fallback['device']
                    }
            except Exception as e:
                print(f"⚠️ Error configuring ASR: {e}")
                asr_config = {'enabled': False}

        # Prepare parameters (matching GUI structure exactly)
        tts_params = {
            'exaggeration': exag_val,
            'cfg_weight': cfg_val,
            'temperature': temp_val,
            'min_p': min_p_val,
            'top_p': top_p_val,
            'repetition_penalty': rep_penalty_val,
            'enable_asr': asr_config.get('enabled', False),  # Match GUI pattern
            'max_workers': int(max_workers_val)  # User-defined worker count
        }

        quality_params = {
            'regeneration_enabled': regen_enabled_val,
            'max_attempts': max_attempts_val,
            'quality_threshold': quality_thresh_val,
            'sentiment_smoothing': sentiment_smooth_val,
            'smoothing_window': smooth_window_val,
            'smoothing_method': smooth_method_val,
            'mfcc_validation': mfcc_val,
            'output_validation': output_val,
            'spectral_threshold': spectral_thresh_val,
            'output_threshold': output_thresh_val
        }

        config_params = {
            'vader_enabled': vader_val,
            'asr_enabled': asr_val,
            'asr_config': asr_config,
            'add_to_batch': add_to_batch_val
        }

        # Set conversion state
        conversion_state['running'] = True
        conversion_state['progress'] = 0
        conversion_state['status'] = 'Starting conversion...'
        conversion_state['current_book'] = book_dir.name  # Track current book

        try:
            # Run conversion using the modular backend in a separate thread
            import threading

            def run_conversion_thread():
                try:
                    result = run_book_conversion(
                        str(book_dir), str(text_dest), str(voice_dest),
                        tts_params, quality_params, config_params
                    )

                    if result['success']:
                        conversion_state['status'] = '🎉 CONVERSION COMPLETE! M4B audiobook ready for playback.'
                        conversion_state['progress'] = 100
                        conversion_state['auto_refresh_needed'] = True  # Flag for auto-refresh
                    else:
                        conversion_state['status'] = f"❌ Conversion failed: {result.get('error', 'Unknown error')}"
                        conversion_state['progress'] = 0

                except Exception as e:
                    conversion_state['status'] = f"❌ Error: {str(e)}"
                    conversion_state['progress'] = 0
                finally:
                    conversion_state['running'] = False

            # Start conversion thread
            thread = threading.Thread(target=run_conversion_thread)
            thread.start()

            # Return immediate response - user will need to refresh to see final results
            return (
                "🚀 Conversion started in background...",
                5,  # Initial progress
                None,
                gr.update(),
                gr.update()
            )

        except Exception as e:
            conversion_state['status'] = f"❌ Error: {str(e)}"
            return conversion_state['status'], 0, None, gr.update(), gr.update()
        finally:
            conversion_state['running'] = False


    # Connect event handlers

    # ASR event handlers
    asr_enabled.change(
        handle_asr_toggle,
        inputs=[asr_enabled],
        outputs=[asr_config_group]
    )

    analyze_system_btn.click(
        analyze_system,
        inputs=[],
        outputs=[system_analysis]
    )

    asr_level.change(
        update_asr_models,
        inputs=[asr_level],
        outputs=[selected_models]
    )

    # Voice upload handler
    voice_file_upload.change(
        handle_voice_upload,
        inputs=[voice_file_upload],
        outputs=[voice_audio]
    )

    # Main conversion handler
    convert_btn.click(
        start_conversion,
        inputs=[
            text_file_upload, voice_file_upload,
            vader_enabled, asr_enabled, asr_level, add_to_batch,
            regeneration_enabled, max_attempts, quality_threshold,
            sentiment_smoothing, smoothing_window, smoothing_method,
            mfcc_validation, output_validation, spectral_threshold, output_threshold,
            exaggeration, cfg_weight, temperature, min_p, top_p, repetition_penalty,
            max_workers
        ],
        outputs=[status_display, progress_display, audio_player, audiobook_selector, m4b_file_selector]
    )

    # Audiobook selector handler
    audiobook_selector.change(
        load_selected_audiobook,
        inputs=[audiobook_selector],
        outputs=[audio_player]
    )

    # M4B regeneration handler
    def handle_m4b_regeneration(selected_m4b, speed):
        """Handle M4B regeneration and update player"""
        status_msg, new_m4b_path = regenerate_m4b_file(selected_m4b, speed)

        if new_m4b_path:
            # Load the new M4B in the player
            new_file_name = Path(new_m4b_path).name
            new_audio = load_selected_audiobook(new_file_name)
            # Update only playback dropdown, keep regeneration dropdown on source file
            audiobook_choices, m4b_choices = update_playback_only(new_file_name)
            return status_msg, new_audio, audiobook_choices, m4b_choices
        else:
            return status_msg, None, gr.update(), gr.update()

    regenerate_m4b_btn.click(
        handle_m4b_regeneration,
        inputs=[m4b_file_selector, playback_speed],
        outputs=[status_display, audio_player, audiobook_selector, m4b_file_selector]
    )

    # Progress monitoring with file-based approach
    def get_current_stats():
        """Get current progress statistics by monitoring output files"""
        try:
            if conversion_state['running']:
                # Look for generated audio chunks to estimate progress
                book_name = conversion_state.get('current_book', 'unknown')
                audiobook_root = Path("Audiobook") / book_name / "TTS" / "audio_chunks"

                if audiobook_root.exists():
                    chunk_files = list(audiobook_root.glob("chunk_*.wav"))
                    current_chunks = len(chunk_files)

                    # Try to estimate total from JSON if available
                    json_path = Path("Text_Input") / f"{book_name}_chunks.json"
                    total_chunks = 0
                    if json_path.exists():
                        import json
                        with open(json_path, 'r') as f:
                            data = json.load(f)
                            total_chunks = len(data)

                    if total_chunks > 0:
                        progress = int((current_chunks / total_chunks) * 100)
                        conversion_state['progress'] = progress
                        conversion_state['current_chunk'] = f"{current_chunks}/{total_chunks}"

                        return (
                            conversion_state.get('realtime_factor', '--'),
                            conversion_state.get('vram_usage', '-- GB'),
                            f"{current_chunks}/{total_chunks}",
                            progress
                        )

            return (
                conversion_state.get('realtime_factor', '--'),
                conversion_state.get('vram_usage', '-- GB'),
                conversion_state.get('current_chunk', '--'),
                conversion_state.get('progress', 0)
            )
        except Exception as e:
            print(f"Error getting stats: {e}")
            return "--", "-- GB", "--", conversion_state.get('progress', 0)

    def auto_check_completion():
        """Automatically check for completion and refresh interface"""
        # First get current stats
        stats = get_current_stats()
        
        # Check if conversion just completed and needs auto-refresh
        if (not conversion_state['running'] and 
            conversion_state['progress'] == 100 and 
            conversion_state.get('auto_refresh_needed', False)):
            
            # Clear the auto-refresh flag
            conversion_state['auto_refresh_needed'] = False
            print("🎉 Auto-detected completion! Refreshing interface...")
            
            # Get completion results
            status, progress, audio, audiobook_choices, m4b_choices = get_status_and_results()
            
            # Return combined stats + completion results
            return (
                stats[0],  # realtime_factor
                stats[1],  # vram_usage  
                stats[2],  # current_chunk
                100,       # progress (completed)
                status,    # completion status
                audio,     # audio player
                audiobook_choices,  # audiobook dropdown
                m4b_choices        # m4b dropdown
            )
        else:
            # Return stats + current status (no completion)
            return (
                stats[0],  # realtime_factor
                stats[1],  # vram_usage
                stats[2],  # current_chunk  
                stats[3],  # progress
                conversion_state.get('status', '⏸ Ready'),  # current status
                gr.update(),  # no audio update
                gr.update(),  # no audiobook update
                gr.update()   # no m4b update
            )

    def get_status_and_results():
        """Get conversion status and results after completion"""
        if not conversion_state['running'] and conversion_state['progress'] == 100:
            # Conversion completed, update dropdowns
            audiobook_choices, m4b_choices = update_audiobook_dropdowns_after_conversion()
            latest_audiobook = None
            if audiobook_choices['choices']:
                latest_audiobook = load_selected_audiobook(audiobook_choices['choices'][0])

            return (
                conversion_state['status'],
                conversion_state['progress'],
                latest_audiobook,
                audiobook_choices,
                m4b_choices
            )
        else:
            return (
                conversion_state['status'],
                conversion_state['progress'],
                None,
                gr.update(),
                gr.update()
            )

    # Create refresh buttons
    with gr.Row():
        refresh_stats_btn = gr.Button("🔄 Refresh Stats", size="sm", variant="secondary")
        check_completion_btn = gr.Button("📋 Check Completion", size="sm", variant="secondary")
    
    # Auto-refresh timer (checks every 5 seconds during conversion)
    auto_timer = gr.Timer(5.0)  # 5 second interval

    refresh_stats_btn.click(
        auto_check_completion,
        outputs=[realtime_factor, vram_usage, current_chunk, progress_display, status_display, audio_player, audiobook_selector, m4b_file_selector]
    )

    check_completion_btn.click(
        get_status_and_results,
        outputs=[status_display, progress_display, audio_player, audiobook_selector, m4b_file_selector]
    )
    
    # Auto-timer for progress monitoring and completion detection
    auto_timer.tick(
        auto_check_completion,
        outputs=[realtime_factor, vram_usage, current_chunk, progress_display, status_display, audio_player, audiobook_selector, m4b_file_selector]
    )

    return {
        'convert_button': convert_btn,
        'status_display': status_display,
        'progress': progress_display
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_convert_book_tab()

    demo.launch()
