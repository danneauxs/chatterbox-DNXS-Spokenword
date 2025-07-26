#!/usr/bin/env python3
"""
Working Gradio Interface for ChatterboxTTS Audiobook Pipeline
Based on successful HuggingFace Spaces example
"""

import random
import numpy as np
import torch
import gradio as gr
import spaces
import tempfile
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Running on device: {DEVICE}")

# --- Global Model Initialization ---
MODEL = None

def get_or_load_model():
    """Loads the ChatterboxTTS model if it hasn't been loaded already,
    and ensures it's on the correct device."""
    global MODEL
    if MODEL is None:
        print("Model not loaded, initializing...")
        try:
            # Import ChatterboxTTS using the correct path
            from chatterbox.src.chatterbox.tts import ChatterboxTTS
            MODEL = ChatterboxTTS.from_pretrained(DEVICE)
            if hasattr(MODEL, 'to') and str(MODEL.device) != DEVICE:
                MODEL.to(DEVICE)
            print(f"Model loaded successfully. Internal device: {getattr(MODEL, 'device', 'N/A')}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return MODEL

# Attempt to load the model at startup.
try:
    get_or_load_model()
except Exception as e:
    print(f"CRITICAL: Failed to load model on startup. Application may not function. Error: {e}")

def set_seed(seed: int):
    """Sets the random seed for reproducibility across torch, numpy, and random."""
    torch.manual_seed(seed)
    if DEVICE == "cuda":
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)

@spaces.GPU
def generate_single_chunk(
    text_input: str,
    audio_prompt_path_input: str = None,
    exaggeration_input: float = 0.5,
    temperature_input: float = 0.8,
    seed_num_input: int = 0,
    cfgw_input: float = 0.5
) -> tuple[int, np.ndarray]:
    """Generate TTS audio for a single text chunk"""
    current_model = get_or_load_model()

    if current_model is None:
        raise RuntimeError("TTS model is not loaded.")

    if seed_num_input != 0:
        set_seed(int(seed_num_input))

    print(f"Generating audio for text: '{text_input[:50]}...'")
    
    # Handle optional audio prompt
    generate_kwargs = {
        "exaggeration": exaggeration_input,
        "temperature": temperature_input,
        "cfg_weight": cfgw_input,
    }
    
    if audio_prompt_path_input:
        generate_kwargs["audio_prompt_path"] = audio_prompt_path_input
    
    wav = current_model.generate(
        text_input[:500],  # Limit chunk size
        **generate_kwargs
    )
    print("Audio generation complete.")
    return (current_model.sr, wav.squeeze(0).numpy())

def process_text_for_audiobook(text_content, max_chunks=10):
    """Simple text chunking for audiobook generation"""
    # Basic sentence splitting
    sentences = []
    current_chunk = ""
    
    # Split by periods, exclamation marks, question marks
    import re
    sentence_endings = re.split(r'[.!?]+', text_content)
    
    for sentence in sentence_endings:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # If adding this sentence would make chunk too long, start new chunk
        if len(current_chunk) + len(sentence) > 300:
            if current_chunk:
                sentences.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # Sentence itself is too long, split it
                words = sentence.split()
                for i in range(0, len(words), 50):  # 50 words per chunk max
                    chunk = " ".join(words[i:i+50])
                    sentences.append(chunk)
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add final chunk
    if current_chunk:
        sentences.append(current_chunk.strip())
    
    # Limit for demo
    return sentences[:max_chunks]

@spaces.GPU
def generate_audiobook(
    text_file,
    voice_sample,
    exaggeration,
    cfg_weight, 
    temperature,
    max_chunks,
    progress=gr.Progress()
):
    """Generate audiobook from uploaded text file and voice sample"""
    
    if text_file is None:
        return None, "❌ Please upload a text file"
    
    if voice_sample is None:
        return None, "❌ Please upload a voice sample"
    
    try:
        progress(0.1, desc="📖 Reading text file...")
        
        # Read text file
        with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        if len(text_content.strip()) == 0:
            return None, "❌ Text file is empty"
        
        progress(0.2, desc="✂️ Chunking text...")
        
        # Process text into chunks
        chunks = process_text_for_audiobook(text_content, max_chunks)
        
        progress(0.3, desc=f"🎤 Generating audio for {len(chunks)} chunks...")
        
        # Generate audio for each chunk
        audio_segments = []
        log_messages = [f"📊 Processing {len(chunks)} chunks"]
        
        for i, chunk_text in enumerate(chunks):
            try:
                # Update progress
                chunk_progress = 0.3 + (0.6 * i / len(chunks))
                progress(chunk_progress, desc=f"🎵 Generating chunk {i+1}/{len(chunks)}")
                
                # Generate audio for this chunk
                sample_rate, audio_data = generate_single_chunk(
                    text_input=chunk_text,
                    audio_prompt_path_input=voice_sample,
                    exaggeration_input=exaggeration,
                    temperature_input=temperature,
                    cfgw_input=cfg_weight
                )
                
                audio_segments.append(audio_data)
                log_messages.append(f"✅ Chunk {i+1}: Generated ({len(chunk_text)} chars)")
                
            except Exception as e:
                log_messages.append(f"❌ Chunk {i+1}: Error - {str(e)}")
                continue
        
        if not audio_segments:
            return None, "❌ No audio chunks were generated successfully"
        
        progress(0.9, desc="🎧 Combining audio segments...")
        
        # Combine audio segments
        try:
            # Add small silence between chunks
            silence = np.zeros(int(sample_rate * 0.5))  # 0.5 second silence
            
            combined_segments = []
            for i, segment in enumerate(audio_segments):
                combined_segments.append(segment)
                if i < len(audio_segments) - 1:  # Don't add silence after last chunk
                    combined_segments.append(silence)
            
            combined_audio = np.concatenate(combined_segments)
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                import soundfile as sf
                sf.write(temp_audio.name, combined_audio, sample_rate)
                temp_audio_path = temp_audio.name
            
            log_messages.append(f"🎉 Generated {len(audio_segments)} chunks successfully")
            log_messages.append(f"📊 Total duration: {len(combined_audio) / sample_rate:.1f} seconds")
            
            progress(1.0, desc="✅ Complete!")
            
            return temp_audio_path, "\n".join(log_messages)
            
        except Exception as e:
            log_messages.append(f"❌ Failed to combine audio: {str(e)}")
            return None, "\n".join(log_messages)
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

# Create Gradio interface
with gr.Blocks(title="ChatterboxTTS Audiobook Generator", theme=gr.themes.Soft()) as demo:
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
                label="🎤 Voice Sample",
                type="filepath",
                info="Upload a clear voice sample (10-30 seconds)"
            )
            
            # TTS Parameters
            with gr.Accordion("🎛️ Advanced Settings", open=False):
                exaggeration = gr.Slider(
                    minimum=0.0,
                    maximum=2.0,
                    value=0.5,
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
                    value=0.8,
                    step=0.1,
                    label="Temperature",
                    info="Randomness/creativity (0.0 = deterministic, 5.0 = very random)"
                )
                
                max_chunks = gr.Slider(
                    minimum=5,
                    maximum=30,
                    value=15,
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
    - **Length**: For demo, keep text under 2000 words
    - **Processing Time**: Expect 1-2 minutes per minute of final audio
    """)
    
    # Event handlers
    generate_btn.click(
        fn=generate_audiobook,
        inputs=[text_file, voice_sample, exaggeration, cfg_weight, temperature, max_chunks],
        outputs=[audio_output, log_output]
    )

# Launch interface
if __name__ == "__main__":
    logger.info("🚀 Starting ChatterboxTTS audiobook generator...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)