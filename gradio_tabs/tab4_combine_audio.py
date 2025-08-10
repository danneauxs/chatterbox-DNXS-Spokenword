#!/usr/bin/env python3
"""
Gradio Tab 4: Combine Audio
Combine processed audio chunks into final audiobook - matches PyQt5 GUI Tab 4 functionality
"""

import gradio as gr
import os
import sys
import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Import backend functionality
try:
    from tools.combine_only import combine_audio_for_book
    from modules.file_manager import get_audio_files_in_directory
    from modules.audio_processor import get_wav_duration
    COMBINE_AVAILABLE = True
    print("✅ Audio combine functionality available")
except ImportError as e:
    print(f"⚠️  Combine functionality not available: {e}")
    COMBINE_AVAILABLE = False

# Global state for combine operations
combine_state = {
    'running': False,
    'progress': 0,
    'status': 'Ready',
    'thread': None,
    'current_book': None
}

def get_available_books():
    """Get list of books with audio chunks available for combining"""
    books = []
    
    # Look in Audiobook directory for processed books
    audiobook_root = Path("Audiobook")
    if audiobook_root.exists():
        for book_dir in audiobook_root.iterdir():
            if book_dir.is_dir():
                # Check for TTS/audio_chunks directory
                audio_chunks_dir = book_dir / "TTS" / "audio_chunks"
                if audio_chunks_dir.exists():
                    chunk_files = list(audio_chunks_dir.glob("chunk_*.wav"))
                    if chunk_files:
                        # Get basic info about the chunks
                        chunk_count = len(chunk_files)
                        try:
                            total_duration = sum(get_wav_duration(chunk) for chunk in chunk_files)
                            duration_str = f"{int(total_duration//3600):02d}:{int((total_duration%3600)//60):02d}:{int(total_duration%60):02d}"
                        except:
                            duration_str = "Unknown"
                        
                        books.append({
                            'name': book_dir.name,
                            'path': str(book_dir),
                            'chunk_count': chunk_count,
                            'duration': duration_str,
                            'status': 'Ready to combine'
                        })
    
    return sorted(books, key=lambda x: x['name'])

def get_book_info(book_path_str):
    """Get detailed information about a book's audio chunks"""
    if not book_path_str:
        return "No book selected"
    
    try:
        book_path = Path(book_path_str)
        audio_chunks_dir = book_path / "TTS" / "audio_chunks"
        
        if not audio_chunks_dir.exists():
            return f"❌ No audio chunks found in {book_path.name}"
        
        chunk_files = get_audio_files_in_directory(audio_chunks_dir)
        if not chunk_files:
            return f"❌ No valid chunk files found in {book_path.name}"
        
        # Calculate statistics
        total_chunks = len(chunk_files)
        try:
            total_duration = sum(get_wav_duration(chunk) for chunk in chunk_files)
            duration_str = f"{int(total_duration//3600):02d}:{int((total_duration%3600)//60):02d}:{int(total_duration%60):02d}"
            avg_duration = total_duration / total_chunks if total_chunks > 0 else 0
        except Exception as e:
            duration_str = "Error calculating"
            avg_duration = 0
        
        # Check for existing combined files
        combined_wav = book_path / f"{book_path.name}_combined.wav"
        combined_m4b = book_path / f"{book_path.name}_combined.m4b"
        
        existing_files = []
        if combined_wav.exists():
            size_mb = combined_wav.stat().st_size / (1024 * 1024)
            existing_files.append(f"WAV: {size_mb:.1f}MB")
        if combined_m4b.exists():
            size_mb = combined_m4b.stat().st_size / (1024 * 1024)
            existing_files.append(f"M4B: {size_mb:.1f}MB")
        
        info = f"""📊 **Book Analysis: {book_path.name}**

**Audio Chunks:**
• Total Chunks: {total_chunks}
• Total Duration: {duration_str}
• Average Chunk: {avg_duration:.1f}s
• Location: {audio_chunks_dir}

**Existing Combined Files:**
{f"• {', '.join(existing_files)}" if existing_files else "• None found"}

**Status:** Ready for combining"""
        
        return info
        
    except Exception as e:
        return f"❌ Error analyzing book: {str(e)}"

def run_combine_operation(book_path_str, voice_name=None):
    """Run the audio combine operation"""
    try:
        if not COMBINE_AVAILABLE:
            return {'success': False, 'error': 'Combine functionality not available'}
        
        print(f"🔗 Starting combine operation for: {book_path_str}")
        
        # Update combine state
        combine_state['running'] = True
        combine_state['progress'] = 10
        combine_state['status'] = 'Starting combine operation...'
        combine_state['current_book'] = Path(book_path_str).name
        
        # Run the actual combine operation
        result = combine_audio_for_book(book_path_str, voice_name)
        
        combine_state['progress'] = 100
        combine_state['status'] = '✅ Combine completed successfully!' if result else '❌ Combine failed'
        
        return {'success': result, 'message': 'Audio chunks combined successfully!' if result else 'Combine operation failed'}
        
    except Exception as e:
        print(f"❌ Combine operation failed: {e}")
        combine_state['status'] = f'❌ Error: {str(e)}'
        combine_state['progress'] = 0
        return {'success': False, 'error': str(e)}
    finally:
        combine_state['running'] = False

def create_combine_audio_tab():
    """Create Tab 4: Combine Audio with all GUI functionality"""
    
    with gr.Column():
        gr.Markdown("# 🔗 Combine Audio Chunks")
        gr.Markdown("*Combine processed audio chunks into final audiobook - matches GUI Tab 4*")
        
        # Important note
        gr.Markdown("""
        ### 📁 **Important Note**
        Select the main book folder (e.g., 'Audiobook/BookName'), NOT the TTS or audio_chunks subfolder.
        This tool combines existing audio chunks that have already been generated by the TTS process.
        """)
        
        # Book Selection Section
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📚 Select Book to Combine")
                
                # Available books dropdown
                available_books = get_available_books()
                book_choices = [f"{book['name']} ({book['chunk_count']} chunks, {book['duration']})" 
                               for book in available_books]
                book_paths = {f"{book['name']} ({book['chunk_count']} chunks, {book['duration']})": book['path'] 
                             for book in available_books}
                
                book_selector = gr.Dropdown(
                    label="Available Books with Audio Chunks",
                    choices=book_choices,
                    value=book_choices[0] if book_choices else None,
                    interactive=True,
                    info="Books with processed audio chunks ready for combining"
                )
                
                # Manual path input (for advanced users)
                manual_path_input = gr.Textbox(
                    label="Or Enter Book Path Manually",
                    placeholder="e.g., /path/to/Audiobook/BookName",
                    interactive=True,
                    info="Full path to book folder containing TTS/audio_chunks"
                )
                
                # Refresh books button
                refresh_books_btn = gr.Button(
                    "🔄 Refresh Book List",
                    variant="secondary",
                    size="sm"
                )
            
            with gr.Column(scale=1):
                # Book information display
                book_info_display = gr.Markdown(
                    "Select a book to see detailed information",
                    label="Book Information"
                )
        
        # Optional Voice Name
        with gr.Row():
            voice_name_input = gr.Textbox(
                label="Voice Name (Optional)",
                placeholder="e.g., NarratorName",
                info="Used for output filename. If empty, uses '_combined' suffix",
                interactive=True
            )
        
        # Action Buttons
        with gr.Row():
            combine_btn = gr.Button(
                "🔗 Combine Audio Chunks",
                variant="primary",
                size="lg",
                interactive=True
            )
            
            stop_btn = gr.Button(
                "⏹️ Stop Operation",
                variant="secondary",
                size="lg",
                interactive=False
            )
        
        # Status and Progress
        with gr.Row():
            with gr.Column(scale=2):
                status_display = gr.Textbox(
                    label="Operation Status",
                    value="Ready to combine audio chunks",
                    interactive=False,
                    lines=2
                )
                
                progress_display = gr.Number(
                    label="Progress %",
                    value=0,
                    interactive=False,
                    precision=0
                )
            
            with gr.Column(scale=1):
                # Operation details
                current_book_display = gr.Textbox(
                    label="Current Book",
                    value="--",
                    interactive=False
                )
                
                operation_time_display = gr.Textbox(
                    label="Operation Time",
                    value="--:--:--",
                    interactive=False
                )
        
        # Output Files Section
        with gr.Column():
            gr.Markdown("### 📁 Generated Files")
            output_files_display = gr.Markdown(
                "No files generated yet",
                label="Output Files"
            )
    
    # Event Handlers
    def update_book_info(selected_book):
        """Update book information when selection changes"""
        if selected_book and selected_book in book_paths:
            book_path = book_paths[selected_book]
            info = get_book_info(book_path)
            return info
        return "No book selected"
    
    def refresh_book_list():
        """Refresh the list of available books"""
        books = get_available_books()
        choices = [f"{book['name']} ({book['chunk_count']} chunks, {book['duration']})" 
                   for book in books]
        paths = {f"{book['name']} ({book['chunk_count']} chunks, {book['duration']})": book['path'] 
                 for book in books}
        
        # Update global book_paths
        nonlocal book_paths
        book_paths = paths
        
        return gr.update(choices=choices, value=choices[0] if choices else None)
    
    def get_selected_book_path(selected_book, manual_path):
        """Get the actual book path from selection or manual input"""
        if manual_path.strip():
            return manual_path.strip()
        elif selected_book and selected_book in book_paths:
            return book_paths[selected_book]
        return None
    
    def start_combine_operation(selected_book, manual_path, voice_name):
        """Start the combine operation"""
        # Validation
        book_path = get_selected_book_path(selected_book, manual_path)
        if not book_path:
            return (
                "❌ Please select a book or enter a manual path",
                0,
                "Error",
                "--:--:--",
                "No files generated",
                gr.update(interactive=False),
                gr.update(interactive=True)
            )
        
        # Check if already running
        if combine_state['running']:
            return (
                "⚠️ Combine operation already in progress",
                combine_state['progress'],
                combine_state.get('current_book', '--'),
                "--:--:--",
                "Operation in progress...",
                gr.update(interactive=False),
                gr.update(interactive=True)
            )
        
        try:
            # Start combine operation in background thread
            def run_combine_thread():
                start_time = time.time()
                try:
                    result = run_combine_operation(book_path, voice_name.strip() or None)
                    elapsed = time.time() - start_time
                    combine_state['elapsed'] = elapsed
                    
                    if result['success']:
                        combine_state['status'] = '✅ Audio combining completed successfully!'
                        
                        # Find generated files
                        book_path_obj = Path(book_path)
                        suffix = f" [{voice_name.strip()}]" if voice_name.strip() else "_combined"
                        
                        generated_files = []
                        wav_file = book_path_obj / f"{book_path_obj.name}{suffix}.wav"
                        m4b_file = book_path_obj / f"{book_path_obj.name}{suffix}.m4b"
                        
                        if wav_file.exists():
                            size_mb = wav_file.stat().st_size / (1024 * 1024)
                            generated_files.append(f"**WAV**: {wav_file.name} ({size_mb:.1f}MB)")
                        
                        if m4b_file.exists():
                            size_mb = m4b_file.stat().st_size / (1024 * 1024)
                            generated_files.append(f"**M4B**: {m4b_file.name} ({size_mb:.1f}MB)")
                        
                        combine_state['generated_files'] = "\n".join(generated_files) if generated_files else "No files found"
                    else:
                        combine_state['status'] = f"❌ Combine failed: {result.get('error', 'Unknown error')}"
                        combine_state['generated_files'] = "No files generated due to error"
                        
                except Exception as e:
                    combine_state['status'] = f"❌ Error: {str(e)}"
                    combine_state['generated_files'] = "No files generated due to error"
                finally:
                    combine_state['running'] = False
            
            # Start thread
            thread = threading.Thread(target=run_combine_thread)
            thread.start()
            combine_state['thread'] = thread
            
            return (
                "🚀 Starting combine operation...",
                5,  # Initial progress
                Path(book_path).name,
                "00:00:00",
                "Starting operation...",
                gr.update(interactive=False),  # Disable combine button
                gr.update(interactive=True)    # Enable stop button
            )
            
        except Exception as e:
            return (
                f"❌ Error starting combine: {str(e)}",
                0,
                "Error",
                "--:--:--",
                "No files generated",
                gr.update(interactive=True),
                gr.update(interactive=False)
            )
    
    def stop_combine_operation():
        """Stop the current combine operation"""
        if combine_state['running']:
            combine_state['running'] = False
            combine_state['status'] = '⏹️ Operation stopped by user'
            combine_state['progress'] = 0
            
            return (
                "⏹️ Operation stopped by user",
                0,
                "--",
                "--:--:--",
                "Operation stopped",
                gr.update(interactive=True),   # Enable combine button
                gr.update(interactive=False)   # Disable stop button
            )
        else:
            return (
                "No operation to stop",
                combine_state.get('progress', 0),
                combine_state.get('current_book', '--'),
                "--:--:--",
                combine_state.get('generated_files', 'No files generated'),
                gr.update(interactive=True),
                gr.update(interactive=False)
            )
    
    def get_current_status():
        """Get current operation status for periodic updates"""
        if combine_state['running']:
            elapsed = time.time() - combine_state.get('start_time', time.time())
            elapsed_str = f"{int(elapsed//3600):02d}:{int((elapsed%3600)//60):02d}:{int(elapsed%60):02d}"
            
            return (
                combine_state.get('status', 'Processing...'),
                combine_state.get('progress', 0),
                combine_state.get('current_book', '--'),
                elapsed_str,
                combine_state.get('generated_files', 'Processing...'),
                gr.update(interactive=False),
                gr.update(interactive=True)
            )
        else:
            # Operation completed or not running
            elapsed = combine_state.get('elapsed', 0)
            elapsed_str = f"{int(elapsed//3600):02d}:{int((elapsed%3600)//60):02d}:{int(elapsed%60):02d}" if elapsed > 0 else "--:--:--"
            
            return (
                combine_state.get('status', 'Ready'),
                combine_state.get('progress', 0),
                combine_state.get('current_book', '--'),
                elapsed_str,
                combine_state.get('generated_files', 'No files generated'),
                gr.update(interactive=True),
                gr.update(interactive=False)
            )
    
    # Connect event handlers
    book_selector.change(
        update_book_info,
        inputs=[book_selector],
        outputs=[book_info_display]
    )
    
    refresh_books_btn.click(
        refresh_book_list,
        inputs=[],
        outputs=[book_selector]
    )
    
    combine_btn.click(
        start_combine_operation,
        inputs=[book_selector, manual_path_input, voice_name_input],
        outputs=[
            status_display, progress_display, current_book_display,
            operation_time_display, output_files_display,
            combine_btn, stop_btn
        ]
    )
    
    stop_btn.click(
        stop_combine_operation,
        inputs=[],
        outputs=[
            status_display, progress_display, current_book_display,
            operation_time_display, output_files_display,
            combine_btn, stop_btn
        ]
    )
    
    # Status refresh button
    with gr.Row():
        refresh_status_btn = gr.Button("🔄 Refresh Status", size="sm", variant="secondary")
    
    refresh_status_btn.click(
        get_current_status,
        inputs=[],
        outputs=[
            status_display, progress_display, current_book_display,
            operation_time_display, output_files_display,
            combine_btn, stop_btn
        ]
    )
    
    return {
        'combine_button': combine_btn,
        'status_display': status_display,
        'progress': progress_display
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_combine_audio_tab()
    
    demo.launch()