#!/bin/bash
# ChatterboxTTS Gradio Interface Launcher Script - LOCAL VERSION
# This version uses shared model cache for local development

echo "🚀 DNXS-Spokenwork Gradio Interface [ChatterboxTTS]"
echo "========================================================="

# Set up shared model cache environment variables (same as GUI + PyTorch Hub)
export HF_HOME="/home/danno/.shared_model_cache/huggingface"
export TRANSFORMERS_CACHE="/home/danno/.shared_model_cache/transformers"
export PIP_CACHE_DIR="/home/danno/.shared_model_cache/pip_cache"
export TORCH_HUB_DIR="/home/danno/.shared_model_cache/torch"

echo "📦 Using shared model cache:"
echo "   HF_HOME: $HF_HOME"
echo "   TRANSFORMERS_CACHE: $TRANSFORMERS_CACHE"
echo "   TORCH_HUB_DIR: $TORCH_HUB_DIR"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found (venv/)"
    echo "   Consider creating one: python3 -m venv venv"
fi

# Check Python version
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "🐍 Python version: $python_version"

# Check if Gradio is installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "❌ Gradio not installed. Installing now..."
    pip install gradio
fi

# Launch the interface
echo "✅ Launching ChatterboxTTS Main Interface (Local Mode)..."
python3 gradio_main_interface.py
