#!/usr/bin/env python3
"""
Quick fix for HuggingFace Spaces requirements.txt
Removes git dependency that causes build failures
"""

fixed_requirements = """# HuggingFace Spaces Requirements
# Optimized for Gradio deployment

# Core TTS and ML
torch>=2.0.0
torchaudio>=2.0.0
transformers>=4.20.0
huggingface_hub>=0.15.0
safetensors>=0.3.0

# ChatterboxTTS specific (included in src/ directory)
# No external git dependency needed

# Audio processing
soundfile>=0.12.0
librosa>=0.9.0
pydub>=0.25.0

# Text processing and NLP
vaderSentiment>=3.3.0

# System utilities
psutil>=5.8.0

# Gradio for web interface
gradio>=4.0.0

# Optional dependencies for HF Spaces
numpy>=1.21.0
scipy>=1.7.0

# Additional dependencies for ChatterboxTTS
einops>=0.6.0
perth>=0.1.0"""

print("Fixed requirements.txt content:")
print("=" * 50)
print(fixed_requirements)
print("=" * 50)
print("\nCopy this content and paste it into your HF Space requirements.txt file")
print("Or upload the file: hf_spaces_deploy/requirements.txt")