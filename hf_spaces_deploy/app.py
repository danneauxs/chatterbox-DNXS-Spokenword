#!/usr/bin/env python3
"""
Step 2: Add ChatterboxTTS imports and basic model loading
"""

import gradio as gr
import torch

# Check device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Device: {DEVICE}")

# Global model variable
MODEL = None

def load_tts_model():
    """Load ChatterboxTTS model"""
    global MODEL
    if MODEL is None:
        try:
            from chatterbox.tts import ChatterboxTTS
            MODEL = ChatterboxTTS.from_pretrained(DEVICE)
            return "✅ ChatterboxTTS model loaded successfully!"
        except Exception as e:
            return f"❌ Model loading failed: {str(e)}"
    return "✅ Model already loaded"

def simple_test(text):
    """Test function that loads model and echoes text"""
    model_status = load_tts_model()
    return f"{model_status}\n\nYou said: {text}"

# Create interface
demo = gr.Interface(
    fn=simple_test,
    inputs="text",
    outputs="text",
    title="ChatterboxTTS Test - Step 2",
    description="Testing model loading"
)

if __name__ == "__main__":
    demo.launch()