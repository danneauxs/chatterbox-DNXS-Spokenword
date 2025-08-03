#!/bin/bash
# ChatterboxTTS Gradio Interface Launcher Script - CONTAINER/CLOUD VERSION
# This version downloads fresh models and uses standard PyTorch cache behavior

echo "🚀 ChatterboxTTS Gradio Interface (Container/Cloud Mode)"
echo "======================================================="

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
echo "✅ Launching ChatterboxTTS Main Interface (Container Mode)..."
echo "💡 This version will download models fresh and use standard cache locations"
python3 gradio_main_interface.py