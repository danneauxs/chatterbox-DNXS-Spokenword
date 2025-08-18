#!/usr/bin/env python3
"""
Gradio Tab 7: Chunk Tools
Interactive chunk editing, search, and audio regeneration - matches PyQt5 GUI Tab 7 functionality
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
    from wrapper.chunk_loader import load_chunks, save_chunks
    from wrapper.chunk_search import search_chunks
    from wrapper.chunk_editor import update_chunk
    from wrapper.chunk_synthesizer import synthesize_chunk
    from wrapper.chunk_player import play_chunk_audio
    from wrapper.chunk_revisions import accept_revision
    from modules.voice_detector import get_likely_voices_for_book
    from config.config import *
    
    CHUNK_TOOLS_AVAILABLE = True
    print("✅ Chunk tools functionality available")
except ImportError as e:
    print(f"⚠️  Chunk tools functionality not available: {e}")
    CHUNK_TOOLS_AVAILABLE = False
    
    # Default values
    AUDIOBOOK_ROOT = 'Audiobook'
    
    # Define fallback functions if imports fail
    def load_chunks(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def save_chunks(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def search_chunks(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def update_chunk(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def play_chunk_audio(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def synthesize_chunk(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def accept_revision(*args, **kwargs):
        raise ImportError("Backend functionality not available")
    
    def get_likely_voices_for_book(*args, **kwargs):
        raise ImportError("Backend functionality not available")

# Global state for chunk operations
chunk_state = {
    'loaded_chunks': None,
    'current_chunk': None,
    'book_path': None,
    'audio_dir': None,
    'search_results': [],
    'voice_candidates': [],
    'selected_voice': None,
    'operation_running': False
}

def get_available_repair_books():
    """Get list of books available for chunk repair/editing"""
    books = []
    
    if not CHUNK_TOOLS_AVAILABLE:
        return books
    
    # Check TTS processing directories first
    audiobook_root = Path(AUDIOBOOK_ROOT)
    if audiobook_root.exists():
        for book_dir in audiobook_root.iterdir():
            if book_dir.is_dir():
                tts_chunks_dir = book_dir / "TTS" / "text_chunks"
                json_path = tts_chunks_dir / "chunks_info.json"
                if json_path.exists():
                    chunk_count = 0
                    try:
                        with open(json_path, 'r') as f:
                            chunks_data = json.load(f)
                            chunk_count = len(chunks_data)
                    except:
                        pass
                    
                    books.append({
                        'name': book_dir.name,
                        'path': str(json_path),
                        'source': 'TTS',
                        'chunk_count': chunk_count,
                        'display': f"{book_dir.name} (TTS: {chunk_count} chunks)"
                    })
    
    # Check Text_Input directory for fallback
    text_input_dir = Path("Text_Input")
    if text_input_dir.exists():
        for chunk_file in text_input_dir.glob("*_chunks.json"):
            book_name = chunk_file.stem.replace("_chunks", "")
            # Only add if not already found in TTS directories
            if not any(book['name'] == book_name for book in books):
                chunk_count = 0
                try:
                    with open(chunk_file, 'r') as f:
                        chunks_data = json.load(f)
                        chunk_count = len(chunks_data)
                except:
                    pass
                
                books.append({
                    'name': book_name,
                    'path': str(chunk_file),
                    'source': 'Text_Input',
                    'chunk_count': chunk_count,
                    'display': f"{book_name} (Text_Input: {chunk_count} chunks)"
                })
    
    return sorted(books, key=lambda x: x['name'])

def load_book_chunks(book_selection):
    """Load chunks for selected book"""
    if not book_selection or book_selection == "-- Select a Book --":
        chunk_state['loaded_chunks'] = None
        chunk_state['current_chunk'] = None
        chunk_state['book_path'] = None
        chunk_state['audio_dir'] = None
        chunk_state['voice_candidates'] = []
        return (
            "No book selected",
            "",  # Clear search
            "No chunks loaded",
            "",  # Clear chunk text
            "none",  # Reset boundary
            0.5, 0.5, 0.8,  # Reset TTS params
            "No chunk selected",
            "No voice detected",
            ["-- Please Select Voice --"]
        )
    
    try:
        # Find the book data
        books = get_available_repair_books()
        selected_book = None
        for book in books:
            if book['display'] == book_selection:
                selected_book = book
                break
        
        if not selected_book:
            return (
                "❌ Selected book not found",
                "", "No chunks loaded", "", "none", 0.5, 0.5, 0.8,
                "No chunk selected", "No voice detected", ["-- Please Select Voice --"]
            )
        
        # Load chunks
        chunks = load_chunks(selected_book['path'])
        
        # Ensure chunks have index fields
        for i, chunk in enumerate(chunks):
            if 'index' not in chunk:
                chunk['index'] = i
        
        chunk_state['loaded_chunks'] = chunks
        chunk_state['book_path'] = Path(selected_book['path'])
        chunk_state['current_chunk'] = None
        chunk_state['search_results'] = []
        
        # Determine audio directory
        audiobook_root = Path(AUDIOBOOK_ROOT)
        chunk_state['audio_dir'] = audiobook_root / selected_book['name'] / "TTS" / "audio_chunks"
        
        # Detect voice candidates
        try:
            likely_voices = get_likely_voices_for_book(selected_book['name'], chunk_state['book_path'])
            chunk_state['voice_candidates'] = likely_voices
            
            voice_choices = ["-- Please Select Voice --"]
            voice_info = ""
            
            if likely_voices:
                for voice_name, voice_path, detection_method in likely_voices:
                    voice_choices.append(f"{voice_name} ({detection_method})")
                voice_info = f"✅ Found {len(likely_voices)} voice candidate(s). Please select voice before resynthesizing."
            else:
                voice_info = "❌ No voice candidates detected. Check JSON metadata or run.log."
                
        except Exception as e:
            voice_choices = ["-- Please Select Voice --"]
            voice_info = f"❌ Error detecting voices: {str(e)}"
            chunk_state['voice_candidates'] = []
        
        return (
            f"✅ Loaded {len(chunks)} chunks from {selected_book['name']}",
            "",  # Clear search
            "Chunks loaded successfully - use search to find specific chunks",
            "",  # Clear chunk text
            "none",  # Reset boundary
            0.5, 0.5, 0.8,  # Reset TTS params
            "No chunk selected - search and select a chunk to edit",
            voice_info,
            voice_choices
        )
        
    except Exception as e:
        return (
            f"❌ Error loading chunks: {str(e)}",
            "", "Failed to load chunks", "", "none", 0.5, 0.5, 0.8,
            "Error loading chunks", "No voice detected", ["-- Please Select Voice --"]
        )

def search_for_chunks(search_query):
    """Search for chunks containing the query text"""
    if not chunk_state['loaded_chunks']:
        return "❌ No chunks loaded - please select a book first", ""
    
    if not search_query.strip():
        return "❌ Please enter text to search for", ""
    
    try:
        results = search_chunks(chunk_state['loaded_chunks'], search_query.strip())
        chunk_state['search_results'] = results
        
        if results:
            # Format results for display
            results_text = f"**Found {len(results)} matching chunks:**\n\n"
            for chunk in results:
                text_preview = chunk['text'][:80] + "..." if len(chunk['text']) > 80 else chunk['text']
                results_text += f"**[{chunk['index']}]** {text_preview}\n\n"
            
            # Create dropdown choices
            choices = []
            for chunk in results:
                text_preview = chunk['text'][:60] + "..." if len(chunk['text']) > 60 else chunk['text']
                choices.append(f"[{chunk['index']}] {text_preview}")
            
            return results_text, gr.update(choices=choices, value=None, visible=True)
        else:
            return "No matching chunks found", gr.update(choices=[], visible=False)
            
    except Exception as e:
        return f"❌ Error searching chunks: {str(e)}", gr.update(choices=[], visible=False)

def select_chunk_for_editing(chunk_selection):
    """Select a chunk for editing from search results"""
    if not chunk_selection or not chunk_state['search_results']:
        return (
            "", "none", 0.5, 0.5, 0.8,
            "No chunk selected"
        )
    
    try:
        # Find the selected chunk by parsing the selection string
        chunk_index_str = chunk_selection.split(']')[0][1:]  # Extract index from "[123] text..."
        chunk_index = int(chunk_index_str)
        
        # Find the chunk with this index
        selected_chunk = None
        for chunk in chunk_state['search_results']:
            if chunk['index'] == chunk_index:
                selected_chunk = chunk
                break
        
        if not selected_chunk:
            return (
                "", "none", 0.5, 0.5, 0.8,
                "❌ Selected chunk not found"
            )
        
        chunk_state['current_chunk'] = selected_chunk
        
        # Extract chunk data
        text = selected_chunk.get('text', '')
        boundary_type = selected_chunk.get('boundary_type', 'none')
        
        # Extract TTS parameters
        tts_params = selected_chunk.get('tts_params', {})
        exaggeration = tts_params.get('exaggeration', 0.5)
        cfg_weight = tts_params.get('cfg_weight', 0.5)
        temperature = tts_params.get('temperature', 0.8)
        
        # Create info display
        sentiment = selected_chunk.get('sentiment_compound', selected_chunk.get('sentiment_score', 'N/A'))
        word_count = selected_chunk.get('word_count', 'N/A')
        
        info_text = f"""**Selected Chunk {chunk_index}**
**Boundary:** {boundary_type} | **Words:** {word_count} | **Sentiment:** {sentiment}
**TTS Params:** exag={exaggeration}, cfg={cfg_weight}, temp={temperature}
**Audio File:** chunk_{chunk_index+1:05d}.wav"""
        
        return (
            text,
            boundary_type,
            exaggeration,
            cfg_weight, 
            temperature,
            info_text
        )
        
    except Exception as e:
        return (
            "", "none", 0.5, 0.5, 0.8,
            f"❌ Error selecting chunk: {str(e)}"
        )

def save_chunk_changes(chunk_text, boundary_type, exaggeration, cfg_weight, temperature):
    """Save changes to the current chunk"""
    if not chunk_state['current_chunk']:
        return "❌ No chunk selected"
    
    try:
        # Update chunk data
        chunk_state['current_chunk']['text'] = chunk_text.strip()
        chunk_state['current_chunk']['boundary_type'] = boundary_type
        chunk_state['current_chunk']['tts_params'] = {
            'exaggeration': exaggeration,
            'cfg_weight': cfg_weight,
            'temperature': temperature
        }
        
        # Update word count
        word_count = len(chunk_text.strip().split())
        chunk_state['current_chunk']['word_count'] = word_count
        
        # Save to file
        if chunk_state['book_path']:
            save_chunks(chunk_state['loaded_chunks'], str(chunk_state['book_path']))
            return f"✅ Chunk {chunk_state['current_chunk']['index']} saved successfully!"
        else:
            return "❌ No book path available for saving"
            
    except Exception as e:
        return f"❌ Error saving chunk: {str(e)}"

def play_original_audio():
    """Play the original audio for the current chunk"""
    if not chunk_state['current_chunk'] or not chunk_state['audio_dir']:
        return "❌ No chunk selected or audio directory not found"
    
    try:
        chunk_index = chunk_state['current_chunk']['index']
        audio_file = chunk_state['audio_dir'] / f"chunk_{chunk_index+1:05d}.wav"
        
        if not audio_file.exists():
            return f"❌ Audio file not found: {audio_file.name}"
        
        # Play audio in background thread to avoid blocking UI
        def play_audio():
            try:
                play_chunk_audio(str(audio_file))
            except Exception as e:
                print(f"Error playing audio: {e}")
        
        threading.Thread(target=play_audio, daemon=True).start()
        return f"🔊 Playing original audio: {audio_file.name}"
        
    except Exception as e:
        return f"❌ Error playing audio: {str(e)}"

def resynthesize_chunk_audio(voice_selection, chunk_text, boundary_type, exaggeration, cfg_weight, temperature):
    """Regenerate audio for the current chunk with new parameters"""
    if not chunk_state['current_chunk']:
        return "❌ No chunk selected"
    
    if not voice_selection or voice_selection == "-- Please Select Voice --":
        return "❌ Please select a voice before resynthesizing"
    
    if chunk_state['operation_running']:
        return "⚠️ Another operation is already running"
    
    try:
        # Find selected voice info
        selected_voice_data = None
        for voice_name, voice_path, detection_method in chunk_state['voice_candidates']:
            if f"{voice_name} ({detection_method})" == voice_selection:
                selected_voice_data = (voice_name, voice_path, detection_method)
                break
        
        if not selected_voice_data:
            return "❌ Selected voice not found in candidates"
        
        voice_name, voice_path, detection_method = selected_voice_data
        
        # Update chunk with current parameters first
        chunk_state['current_chunk']['text'] = chunk_text.strip()
        chunk_state['current_chunk']['boundary_type'] = boundary_type
        chunk_state['current_chunk']['tts_params'] = {
            'exaggeration': exaggeration,
            'cfg_weight': cfg_weight,
            'temperature': temperature
        }
        
        # Start resynthesis in background
        def resynth_worker():
            chunk_state['operation_running'] = True
            try:
                chunk_index = chunk_state['current_chunk']['index']
                result = synthesize_chunk(
                    chunk_state['current_chunk'],
                    voice_path,
                    str(chunk_state['audio_dir']),
                    chunk_index
                )
                chunk_state['operation_running'] = False
                return result
            except Exception as e:
                chunk_state['operation_running'] = False
                print(f"Error in resynthesis: {e}")
                return False
        
        # Run in thread
        threading.Thread(target=resynth_worker, daemon=True).start()
        
        return f"🎤 Starting resynthesis with voice '{voice_name}'...\n⏳ This may take a few moments."
        
    except Exception as e:
        chunk_state['operation_running'] = False
        return f"❌ Error resynthesizing chunk: {str(e)}"

def play_revised_audio():
    """Play the revised audio for the current chunk"""
    if not chunk_state['current_chunk'] or not chunk_state['audio_dir']:
        return "❌ No chunk selected or audio directory not found"
    
    try:
        chunk_index = chunk_state['current_chunk']['index']
        # Look for revised audio file (typically has _revised suffix or similar)
        revised_file = chunk_state['audio_dir'] / f"chunk_{chunk_index+1:05d}_revised.wav"
        if not revised_file.exists():
            # Fallback to regular file if revised doesn't exist
            revised_file = chunk_state['audio_dir'] / f"chunk_{chunk_index+1:05d}.wav"
        
        if not revised_file.exists():
            return f"❌ Revised audio file not found: {revised_file.name}"
        
        def play_audio():
            try:
                play_chunk_audio(str(revised_file))
            except Exception as e:
                print(f"Error playing revised audio: {e}")
        
        threading.Thread(target=play_audio, daemon=True).start()
        return f"🔊 Playing revised audio: {revised_file.name}"
        
    except Exception as e:
        return f"❌ Error playing revised audio: {str(e)}"

def accept_chunk_revision():
    """Accept the current chunk revision"""
    if not chunk_state['current_chunk']:
        return "❌ No chunk selected"
    
    try:
        chunk_index = chunk_state['current_chunk']['index']
        result = accept_revision(chunk_index, str(chunk_state['audio_dir']))
        
        if result:
            return f"✅ Revision accepted for chunk {chunk_index}"
        else:
            return f"❌ Failed to accept revision for chunk {chunk_index}"
            
    except Exception as e:
        return f"❌ Error accepting revision: {str(e)}"

def create_chunk_tools_tab():
    """Create Tab 7: Chunk Tools with all GUI functionality"""
    
    with gr.Column():
        gr.Markdown("# 🔧 Chunk Repair and Editing Tool")
        gr.Markdown("*Interactive chunk editing, search, and audio regeneration - matches GUI Tab 7*")
        
        if not CHUNK_TOOLS_AVAILABLE:
            gr.Markdown("### ❌ Chunk Tools Not Available")
            gr.Markdown("Missing required backend modules. Please ensure all wrapper modules are installed.")
            return {}
        
        # Book Selection Section
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📚 Book Selection")
                
                available_books = get_available_repair_books()
                book_choices = ["-- Select a Book --"] + [book['display'] for book in available_books]
                
                book_selector = gr.Dropdown(
                    label="Select Book for Chunk Editing",
                    choices=book_choices,
                    value="-- Select a Book --",
                    interactive=True,
                    info="Books with processed chunks available for editing"
                )
                
                refresh_books_btn = gr.Button(
                    "🔄 Refresh Book List",
                    variant="secondary",
                    size="sm"
                )
                
                load_status = gr.Textbox(
                    label="Load Status",
                    value="No book selected",
                    interactive=False,
                    lines=2
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 🎤 Voice Selection")
                
                voice_info_display = gr.Markdown(
                    "No voice detected",
                    label="Voice Detection Status"
                )
                
                voice_selector = gr.Dropdown(
                    label="Select Voice for Resynthesis",
                    choices=["-- Please Select Voice --"],
                    value="-- Please Select Voice --",
                    interactive=True,
                    info="Detected voice candidates for this book"
                )
                
                refresh_voices_btn = gr.Button(
                    "🔄 Re-detect Voice Candidates",
                    variant="secondary",
                    size="sm"
                )
        
        # Search and Selection Section
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔍 Search and Select Chunks")
                
                search_input = gr.Textbox(
                    label="Search for Text Fragment",
                    placeholder="Enter text to search for in chunks...",
                    interactive=True,
                    info="Search through chunk text content"
                )
                
                search_btn = gr.Button(
                    "🔍 Search Chunks",
                    variant="primary",
                    size="lg"
                )
                
                search_results_display = gr.Markdown(
                    "No search performed yet",
                    label="Search Results"
                )
                
                chunk_selector = gr.Dropdown(
                    label="Select Chunk to Edit",
                    choices=[],
                    value=None,
                    interactive=True,
                    visible=False,
                    info="Choose chunk from search results"
                )
        
        # Chunk Editor Section
        with gr.Column():
            gr.Markdown("### ✏️ Edit Selected Chunk")
            
            chunk_info_display = gr.Markdown(
                "No chunk selected",
                label="Chunk Information"
            )
            
            # Text editing
            with gr.Row():
                chunk_text_editor = gr.Textbox(
                    label="Chunk Text",
                    placeholder="Select a chunk to edit its text...",
                    interactive=True,
                    lines=4,
                    info="Edit the text content of the selected chunk"
                )
            
            # Metadata and TTS Parameters
            with gr.Row():
                boundary_selector = gr.Dropdown(
                    label="Boundary Type",
                    choices=[
                        "none", "paragraph_end", "chapter_start", "chapter_end", "section_break",
                        "period", "comma", "semicolon", "colon", "question_mark", "exclamation",
                        "dash", "ellipsis", "quote_end"
                    ],
                    value="none",
                    interactive=True,
                    info="Chunk boundary classification"
                )
                
                exag_param = gr.Slider(
                    label="TTS Exaggeration",
                    minimum=0.0, maximum=3.0, step=0.1,
                    value=0.5,
                    interactive=True,
                    info="Speech exaggeration level"
                )
                
                cfg_param = gr.Slider(
                    label="TTS CFG Weight", 
                    minimum=0.0, maximum=2.0, step=0.1,
                    value=0.5,
                    interactive=True,
                    info="CFG guidance strength"
                )
                
                temp_param = gr.Slider(
                    label="TTS Temperature",
                    minimum=0.0, maximum=2.0, step=0.1,
                    value=0.8,
                    interactive=True,
                    info="TTS randomness/creativity"
                )
        
        # Action Buttons
        with gr.Row():
            play_original_btn = gr.Button(
                "🔊 Play Original",
                variant="secondary",
                size="lg",
                interactive=True
            )
            
            save_changes_btn = gr.Button(
                "💾 Save Changes",
                variant="primary", 
                size="lg",
                interactive=True
            )
            
            resynthesize_btn = gr.Button(
                "🎤 Resynthesize",
                variant="primary",
                size="lg", 
                interactive=True
            )
            
            play_revised_btn = gr.Button(
                "🔊 Play Revised",
                variant="secondary",
                size="lg",
                interactive=True
            )
            
            accept_revision_btn = gr.Button(
                "✅ Accept Revision", 
                variant="primary",
                size="lg",
                interactive=True
            )
        
        # Operation Status
        with gr.Row():
            operation_status = gr.Textbox(
                label="Operation Status",
                value="Ready for chunk editing operations",
                interactive=False,
                lines=2
            )
    
    # Event Handlers
    def refresh_book_list():
        """Refresh the available books list"""
        books = get_available_repair_books()
        choices = ["-- Select a Book --"] + [book['display'] for book in books]
        return gr.update(choices=choices, value="-- Select a Book --")
    
    def refresh_voice_candidates():
        """Refresh voice candidates for current book"""
        if chunk_state['book_path']:
            # Re-run voice detection
            try:
                book_name = chunk_state['book_path'].parent.parent.name if chunk_state['book_path'] else ""
                likely_voices = get_likely_voices_for_book(book_name, chunk_state['book_path'])
                chunk_state['voice_candidates'] = likely_voices
                
                voice_choices = ["-- Please Select Voice --"]
                voice_info = ""
                
                if likely_voices:
                    for voice_name, voice_path, detection_method in likely_voices:
                        voice_choices.append(f"{voice_name} ({detection_method})")
                    voice_info = f"✅ Found {len(likely_voices)} voice candidate(s). Please select voice before resynthesizing."
                else:
                    voice_info = "❌ No voice candidates detected. Check JSON metadata or run.log."
                
                return voice_info, gr.update(choices=voice_choices)
            except Exception as e:
                return f"❌ Error refreshing voices: {str(e)}", gr.update(choices=["-- Please Select Voice --"])
        else:
            return "No book selected - cannot refresh voice candidates", gr.update(choices=["-- Please Select Voice --"])
    
    # Connect event handlers
    refresh_books_btn.click(
        refresh_book_list,
        inputs=[],
        outputs=[book_selector]
    )
    
    book_selector.change(
        load_book_chunks,
        inputs=[book_selector],
        outputs=[
            load_status, search_input, search_results_display, chunk_text_editor,
            boundary_selector, exag_param, cfg_param, temp_param,
            chunk_info_display, voice_info_display, voice_selector
        ]
    )
    
    refresh_voices_btn.click(
        refresh_voice_candidates,
        inputs=[],
        outputs=[voice_info_display, voice_selector]
    )
    
    search_btn.click(
        search_for_chunks,
        inputs=[search_input],
        outputs=[search_results_display, chunk_selector]
    )
    
    search_input.submit(
        search_for_chunks,
        inputs=[search_input],
        outputs=[search_results_display, chunk_selector]
    )
    
    chunk_selector.change(
        select_chunk_for_editing,
        inputs=[chunk_selector],
        outputs=[
            chunk_text_editor, boundary_selector, exag_param, cfg_param,
            temp_param, chunk_info_display
        ]
    )
    
    save_changes_btn.click(
        save_chunk_changes,
        inputs=[chunk_text_editor, boundary_selector, exag_param, cfg_param, temp_param],
        outputs=[operation_status]
    )
    
    play_original_btn.click(
        play_original_audio,
        inputs=[],
        outputs=[operation_status]
    )
    
    resynthesize_btn.click(
        resynthesize_chunk_audio,
        inputs=[voice_selector, chunk_text_editor, boundary_selector, exag_param, cfg_param, temp_param],
        outputs=[operation_status]
    )
    
    play_revised_btn.click(
        play_revised_audio,
        inputs=[],
        outputs=[operation_status]
    )
    
    accept_revision_btn.click(
        accept_chunk_revision,
        inputs=[],
        outputs=[operation_status]
    )
    
    return {
        'book_selector': book_selector,
        'search_button': search_btn,
        'operation_status': operation_status
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_chunk_tools_tab()
    
    demo.launch()