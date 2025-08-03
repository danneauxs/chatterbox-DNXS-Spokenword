# ChatterboxTTS RunPod Deployment Guide

## Quick Start

0. Choose **<u>python 2.2</u>** for runpod
1. **Upload the deployment package** to your RunPod instance
2. **Extract and run installation:**

```bash
# Make installation script executable (IMPORTANT!)
chmod +x *.sh
# Run installation
./install_runpod.sh
```

## What This Package Contains

- `install_runpod.sh` - Main installation script
- `start.sh` - Interface launcher
- `requirements.txt` - Full dependencies (local development)
- `requirements-runpod.txt` - Streamlined dependencies (cloud deployment)
- `chatterbox_modules.tar.gz` - Complete ChatterboxTTS codebase

## Installation Process

The installation script will: (it may seem to stall but just wait)

1. Update system packages
2. Install required system dependencies (takes time)
3. Create Python virtual environment
4. Install PyTorch with CUDA support (takes time)
5. Install all Python requirements (um more time)
6. Extract ChatterboxTTS modules (yeah more time)
7. Set up environment variables
8. Launch the interface   (after abouot 20-25 min)

## Directory Structure After Installation

```
/workspace/
├── Text_Input/          # Your books (.txt files)  CLI version use only
├── Voice_Samples/       # Voice cloning samples   CLI version use only
├── Audiobook/          # Generated audiobooks   Output of conversion
├── Output/             # Final output files  *** not quite sure on that
├── venv/               # Python virtual environment
├── gradio_main_interface.py
├── main_launcher.py
├── modules/
├── src/
├── config/
└── ... (other files)
```

## Usage

After installation, you can choose between:

1. **Gradio Web Interface** (Recommended) - Modern web UI
2. **CLI Interface** - Command-line tools

## Troubleshooting

### Permission Issues

```bash
chmod +x install_runpod.sh
chmod +x start.sh
```

### Missing Dependencies

The installation script includes all required dependencies. If you encounter missing packages, they will be installed automatically.

### CUDA Issues

The script automatically detects and configures CUDA if available.

## Support

Post a message. It's a one man operation so maybe yes maybe no it happens