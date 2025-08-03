#!/bin/bash
# ChatterboxTTS RunPod Installation Script
# Comprehensive setup for RunPod deployment

set -e  # Exit on any error

echo "🚀 ChatterboxTTS DNXS-Spokenword RunPod Installation Started"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (RunPod typically runs as root)
if [[ $EUID -eq 0 ]]; then
    print_status "Running as root - typical for RunPod"
else
    print_warning "Not running as root - may need sudo for some operations"
fi

# Update system packages
print_status "Updating system packages..."
apt-get update -y
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    wget \
    curl \
    build-essential \
    pkg-config \
    libsndfile1 \
    portaudio19-dev \
    python3-dev

print_success "System packages updated"

# Check Python version
python_version=$(python3 --version)
print_status "Python version: $python_version"

# Create workspace directories directly in workspace root
print_status "Creating workspace directories..."
cd /workspace

# Create data directories directly in workspace root (correct structure)
mkdir -p Text_Input Voice_Samples Audiobook Output
mkdir -p models
mkdir -p logs

# Set permissions
chmod -R 755 Text_Input Voice_Samples Audiobook Output
chmod -R 755 models

print_success "Workspace directories created"

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
python3 -m pip install --upgrade pip setuptools wheel

# Install PyTorch with CUDA support (pinned to working versions)
print_status "Installing PyTorch with CUDA support..."
python3 -m pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118

# Install Gradio first (essential for web interface)
print_status "Installing Gradio web interface..."
python3 -m pip install gradio>=4.0.0

# Install other requirements
print_status "Installing other requirements...LOOOONG TIME INSTALLING"
python3 -m pip install -r requirements-runpod.txt

print_success "Python dependencies installed"

# Check CUDA availability
print_status "Checking CUDA availability..."
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA devices: {torch.cuda.device_count()}')" || print_warning "Could not check CUDA status"

# Set up environment variables
print_status "Setting up environment variables..."
cat > /workspace/.env << 'EOF'
# ChatterboxTTS Environment Variables
CHATTERBOX_DATA_ROOT=/workspace/data
CUDA_VISIBLE_DEVICES=0
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
HF_HOME=/workspace/models/huggingface
TRANSFORMERS_CACHE=/workspace/models/transformers
EOF

print_success "Environment variables configured"

# Work in current directory - don't change directories
print_status "Installing in current directory: $(pwd)"

# Extract the main code modules
if [ -f "chatterbox_modules.tar.gz" ]; then
    print_status "Extracting ChatterboxTTS modules..."
    tar -xzf chatterbox_modules.tar.gz --no-same-owner
else
    print_error "chatterbox_modules.tar.gz not found!"
    exit 1
fi

print_success "ChatterboxTTS files installed"

# Download essential models (optional, models will download on first use)
print_status "Model download will happen automatically on first use"
print_status "To pre-download models, run the interface and trigger TTS generation"

# Set final permissions
chmod +x /workspace/*.py
chmod +x /workspace/*.sh

print_success "Installation completed successfully!"

echo ""
echo "🎉 DNXS-Spokenword [Chatterbox-xTTS] Installation Complete!"
echo "=========================================================="
echo ""
echo "📁 Data directories created:"
echo "  - Text Input: /workspace/Text_Input/"
echo "  - Voice Samples: /workspace/Voice_Samples/"
echo "  - Audiobook: /workspace/Audiobook/"
echo "  - Output: /workspace/Output/"
echo ""
echo "🚀 Starting DNXS-Spokenword [Chatterbox-xTTS]..."
echo ""

# Launch the main startup script
./start.sh