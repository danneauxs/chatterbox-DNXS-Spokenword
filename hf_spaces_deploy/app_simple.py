#!/usr/bin/env python3
"""
Simplified Gradio Interface for ChatterboxTTS Audiobook Pipeline
HuggingFace Spaces Deployment with Dependency Error Handling
"""

import gradio as gr
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_demo_interface():
    """Create a demo interface that explains the deployment status"""
    
    # Check what's available
    dependencies_status = []
    
    try:
        import torch
        dependencies_status.append("✅ PyTorch available")
        if torch.cuda.is_available():
            dependencies_status.append(f"✅ CUDA available (GPU: {torch.cuda.get_device_name()})")
        else:
            dependencies_status.append("⚠️ CUDA not available (CPU mode)")
    except ImportError:
        dependencies_status.append("❌ PyTorch not available")
    
    try:
        import transformers
        dependencies_status.append("✅ Transformers available")
    except ImportError:
        dependencies_status.append("❌ Transformers not available")
    
    try:
        import librosa
        dependencies_status.append("✅ Librosa available")
    except ImportError:
        dependencies_status.append("❌ Librosa not available")
    
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        dependencies_status.append("✅ VADER Sentiment available")
    except ImportError:
        dependencies_status.append("❌ VADER Sentiment not available")
    
    # Try to import ChatterboxTTS
    chatterbox_status = "❌ ChatterboxTTS not available"
    error_details = ""
    try:
        from src.chatterbox.tts import ChatterboxTTS
        chatterbox_status = "✅ ChatterboxTTS available"
    except ImportError as e:
        error_details = f"Import error: {str(e)}"
    except Exception as e:
        error_details = f"Other error: {str(e)}"
    
    status_report = "\n".join(dependencies_status + [chatterbox_status])
    if error_details:
        status_report += f"\n\nError details:\n{error_details}"
    
    def show_status():
        return status_report
    
    def placeholder_generate(text_file, voice_sample):
        if chatterbox_status.startswith("✅"):
            return None, "🚧 ChatterboxTTS is available but full pipeline needs additional setup"
        else:
            return None, f"❌ Cannot generate audio: ChatterboxTTS not properly loaded\n\n{error_details}"
    
    with gr.Blocks(title="ChatterboxTTS Status Check", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🎙️ ChatterboxTTS Audiobook Generator - Deployment Status
        
        This space is checking the availability of ChatterboxTTS and its dependencies.
        """)
        
        with gr.Row():
            with gr.Column():
                status_btn = gr.Button("🔍 Check System Status", variant="primary")
                status_output = gr.Textbox(
                    label="📋 System Status",
                    lines=15,
                    value=status_report
                )
            
            with gr.Column():
                gr.Markdown("### 🧪 Test Upload (Demo)")
                text_file = gr.File(
                    label="📖 Book Text File (.txt)",
                    file_types=[".txt"]
                )
                voice_sample = gr.Audio(
                    label="🎤 Voice Sample",
                    type="filepath"
                )
                test_btn = gr.Button("🧪 Test Generation", variant="secondary")
                test_output = gr.Textbox(
                    label="📄 Test Result",
                    lines=10
                )
        
        gr.Markdown("""
        ## 📚 About This Space
        
        This is a ChatterboxTTS audiobook generation system that:
        - Converts text to speech using voice cloning
        - Applies sentiment analysis for dynamic expression
        - Generates professional audiobooks with proper pacing
        
        **Current Status**: Checking dependencies and setup
        
        ## 🔧 Technical Details
        
        The system requires:
        - ChatterboxTTS neural TTS engine
        - Custom text processing modules
        - Audio processing pipeline
        - CUDA for GPU acceleration (optional)
        
        If you see errors above, the ChatterboxTTS package may need additional setup or dependencies.
        """)
        
        # Event handlers
        status_btn.click(fn=show_status, outputs=status_output)
        test_btn.click(
            fn=placeholder_generate,
            inputs=[text_file, voice_sample],
            outputs=[gr.Audio(label="Generated Audio"), test_output]
        )
    
    return interface

# Launch interface
if __name__ == "__main__":
    logger.info("🚀 Starting ChatterboxTTS status check interface...")
    
    interface = create_demo_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )