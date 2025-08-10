#!/usr/bin/env python3
"""
Gradio Tab 5: Prepare Text
Text file preparation and chunking with VADER analysis - matches PyQt5 GUI Tab 5 functionality
"""

import gradio as gr
import os
import sys
import threading
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Import backend functionality
try:
    from modules.tts_engine import generate_enriched_chunks
    from config.config import (
        AUDIOBOOK_ROOT, TEXT_INPUT_ROOT,
        BASE_EXAGGERATION, BASE_CFG_WEIGHT, BASE_TEMPERATURE,
        DEFAULT_MIN_P, DEFAULT_TOP_P, DEFAULT_REPETITION_PENALTY,
        ENABLE_SENTIMENT_SMOOTHING, SENTIMENT_SMOOTHING_WINDOW, SENTIMENT_SMOOTHING_METHOD,
        VADER_EXAGGERATION_SENSITIVITY, VADER_CFG_WEIGHT_SENSITIVITY, VADER_TEMPERATURE_SENSITIVITY
    )
    PREPARE_TEXT_AVAILABLE = True
    print("✅ Text preparation functionality available")
except ImportError as e:
    print(f"⚠️  Text preparation functionality not available: {e}")
    PREPARE_TEXT_AVAILABLE = False
    # Default values if config not available
    BASE_EXAGGERATION = 0.5
    BASE_CFG_WEIGHT = 0.5
    BASE_TEMPERATURE = 0.8
    DEFAULT_MIN_P = 0.1
    DEFAULT_TOP_P = 0.9
    DEFAULT_REPETITION_PENALTY = 1.0
    ENABLE_SENTIMENT_SMOOTHING = True
    SENTIMENT_SMOOTHING_WINDOW = 3
    SENTIMENT_SMOOTHING_METHOD = "gaussian"
    VADER_EXAGGERATION_SENSITIVITY = 0.3
    VADER_CFG_WEIGHT_SENSITIVITY = 0.3
    VADER_TEMPERATURE_SENSITIVITY = 0.3

# Global state for text preparation
prepare_state = {
    'preparation_running': False,
    'current_file': None,
    'progress': 0,
    'status': 'Ready',
    'generated_chunks': 0,
    'output_path': None
}

def get_available_text_files():
    """Find available text files for preparation"""
    text_files = []
    
    if not PREPARE_TEXT_AVAILABLE:
        return text_files
    
    # Look in Text_Input directory structure
    text_input_root = Path(TEXT_INPUT_ROOT) if 'TEXT_INPUT_ROOT' in globals() else Path("Text_Input")
    if text_input_root.exists():
        # Look for text files in subdirectories (book folders)
        for book_dir in text_input_root.iterdir():
            if book_dir.is_dir():
                for text_file in book_dir.glob("*.txt"):
                    try:
                        # Check if file has content
                        if text_file.stat().st_size > 0:
                            text_files.append({
                                'name': f"{book_dir.name}/{text_file.name}",
                                'path': str(text_file),
                                'book_name': book_dir.name,
                                'file_name': text_file.name,
                                'size': text_file.stat().st_size,
                                'display': f"{book_dir.name}/{text_file.name} ({text_file.stat().st_size // 1024}KB)"
                            })
                    except:
                        pass
        
        # Also look for direct text files in Text_Input root
        for text_file in text_input_root.glob("*.txt"):
            try:
                if text_file.stat().st_size > 0:
                    text_files.append({
                        'name': text_file.name,
                        'path': str(text_file),
                        'book_name': text_file.stem,
                        'file_name': text_file.name,
                        'size': text_file.stat().st_size,
                        'display': f"{text_file.name} ({text_file.stat().st_size // 1024}KB)"
                    })
            except:
                pass
    
    return sorted(text_files, key=lambda x: x['name'])

def load_text_file_info(file_selection):
    """Load information about selected text file"""
    if not file_selection or file_selection == "-- Select Text File --":
        return "No text file selected", "No file loaded"
    
    try:
        # Find the selected file
        text_files = get_available_text_files()
        selected_file = None
        for tf in text_files:
            if tf['display'] == file_selection:
                selected_file = tf
                break
        
        if not selected_file:
            return "❌ Selected file not found", "Error"
        
        prepare_state['current_file'] = selected_file
        
        # Analyze text file
        text_path = Path(selected_file['path'])
        with open(text_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic statistics
        char_count = len(content)
        word_count = len(content.split())
        line_count = len(content.splitlines())
        paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        
        # Estimate chunks (rough calculation)
        estimated_chunks = max(1, word_count // 20)  # Assuming ~20 words per chunk average
        
        # Check for existing processed version
        book_name = selected_file['book_name']
        existing_json_path = Path(AUDIOBOOK_ROOT) / book_name / "TTS" / "text_chunks" / "chunks_info.json"
        existing_status = ""
        if existing_json_path.exists():
            try:
                with open(existing_json_path, 'r') as f:
                    existing_data = json.load(f)
                existing_chunks = len(existing_data)
                existing_status = f"\n\n**⚠️ Already Processed:**\n• Existing JSON: {existing_chunks} chunks\n• Path: {existing_json_path}"
            except:
                existing_status = f"\n\n**⚠️ Partial Processing:**\n• JSON file exists but may be corrupted"
        
        info = f"""**📄 Text File Analysis:**
**File:** {selected_file['name']}
**Path:** {text_path}
**Book Name:** {book_name}

**Content Statistics:**
• File Size: {char_count:,} characters ({selected_file['size'] // 1024}KB)
• Word Count: {word_count:,} words
• Lines: {line_count:,}
• Paragraphs: {paragraph_count:,}
• Estimated Chunks: ~{estimated_chunks}

**Processing Status:**
• Ready for preparation: {'✅ Yes' if word_count > 0 else '❌ Empty file'}{existing_status}"""
        
        current_file = f"📁 Selected: {selected_file['name']} ({word_count:,} words)"
        
        return info, current_file
        
    except Exception as e:
        return f"❌ Error loading text file: {str(e)}", "Error loading file"

def start_text_preparation(
    file_selection, 
    use_vader, exaggeration, cfg_weight, temperature, min_p, top_p, repetition_penalty,
    sentiment_smoothing, smoothing_window, smoothing_method,
    vader_exag_sens, vader_cfg_sens, vader_temp_sens
):
    """Start text preparation with enriched chunking"""
    if prepare_state['preparation_running']:
        return "⚠️ Text preparation already in progress", 0, "Processing...", "Generation running..."
    
    if not file_selection or file_selection == "-- Select Text File --":
        return "❌ Please select a text file", 0, "No file selected", "Ready"
    
    try:
        # Find selected file
        text_files = get_available_text_files()
        selected_file = None
        for tf in text_files:
            if tf['display'] == file_selection:
                selected_file = tf
                break
        
        if not selected_file:
            return "❌ Invalid file selection", 0, "Selection error", "Ready"
        
        prepare_state['current_file'] = selected_file
        prepare_state['preparation_running'] = True
        prepare_state['progress'] = 0
        prepare_state['status'] = 'Starting text preparation...'
        
        # Start preparation in background thread
        def preparation_worker():
            try:
                prepare_state['status'] = '📝 Analyzing text and generating chunks...'
                prepare_state['progress'] = 10
                
                text_path = Path(selected_file['path'])
                book_name = selected_file['book_name']
                
                # Create output directory
                book_output_dir = Path(AUDIOBOOK_ROOT) / book_name / "TTS" / "text_chunks"
                book_output_dir.mkdir(parents=True, exist_ok=True)
                
                prepare_state['progress'] = 20
                prepare_state['status'] = '🎭 Applying VADER sentiment analysis...'
                
                # Prepare TTS parameters
                user_tts_params = {
                    'exaggeration': exaggeration,
                    'cfg_weight': cfg_weight,
                    'temperature': temperature,
                    'min_p': min_p,
                    'top_p': top_p,
                    'repetition_penalty': repetition_penalty,
                    'use_vader': use_vader
                }
                
                # Prepare quality parameters
                quality_params = {
                    'sentiment_smoothing': sentiment_smoothing,
                    'smoothing_window': int(smoothing_window),
                    'smoothing_method': smoothing_method
                }
                
                # Prepare config parameters
                config_params = {
                    'vader_exag_sensitivity': vader_exag_sens,
                    'vader_cfg_sensitivity': vader_cfg_sens,
                    'vader_temp_sensitivity': vader_temp_sens
                }
                
                prepare_state['progress'] = 50
                prepare_state['status'] = '🔬 Generating enriched chunks with metadata...'
                
                # Generate enriched chunks
                enriched_chunks = generate_enriched_chunks(
                    text_path,
                    book_output_dir,
                    user_tts_params,
                    quality_params,
                    config_params
                )
                
                prepare_state['progress'] = 90
                prepare_state['status'] = '💾 Saving JSON metadata...'
                
                json_path = book_output_dir / "chunks_info.json"
                prepare_state['generated_chunks'] = len(enriched_chunks)
                prepare_state['output_path'] = str(json_path)
                
                prepare_state['progress'] = 100
                prepare_state['status'] = '✅ Text preparation completed successfully!'
                
            except Exception as e:
                prepare_state['progress'] = 0
                prepare_state['status'] = f'❌ Preparation error: {str(e)}'
                prepare_state['generated_chunks'] = 0
                prepare_state['output_path'] = None
            finally:
                prepare_state['preparation_running'] = False
        
        # Start worker thread
        threading.Thread(target=preparation_worker, daemon=True).start()
        
        return (
            "📝 Starting text preparation with VADER analysis...",
            10,
            f"Processing: {selected_file['name']}",
            "Preparation started"
        )
        
    except Exception as e:
        prepare_state['preparation_running'] = False
        return f"❌ Error starting preparation: {str(e)}", 0, "Preparation failed", "Error"

def get_preparation_status():
    """Get current preparation status"""
    if prepare_state['generated_chunks'] > 0:
        chunk_info = f" ({prepare_state['generated_chunks']} chunks generated)"
        output_info = f"JSON saved: {prepare_state['output_path']}" if prepare_state['output_path'] else "Processing..."
    else:
        chunk_info = ""
        output_info = "No output yet" if prepare_state['preparation_running'] else "Ready for text preparation"
    
    return (
        prepare_state.get('status', 'Ready') + chunk_info,
        prepare_state.get('progress', 0),
        output_info,
        "Processing..." if prepare_state['preparation_running'] else "Ready"
    )

def stop_text_preparation():
    """Stop current preparation (if possible)"""
    if prepare_state['preparation_running']:
        prepare_state['preparation_running'] = False
        prepare_state['status'] = '⏹️ Preparation stopped by user'
        prepare_state['progress'] = 0
        return "⏹️ Preparation stopped", 0, "Preparation stopped", "Ready"
    else:
        return "No preparation to stop", prepare_state.get('progress', 0), prepare_state.get('status', 'Ready'), "Ready"

def create_prepare_text_tab():
    """Create Tab 5: Prepare Text with all GUI functionality"""
    
    with gr.Column():
        gr.Markdown("# 📝 Prepare Text for Processing")
        gr.Markdown("*Text file preparation with VADER sentiment analysis and chunking - matches GUI Tab 5*")
        
        if not PREPARE_TEXT_AVAILABLE:
            gr.Markdown("### ❌ Text Preparation Not Available")
            gr.Markdown("Missing required backend modules. Please ensure modules/tts_engine.py is available.")
            return {}
        
        # Important guidance note
        gr.Markdown("""
        ### 💡 **Important Usage Information**
        
        This tool prepares text files for TTS conversion by:
        - **Chunking**: Breaking text into optimal segments for TTS processing
        - **VADER Analysis**: Applying sentiment analysis to adjust TTS parameters per chunk
        - **JSON Generation**: Creating metadata files ready for audiobook generation
        
        **Configure your parameters below, then select and process your text file.**
        """)
        
        # Text File Selection Section
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📄 Text File Selection")
                
                text_files = get_available_text_files()
                text_choices = ["-- Select Text File --"] + [tf['display'] for tf in text_files]
                
                text_file_selector = gr.Dropdown(
                    label="Text File to Prepare",
                    choices=text_choices,
                    value="-- Select Text File --",
                    interactive=True,
                    info="Select text file from Text_Input directory for preparation"
                )
                
                # Manual path input
                text_manual_path = gr.Textbox(
                    label="Or Enter Text File Path Manually",
                    placeholder="e.g., /path/to/book.txt",
                    interactive=True,
                    info="Direct path to text file"
                )
                
                refresh_files_btn = gr.Button(
                    "🔄 Refresh File List",
                    variant="secondary",
                    size="sm"
                )
            
            with gr.Column(scale=1):
                text_file_info = gr.Markdown(
                    "No text file selected",
                    label="File Information"
                )
        
        # TTS Base Parameters Section
        with gr.Column():
            gr.Markdown("### ⚙️ Base TTS Parameters")
            gr.Markdown("*These parameters will be used as the baseline, with VADER adjustments applied per chunk*")
            
            with gr.Row():
                use_vader_check = gr.Checkbox(
                    label="Enable VADER Sentiment Analysis",
                    value=True,
                    info="Apply sentiment-based TTS parameter adjustments"
                )
            
            with gr.Row():
                exaggeration_param = gr.Slider(
                    label="Base Exaggeration",
                    minimum=0.0, maximum=2.0, step=0.1,
                    value=BASE_EXAGGERATION,
                    interactive=True,
                    info="Base speech exaggeration level"
                )
                
                cfg_weight_param = gr.Slider(
                    label="Base CFG Weight",
                    minimum=0.0, maximum=1.0, step=0.1,
                    value=BASE_CFG_WEIGHT,
                    interactive=True,
                    info="Base CFG guidance strength"
                )
                
                temperature_param = gr.Slider(
                    label="Base Temperature",
                    minimum=0.0, maximum=2.0, step=0.1,
                    value=BASE_TEMPERATURE,
                    interactive=True,
                    info="Base TTS randomness/creativity"
                )
            
            with gr.Row():
                min_p_param = gr.Slider(
                    label="Min P",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=DEFAULT_MIN_P,
                    interactive=True,
                    info="Minimum probability threshold"
                )
                
                top_p_param = gr.Slider(
                    label="Top P",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=DEFAULT_TOP_P,
                    interactive=True,
                    info="Nucleus sampling parameter"
                )
                
                repetition_penalty_param = gr.Slider(
                    label="Repetition Penalty",
                    minimum=0.5, maximum=2.0, step=0.1,
                    value=DEFAULT_REPETITION_PENALTY,
                    interactive=True,
                    info="Penalty for repetitive speech"
                )
        
        # Sentiment Processing Section
        with gr.Column():
            gr.Markdown("### 🎭 Sentiment Analysis Settings")
            
            with gr.Row():
                sentiment_smoothing_check = gr.Checkbox(
                    label="Enable Sentiment Smoothing",
                    value=ENABLE_SENTIMENT_SMOOTHING,
                    info="Smooth sentiment scores across adjacent chunks"
                )
                
                smoothing_window_param = gr.Slider(
                    label="Smoothing Window",
                    minimum=1, maximum=10, step=1,
                    value=SENTIMENT_SMOOTHING_WINDOW,
                    interactive=True,
                    info="Number of chunks to include in smoothing"
                )
                
                smoothing_method_param = gr.Dropdown(
                    label="Smoothing Method",
                    choices=["gaussian", "moving_average", "exponential"],
                    value=SENTIMENT_SMOOTHING_METHOD,
                    interactive=True,
                    info="Algorithm for sentiment smoothing"
                )
        
        # VADER Sensitivity Section
        with gr.Column():
            gr.Markdown("### 🎚️ VADER Sensitivity Settings")
            gr.Markdown("*Control how much sentiment analysis affects TTS parameters*")
            
            with gr.Row():
                vader_exag_sens_param = gr.Slider(
                    label="Exaggeration Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_EXAGGERATION_SENSITIVITY,
                    interactive=True,
                    info="How much sentiment affects exaggeration"
                )
                
                vader_cfg_sens_param = gr.Slider(
                    label="CFG Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_CFG_WEIGHT_SENSITIVITY,
                    interactive=True,
                    info="How much sentiment affects CFG weight"
                )
                
                vader_temp_sens_param = gr.Slider(
                    label="Temperature Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_TEMPERATURE_SENSITIVITY,
                    interactive=True,
                    info="How much sentiment affects temperature"
                )
        
        # Preparation Controls
        with gr.Row():
            prepare_btn = gr.Button(
                "📝 Prepare Text for Chunking",
                variant="primary",
                size="lg",
                interactive=True
            )
            
            stop_btn = gr.Button(
                "⏹️ Stop Preparation",
                variant="secondary",
                size="lg",
                interactive=True
            )
        
        # Progress and Status
        with gr.Row():
            with gr.Column(scale=2):
                preparation_status = gr.Textbox(
                    label="Preparation Status",
                    value="Ready for text preparation",
                    interactive=False,
                    lines=2
                )
                
                progress_bar = gr.Slider(
                    label="Progress %",
                    minimum=0, maximum=100, step=1,
                    value=0,
                    interactive=False,
                    info="Preparation progress"
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
        
        # Output Information
        with gr.Column():
            gr.Markdown("### 📁 Generated Output")
            
            output_info = gr.Textbox(
                label="Generated JSON File",
                value="No output generated yet",
                interactive=False,
                info="Location of generated chunks_info.json file"
            )
            
            with gr.Row():
                refresh_status_btn = gr.Button(
                    "🔄 Refresh Status",
                    variant="secondary",
                    size="sm"
                )
                
                next_steps_btn = gr.Button(
                    "➡️ Next Steps Guide",
                    variant="secondary",
                    size="sm"
                )
            
            next_steps_info = gr.Markdown(
                "*After preparation completes, use Tab 1 (Convert Book) or Tab 8 (JSON Generate) to create the audiobook.*",
                visible=False
            )
    
    # Event Handlers
    def refresh_file_list():
        """Refresh text files list"""
        text_files = get_available_text_files()
        choices = ["-- Select Text File --"] + [tf['display'] for tf in text_files]
        return gr.update(choices=choices, value="-- Select Text File --")
    
    def show_next_steps():
        """Show next steps information"""
        return """## 📋 Next Steps After Text Preparation

**Your text has been prepared and is ready for audiobook generation!**

### Option 1: Use Tab 1 (Convert Book) - **Recommended**
1. Go to **Tab 1: Convert Book**
2. Select your prepared book from the dropdown
3. Choose a voice sample
4. Click "Generate Audiobook" for full processing

### Option 2: Use Tab 8 (JSON Generate) - **Advanced**
1. Go to **Tab 8: JSON Generate** 
2. Select the generated JSON file
3. Choose a voice sample
4. Generate audiobook directly from JSON

### Files Created:
- **JSON Chunks**: `Audiobook/[BookName]/TTS/text_chunks/chunks_info.json`
- **Metadata**: Includes sentiment analysis and TTS parameters per chunk
- **Ready**: For immediate audiobook generation

### Benefits of Preparation:
- ✅ **VADER Analysis**: Sentiment-based TTS parameter adjustment
- ✅ **Optimized Chunks**: Smart text segmentation for better TTS
- ✅ **Metadata Rich**: Each chunk has custom TTS parameters
- ✅ **Faster Generation**: Skip text processing in future runs
"""
    
    # Connect event handlers
    refresh_files_btn.click(
        refresh_file_list,
        inputs=[],
        outputs=[text_file_selector]
    )
    
    text_file_selector.change(
        load_text_file_info,
        inputs=[text_file_selector],
        outputs=[text_file_info, current_file_display]
    )
    
    prepare_btn.click(
        start_text_preparation,
        inputs=[
            text_file_selector, 
            use_vader_check, exaggeration_param, cfg_weight_param, temperature_param,
            min_p_param, top_p_param, repetition_penalty_param,
            sentiment_smoothing_check, smoothing_window_param, smoothing_method_param,
            vader_exag_sens_param, vader_cfg_sens_param, vader_temp_sens_param
        ],
        outputs=[preparation_status, progress_bar, output_info, operation_status]
    )
    
    stop_btn.click(
        stop_text_preparation,
        inputs=[],
        outputs=[preparation_status, progress_bar, output_info, operation_status]
    )
    
    refresh_status_btn.click(
        get_preparation_status,
        inputs=[],
        outputs=[preparation_status, progress_bar, output_info, operation_status]
    )
    
    next_steps_btn.click(
        show_next_steps,
        inputs=[],
        outputs=[next_steps_info]
    ).then(
        lambda: gr.update(visible=True),
        outputs=[next_steps_info]
    )
    
    return {
        'file_selector': text_file_selector,
        'prepare_button': prepare_btn,
        'status_display': preparation_status
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_prepare_text_tab()
    
    demo.launch()