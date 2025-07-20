#!/usr/bin/env python3
"""
Gradio Interface for ChatterboxTTS Audiobook Pipeline
HuggingFace Spaces Deployment
"""

import gradio as gr
import torch
import tempfile
import os
import json
import zipfile
from pathlib import Path
import logging
from datetime import datetime
import traceback

# Import your existing modules
from src.chatterbox.tts import ChatterboxTTS
from modules.text_processor import sentence_chunk_text, smart_punctuate, detect_content_boundaries
from modules.audio_processor import smart_audio_validation_memory, add_contextual_silence
from modules.file_manager import convert_to_m4b, add_metadata_to_m4b
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global TTS instance (load once for efficiency)
tts_model = None
sentiment_analyzer = SentimentIntensityAnalyzer()

def initialize_tts():
    """Initialize TTS model once at startup"""
    global tts_model
    if tts_model is None:
        try:
            logger.info("🔄 Loading ChatterboxTTS model...")
            
            # Check if running on HuggingFace Spaces (limited GPU memory)
            if "SPACE_ID" in os.environ:
                # HF Spaces optimization
                torch.backends.cudnn.benchmark = False
                if torch.cuda.is_available():
                    torch.cuda.set_per_process_memory_fraction(0.8)
            
            tts_model = ChatterboxTTS()
            logger.info("✅ TTS model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load TTS model: {e}")
            raise e
    return tts_model

def process_text_to_chunks(text_content, chunk_words=50):
    """Process text into chunks with metadata"""
    try:
        # Apply smart punctuation normalization
        normalized_text = smart_punctuate(text_content)
        
        # Generate chunks with boundaries
        chunks = sentence_chunk_text(
            normalized_text, 
            chunk_words=chunk_words,
            enable_boundary_detection=True
        )
        
        # Add sentiment analysis and TTS parameters
        enriched_chunks = []
        for i, chunk in enumerate(chunks):
            # Sentiment analysis
            sentiment = sentiment_analyzer.polarity_scores(chunk['text'])
            
            # Calculate dynamic TTS parameters based on sentiment
            base_exaggeration = 0.4
            base_cfg_weight = 0.5
            base_temperature = 0.9
            
            # Adjust parameters based on sentiment
            compound_score = sentiment['compound']
            if compound_score > 0.1:  # Positive
                exaggeration = min(base_exaggeration * 1.3, 2.0)
                temperature = min(base_temperature * 1.1, 5.0)
            elif compound_score < -0.1:  # Negative
                exaggeration = max(base_exaggeration * 0.8, 0.0)
                temperature = max(base_temperature * 0.9, 0.0)
            else:  # Neutral
                exaggeration = base_exaggeration
                temperature = base_temperature
            
            enriched_chunk = {
                **chunk,
                'chunk_id': i,
                'sentiment': sentiment,
                'tts_params': {
                    'exaggeration': round(exaggeration, 2),
                    'cfg_weight': base_cfg_weight,
                    'temperature': round(temperature, 2)
                }
            }
            enriched_chunks.append(enriched_chunk)
        
        return enriched_chunks
    
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise e

def generate_chunk_audio(chunk, voice_sample_path, progress_callback=None):
    """Generate audio for a single chunk"""
    try:
        tts = initialize_tts()
        
        # Extract TTS parameters
        params = chunk.get('tts_params', {})
        exaggeration = params.get('exaggeration', 0.4)
        cfg_weight = params.get('cfg_weight', 0.5)
        temperature = params.get('temperature', 0.9)
        
        # Generate audio
        audio_data = tts.generate_speech(
            text=chunk['text'],
            voice_sample=voice_sample_path,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature
        )
        
        # Apply audio processing
        if audio_data is not None:
            # Add contextual silence based on boundary type
            boundary_type = chunk.get('boundary_type', 'sentence_end')
            audio_data = add_contextual_silence(audio_data, boundary_type)
            
            if progress_callback:
                progress_callback(f"✅ Generated chunk {chunk['chunk_id']}")
        
        return audio_data
    
    except Exception as e:
        logger.error(f"Error generating audio for chunk {chunk.get('chunk_id', '?')}: {e}")
        return None

def generate_audiobook(text_file, voice_sample, exaggeration, cfg_weight, temperature, chunk_words, max_chunks, progress=gr.Progress()):
    """Main function to generate audiobook from text and voice sample"""
    try:
        if text_file is None:
            return None, "❌ Please upload a text file"
        
        if voice_sample is None:
            return None, "❌ Please upload a voice sample"
        
        progress(0.1, desc="📖 Reading text file...")
        
        # Read text file
        with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        if len(text_content.strip()) == 0:
            return None, "❌ Text file is empty"
        
        progress(0.2, desc="✂️ Chunking text...")
        
        # Process text into chunks
        chunks = process_text_to_chunks(text_content, chunk_words)
        
        # Limit chunks for demo (HF has time limits)
        if len(chunks) > max_chunks:
            chunks = chunks[:max_chunks]
            logger.info(f"⚠️ Limited to {max_chunks} chunks for demo")
        
        progress(0.3, desc=f"🎤 Generating audio for {len(chunks)} chunks...")
        
        # Generate audio for each chunk
        audio_segments = []
        log_messages = [f"📊 Processing {len(chunks)} chunks"]
        
        for i, chunk in enumerate(chunks):
            try:
                # Update progress
                chunk_progress = 0.3 + (0.6 * i / len(chunks))
                progress(chunk_progress, desc=f"🎵 Generating chunk {i+1}/{len(chunks)}")
                
                # Override global parameters if specified
                if exaggeration != 0.4:
                    chunk['tts_params']['exaggeration'] = exaggeration
                if cfg_weight != 0.5:
                    chunk['tts_params']['cfg_weight'] = cfg_weight
                if temperature != 0.9:
                    chunk['tts_params']['temperature'] = temperature
                
                # Generate audio
                audio_data = generate_chunk_audio(chunk, voice_sample)
                
                if audio_data is not None:
                    audio_segments.append(audio_data)
                    log_messages.append(f"✅ Chunk {i+1}: Generated ({len(chunk['text'])} chars)")
                else:
                    log_messages.append(f"❌ Chunk {i+1}: Failed to generate")
                
            except Exception as e:
                log_messages.append(f"❌ Chunk {i+1}: Error - {str(e)}")
                continue
        
        if not audio_segments:
            return None, "❌ No audio chunks were generated successfully"
        
        progress(0.9, desc="🎧 Combining audio segments...")
        
        # Combine audio segments
        try:
            import torchaudio
            combined_audio = torch.cat(audio_segments, dim=-1)
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                torchaudio.save(temp_audio.name, combined_audio, 24000)
                temp_audio_path = temp_audio.name
            
            log_messages.append(f"🎉 Generated {len(audio_segments)} chunks successfully")
            log_messages.append(f"📊 Total duration: {combined_audio.shape[-1] / 24000:.1f} seconds")
            
            progress(1.0, desc="✅ Complete!")
            
            return temp_audio_path, "\n".join(log_messages)
            
        except Exception as e:
            log_messages.append(f"❌ Failed to combine audio: {str(e)}")
            return None, "\n".join(log_messages)
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return None, error_msg

# Create Gradio interface
def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="ChatterboxTTS Audiobook Generator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🎙️ ChatterboxTTS Audiobook Generator
        
        Transform any text into a professional audiobook using AI voice cloning!
        
        **Instructions:**
        1. Upload a text file (.txt) containing your book content
        2. Upload a voice sample (.wav) for voice cloning (10-30 seconds recommended)
        3. Adjust TTS parameters if desired
        4. Click "Generate Audiobook" and wait for processing
        
        **Note:** This demo is limited to shorter texts due to processing time constraints.
        """)
        
        with gr.Row():
            with gr.Column():
                # Input files
                text_file = gr.File(
                    label="📖 Book Text File (.txt)",
                    file_types=[".txt"],
                    info="Upload your book content as a plain text file"
                )
                
                voice_sample = gr.Audio(
                    label="🎤 Voice Sample (.wav)",
                    type="filepath",
                    info="Upload a clear voice sample (10-30 seconds)"
                )
                
                # TTS Parameters
                with gr.Accordion("🎛️ Advanced Settings", open=False):
                    exaggeration = gr.Slider(
                        minimum=0.0,
                        maximum=2.0,
                        value=0.4,
                        step=0.1,
                        label="Exaggeration",
                        info="Emotional intensity (0.0 = monotone, 2.0 = very expressive)"
                    )
                    
                    cfg_weight = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.5,
                        step=0.1,
                        label="CFG Weight",
                        info="Text faithfulness (0.0 = creative, 1.0 = precise)"
                    )
                    
                    temperature = gr.Slider(
                        minimum=0.0,
                        maximum=5.0,
                        value=0.9,
                        step=0.1,
                        label="Temperature",
                        info="Randomness/creativity (0.0 = deterministic, 5.0 = very random)"
                    )
                    
                    chunk_words = gr.Slider(
                        minimum=20,
                        maximum=100,
                        value=50,
                        step=10,
                        label="Words per Chunk",
                        info="Sentence chunking size"
                    )
                    
                    max_chunks = gr.Slider(
                        minimum=5,
                        maximum=50,
                        value=20,
                        step=5,
                        label="Max Chunks (Demo Limit)",
                        info="Maximum chunks to process (for demo purposes)"
                    )
                
                generate_btn = gr.Button("🚀 Generate Audiobook", variant="primary", size="lg")
            
            with gr.Column():
                # Outputs
                audio_output = gr.Audio(
                    label="🎧 Generated Audiobook",
                    type="filepath"
                )
                
                log_output = gr.Textbox(
                    label="📋 Processing Log",
                    lines=15,
                    max_lines=20,
                    info="Real-time processing status and information"
                )
        
        # Examples
        gr.Markdown("""
        ## 📚 Tips for Best Results:
        
        - **Text Quality**: Clean, well-formatted text works best
        - **Voice Sample**: Clear, noise-free recording with consistent tone
        - **Length**: For demo, keep text under 1000 words
        - **Processing Time**: Expect 1-2 minutes per minute of final audio
        """)
        
        # Event handlers
        generate_btn.click(
            fn=generate_audiobook,
            inputs=[text_file, voice_sample, exaggeration, cfg_weight, temperature, chunk_words, max_chunks],
            outputs=[audio_output, log_output]
        )
    
    return interface

# Launch interface
if __name__ == "__main__":
    # Initialize TTS model at startup
    try:
        initialize_tts()
        logger.info("🚀 Starting Gradio interface...")
        
        interface = create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    
    except Exception as e:
        logger.error(f"Failed to start interface: {e}")
        raise e