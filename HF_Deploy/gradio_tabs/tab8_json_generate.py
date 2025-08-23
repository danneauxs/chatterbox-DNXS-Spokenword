#!/usr/bin/env python3
"""
Gradio Tab 8: JSON Generate
Generate audiobooks directly from JSON files with voice selection - matches PyQt5 GUI Tab 8 functionality
"""

import gradio as gr
import os
import sys
import threading
import time
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Import backend functionality
try:
    from modules.gui_json_generator import generate_audiobook_from_json
    from modules.file_manager import list_voice_samples
    from config.config import AUDIOBOOK_ROOT
    JSON_GENERATE_AVAILABLE = True
    print("✅ JSON generation functionality available")
except ImportError as e:
    print(f"⚠️  JSON generation functionality not available: {e}")
    JSON_GENERATE_AVAILABLE = False

# Global state for JSON generation
json_state = {
    'generation_running': False,
    'current_json_file': None,
    'current_voice': None,
    'generated_audiobook': None,
    'audio_process': None,
    'audio_position': 0,
    'audio_duration': 0,
    'progress': 0,
    'status': 'Ready'
}

def get_available_json_files():
    """Find available JSON chunk files for generation"""
    json_files = []
    
    if not JSON_GENERATE_AVAILABLE:
        return json_files
    
    # Look in TTS processing directories
    audiobook_root = Path(AUDIOBOOK_ROOT)
    if audiobook_root.exists():
        for book_dir in audiobook_root.iterdir():
            if book_dir.is_dir():
                tts_chunks_dir = book_dir / "TTS" / "text_chunks"
                json_path = tts_chunks_dir / "chunks_info.json"
                if json_path.exists():
                    try:
                        with open(json_path, 'r') as f:
                            chunks_data = json.load(f)
                            chunk_count = len(chunks_data)
                        
                        json_files.append({
                            'name': book_dir.name,
                            'path': str(json_path),
                            'chunk_count': chunk_count,
                            'display': f"{book_dir.name} ({chunk_count} chunks)",
                            'type': 'TTS'
                        })
                    except:
                        pass
    
    # Look in Text_Input directory
    text_input_dir = Path("Text_Input")
    if text_input_dir.exists():
        for json_file in text_input_dir.glob("*_chunks.json"):
            book_name = json_file.stem.replace("_chunks", "")
            # Only add if not already found in TTS directories
            if not any(jf['name'] == book_name for jf in json_files):
                try:
                    with open(json_file, 'r') as f:
                        chunks_data = json.load(f)
                        chunk_count = len(chunks_data)
                    
                    json_files.append({
                        'name': book_name,
                        'path': str(json_file),
                        'chunk_count': chunk_count,
                        'display': f"{book_name} ({chunk_count} chunks)",
                        'type': 'Text_Input'
                    })
                except:
                    pass
    
    return sorted(json_files, key=lambda x: x['name'])

def get_available_voices():
    """Get list of available voice samples"""
    voices = []
    
    if not JSON_GENERATE_AVAILABLE:
        return voices
    
    try:
        voice_files = list_voice_samples()
        for voice_file in voice_files:
            voices.append({
                'name': voice_file.stem,
                'path': str(voice_file),
                'display': f"{voice_file.stem} ({voice_file.name})"
            })
    except Exception as e:
        print(f"Error getting voices: {e}")
    
    return sorted(voices, key=lambda x: x['name'])

def load_json_file_info(file_selection):
    """Load information about selected JSON file"""
    if not file_selection or file_selection == "-- Select JSON File --":
        return "No JSON file selected", "No file loaded"
    
    try:
        # Find the selected file
        json_files = get_available_json_files()
        selected_file = None
        for jf in json_files:
            if jf['display'] == file_selection:
                selected_file = jf
                break
        
        if not selected_file:
            return "❌ Selected file not found", "Error"
        
        json_state['current_json_file'] = selected_file
        
        # Load and analyze JSON
        with open(selected_file['path'], 'r') as f:
            chunks_data = json.load(f)
        
        chunk_count = len(chunks_data)
        
        # Calculate estimated metrics
        total_words = sum(chunk.get('word_count', len(chunk.get('text', '').split())) for chunk in chunks_data)
        estimated_duration_seconds = total_words * 0.4  # Rough estimate: 0.4 seconds per word
        estimated_duration = f"{int(estimated_duration_seconds // 3600):02d}:{int((estimated_duration_seconds % 3600) // 60):02d}:{int(estimated_duration_seconds % 60):02d}"
        
        # Check for existing audio chunks
        book_name = selected_file['name']
        audio_chunks_dir = Path(AUDIOBOOK_ROOT) / book_name / "TTS" / "audio_chunks"
        existing_chunks = 0
        if audio_chunks_dir.exists():
            existing_chunks = len(list(audio_chunks_dir.glob("chunk_*.wav")))
        
        info = f"""**📄 JSON File Analysis:**
**File:** {selected_file['path']}
**Book:** {book_name}
**Source:** {selected_file['type']}

**Content:**
• Total Chunks: {chunk_count}
• Total Words: {total_words:,}
• Estimated Duration: {estimated_duration}

**Status:**
• Existing Audio: {existing_chunks}/{chunk_count} chunks
• Ready for Generation: {'✅ Yes' if chunk_count > 0 else '❌ No chunks found'}"""
        
        current_file = f"📁 Selected: {book_name} ({chunk_count} chunks)"
        
        return info, current_file
        
    except Exception as e:
        return f"❌ Error loading JSON file: {str(e)}", "Error loading file"

def start_json_generation(json_selection, voice_selection, temperature_override):
    """Start JSON-to-audiobook generation"""
    if json_state['generation_running']:
        return "⚠️ Generation already in progress", 0, "Generation running...", "Processing..."
    
    if not json_selection or json_selection == "-- Select JSON File --":
        return "❌ Please select a JSON file", 0, "No file selected", "Ready"
    
    if not voice_selection or voice_selection == "-- Select Voice --":
        return "❌ Please select a voice", 0, "No voice selected", "Ready"
    
    try:
        # Find selected files
        json_files = get_available_json_files()
        voices = get_available_voices()
        
        selected_json = None
        for jf in json_files:
            if jf['display'] == json_selection:
                selected_json = jf
                break
        
        selected_voice = None
        for v in voices:
            if v['display'] == voice_selection:
                selected_voice = v
                break
        
        if not selected_json or not selected_voice:
            return "❌ Invalid selection", 0, "Selection error", "Ready"
        
        json_state['current_json_file'] = selected_json
        json_state['current_voice'] = selected_voice
        json_state['generation_running'] = True
        json_state['progress'] = 0
        json_state['status'] = 'Starting generation...'
        
        # Start generation in background thread
        def generation_worker():
            try:
                json_state['status'] = '🎵 Generating audiobook from JSON...'
                json_state['progress'] = 10
                
                # Apply temperature override if specified
                temp_setting = None
                if temperature_override and temperature_override > 0:
                    temp_setting = temperature_override
                
                # Run the generation
                success, message, audiobook_path = generate_audiobook_from_json(
                    selected_json['path'],
                    selected_voice['name'], 
                    temp_setting
                )
                
                if success:
                    json_state['progress'] = 100
                    json_state['status'] = '✅ Generation completed successfully!'
                    json_state['generated_audiobook'] = audiobook_path
                else:
                    json_state['progress'] = 0
                    json_state['status'] = f'❌ Generation failed: {message}'
                    json_state['generated_audiobook'] = None
                    
            except Exception as e:
                json_state['progress'] = 0
                json_state['status'] = f'❌ Generation error: {str(e)}'
                json_state['generated_audiobook'] = None
            finally:
                json_state['generation_running'] = False
        
        # Start worker thread
        threading.Thread(target=generation_worker, daemon=True).start()
        
        return (
            "🎵 Starting JSON audiobook generation...",
            10,
            f"Generating: {selected_json['name']} with voice: {selected_voice['name']}",
            "Generation started"
        )
        
    except Exception as e:
        json_state['generation_running'] = False
        return f"❌ Error starting generation: {str(e)}", 0, "Generation failed", "Error"

def get_generation_status():
    """Get current generation status"""
    return (
        json_state.get('status', 'Ready'),
        json_state.get('progress', 0),
        json_state.get('generated_audiobook', 'No audiobook generated') or 'No audiobook generated',
        "Generation running..." if json_state['generation_running'] else "Ready"
    )

def stop_json_generation():
    """Stop current generation (if possible)"""
    if json_state['generation_running']:
        json_state['generation_running'] = False
        json_state['status'] = '⏹️ Generation stopped by user'
        json_state['progress'] = 0
        return "⏹️ Generation stopped", 0, "Generation stopped", "Ready"
    else:
        return "No generation to stop", json_state.get('progress', 0), json_state.get('status', 'Ready'), "Ready"

# Audio playback functions (simplified - web browsers handle audio playback)
def play_audio():
    """Play generated audiobook"""
    if not json_state.get('generated_audiobook'):
        return "❌ No audiobook generated to play"
    
    try:
        audiobook_path = json_state['generated_audiobook']
        if isinstance(audiobook_path, str):
            audiobook_path = Path(audiobook_path)
        
        if not audiobook_path.exists():
            return f"❌ Audio file not found: {audiobook_path}"
        
        # For web interface, we can't directly control audio playback
        # User would need to download and play manually
        return f"🔊 Audio file ready for playback: {audiobook_path.name}"
        
    except Exception as e:
        return f"❌ Error accessing audio: {str(e)}"

def create_json_generate_tab():
    """Create Tab 8: JSON Generate with all GUI functionality"""
    
    with gr.Column():
        gr.Markdown("# 📄 Generate Audiobook from JSON")
        gr.Markdown("*Direct audiobook generation from preprocessed JSON files - matches GUI Tab 8*")
        
        if not JSON_GENERATE_AVAILABLE:
            gr.Markdown("### ❌ JSON Generation Not Available")
            gr.Markdown("Missing required backend modules. Please ensure modules/gui_json_generator.py is available.")
            return {}
        
        # JSON File Selection Section
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📄 JSON File Selection")
                
                json_files = get_available_json_files()
                json_choices = ["-- Select JSON File --"] + [jf['display'] for jf in json_files]
                
                json_file_selector = gr.Dropdown(
                    label="JSON Chunks File",
                    choices=json_choices,
                    value="-- Select JSON File --",
                    interactive=True,
                    info="Select preprocessed JSON file containing text chunks"
                )
                
                # Manual path input
                json_manual_path = gr.Textbox(
                    label="Or Enter JSON Path Manually",
                    placeholder="e.g., /path/to/book_chunks.json",
                    interactive=True,
                    info="Direct path to JSON chunks file"
                )
                
                refresh_json_btn = gr.Button(
                    "🔄 Refresh JSON Files",
                    variant="secondary",
                    size="sm"
                )
            
            with gr.Column(scale=1):
                json_file_info = gr.Markdown(
                    "No JSON file selected",
                    label="File Information"
                )
        
        # Voice Selection Section
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎤 Voice Selection")
                
                voices = get_available_voices()
                voice_choices = ["-- Select Voice --"] + [v['display'] for v in voices]
                
                voice_selector = gr.Dropdown(
                    label="Voice for Generation",
                    choices=voice_choices,
                    value="-- Select Voice --",
                    interactive=True,
                    info="Select voice sample for audiobook generation"
                )
                
                refresh_voices_btn = gr.Button(
                    "🔄 Refresh Voice List",
                    variant="secondary",
                    size="sm"
                )
        
        # Generation Parameters
        with gr.Row():
            with gr.Column():
                gr.Markdown("### ⚙️ Generation Parameters")
                
                temperature_override = gr.Slider(
                    label="Temperature Override (Optional)",
                    minimum=0.0, maximum=2.0, step=0.1,
                    value=0.0,
                    interactive=True,
                    info="Override TTS temperature (0 = use JSON values)"
                )
                
                gr.Markdown("*Leave temperature at 0 to use individual chunk TTS parameters from JSON*")
        
        # Generation Controls
        with gr.Row():
            generate_btn = gr.Button(
                "🎵 Generate Audiobook from JSON",
                variant="primary",
                size="lg",
                interactive=True
            )
            
            stop_btn = gr.Button(
                "⏹️ Stop Generation",
                variant="secondary",
                size="lg",
                interactive=True
            )
        
        # Progress and Status
        with gr.Row():
            with gr.Column(scale=2):
                generation_status = gr.Textbox(
                    label="Generation Status",
                    value="Ready for JSON audiobook generation",
                    interactive=False,
                    lines=2
                )
                
                progress_bar = gr.Slider(
                    label="Progress %",
                    minimum=0, maximum=100, step=1,
                    value=0,
                    interactive=False,
                    info="Generation progress"
                )
            
            with gr.Column(scale=1):
                current_file_display = gr.Textbox(
                    label="Current File",
                    value="No file selected",
                    interactive=False
                )
                
                operation_status = gr.Textbox(
                    label="Operation Status", 
                    value="Ready",
                    interactive=False
                )
        
        # Audio Playback Section
        with gr.Column():
            gr.Markdown("### 🔊 Generated Audiobook")
            
            generated_file_info = gr.Textbox(
                label="Generated Audiobook",
                value="No audiobook generated",
                interactive=False,
                info="Path to generated audiobook file"
            )
            
            # Simple playback controls (web-based)
            with gr.Row():
                play_info_btn = gr.Button(
                    "📁 Show File Info",
                    variant="secondary",
                    size="lg"
                )
                
                download_btn = gr.Button(
                    "⬇️ Download Instructions",
                    variant="secondary", 
                    size="lg"
                )
            
            playback_info = gr.Markdown(
                "*Generated audiobook files will be saved to the Output/ directory. Download and play using your preferred audio player.*",
                visible=True
            )
        
        # Status refresh button
        with gr.Row():
            refresh_status_btn = gr.Button(
                "🔄 Refresh Status",
                variant="secondary",
                size="sm"
            )
    
    # Event Handlers
    def refresh_json_files():
        """Refresh JSON files list"""
        json_files = get_available_json_files()
        choices = ["-- Select JSON File --"] + [jf['display'] for jf in json_files]
        return gr.update(choices=choices, value="-- Select JSON File --")
    
    def refresh_voice_list():
        """Refresh voice samples list"""
        voices = get_available_voices()
        choices = ["-- Select Voice --"] + [v['display'] for v in voices]
        return gr.update(choices=choices, value="-- Select Voice --")
    
    def show_download_info():
        """Show download/playback instructions"""
        return """## 📁 Audiobook File Access

**Generated audiobooks are saved to:**
- `Output/[BookName]/` directory
- Files: `.wav` (uncompressed) and `.m4b` (audiobook format)

**To play your audiobook:**
1. Navigate to the Output directory
2. Download the `.m4b` file for best audiobook experience
3. Use any audio player (VLC, iTunes, Audible app, etc.)
4. The `.m4b` format supports chapters and bookmarks

**File locations:**
- Individual chunks: `Audiobook/[BookName]/TTS/audio_chunks/`
- Combined audiobook: `Output/[BookName]/`
"""
    
    # Connect event handlers
    refresh_json_btn.click(
        refresh_json_files,
        inputs=[],
        outputs=[json_file_selector]
    )
    
    refresh_voices_btn.click(
        refresh_voice_list,
        inputs=[],
        outputs=[voice_selector]
    )
    
    json_file_selector.change(
        load_json_file_info,
        inputs=[json_file_selector],
        outputs=[json_file_info, current_file_display]
    )
    
    generate_btn.click(
        start_json_generation,
        inputs=[json_file_selector, voice_selector, temperature_override],
        outputs=[generation_status, progress_bar, generated_file_info, operation_status]
    )
    
    stop_btn.click(
        stop_json_generation,
        inputs=[],
        outputs=[generation_status, progress_bar, generated_file_info, operation_status]
    )
    
    refresh_status_btn.click(
        get_generation_status,
        inputs=[],
        outputs=[generation_status, progress_bar, generated_file_info, operation_status]
    )
    
    play_info_btn.click(
        play_audio,
        inputs=[],
        outputs=[generated_file_info]
    )
    
    download_btn.click(
        show_download_info,
        inputs=[],
        outputs=[playback_info]
    )
    
    return {
        'json_selector': json_file_selector,
        'voice_selector': voice_selector,
        'generate_button': generate_btn,
        'status_display': generation_status
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_json_generate_tab()
    
    demo.launch()