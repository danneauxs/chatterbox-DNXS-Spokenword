#!/bin/bash

echo "🚀 Starting ChatterboxTTS GUI..."
cd "/home/danno/MyApps/chatterbox (copy)"

# Set up shared model cache environment variables
export HF_HOME="/home/danno/.shared_model_cache/huggingface"
export TRANSFORMERS_CACHE="/home/danno/.shared_model_cache/transformers"
export PIP_CACHE_DIR="/home/danno/.shared_model_cache/pip_cache"

echo "📦 Using shared model cache:"
echo "   HF_HOME: $HF_HOME"
echo "   TRANSFORMERS_CACHE: $TRANSFORMERS_CACHE"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ No virtual environment found - using system Python"
fi

# Check for required packages
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ PyQt5 not found. Installing..."
    pip install PyQt5
fi

echo "🎨 Launching ChatterboxTTS GUI..."
python3 chatterbox_gui.py