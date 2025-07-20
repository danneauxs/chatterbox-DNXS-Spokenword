#!/bin/bash
# Setup script for ChatterboxTTS Audiobook Pipeline

echo "🚀 Setting up ChatterboxTTS Audiobook Pipeline..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "📍 Python version: $python_version"

if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.8+ required. Please upgrade Python."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p Text_Input Audiobook Output audio_chunks InputAudio InputVoice

# Check for FFmpeg
if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ FFmpeg found"
else
    echo "⚠️  FFmpeg not found. Please install FFmpeg for audio processing:"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   macOS: brew install ffmpeg"
    echo "   Windows: Download from https://ffmpeg.org/"
fi

# Check for CUDA
if python3 -c "import torch; print('✅ CUDA available' if torch.cuda.is_available() else '⚠️  CUDA not available - using CPU mode')" 2>/dev/null; then
    :
else
    echo "⚠️  PyTorch not installed yet - will be installed via requirements"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Add your book text files to Text_Input/ directory"
echo "3. Add voice samples to Voice_Samples/ directory"
echo "4. Run the program: python3 main_launcher.py"
echo ""
echo "📖 See README.md for detailed usage instructions"