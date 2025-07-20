# Enhanced ChatterboxTTS Audiobook Pipeline

A comprehensive audiobook production system built on ChatterboxTTS with advanced text processing, quality control, and repair tools.

## Features

- **Intelligent Text Processing**: Smart sentence chunking with boundary detection
- **Sentiment-Aware TTS**: VADER sentiment analysis for dynamic parameter adjustment  
- **Quality Control**: Audio trimming, silence insertion, and validation
- **Repair Tools**: Interactive chunk editing and re-synthesis
- **Professional Output**: M4B audiobooks with metadata and normalization
- **Resume Capability**: Continue interrupted processing from any point
- **Memory Optimization**: Efficient processing for long books

## Quick Start

### 1. Installation

#### Prerequisites

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.8+ and FFmpeg
brew install python@3.11 ffmpeg

# Install Git (if not already installed)
brew install git
```

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg git
```

**Windows:**
- Install Python 3.8+ from python.org
- Install FFmpeg from https://ffmpeg.org/
- Install Git from git-scm.com

#### Setup

```bash
git clone https://github.com/danneauxs/chatterbox-DNXS-Spokenword.git
cd chatterbox-DNXS-Spokenword

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup

1. **Models**: ChatterboxTTS models will be downloaded automatically on first run
2. **Voice Samples**: Add your voice cloning samples to `Voice_Samples/`
3. **Books**: Create directories in `Text_Input/` with your book text files

### 3. Basic Usage

```bash
python3 main_launcher.py
```

**Menu Options:**
- **Option 1**: Full audiobook generation (text → JSON → audio → M4B)
- **Option 3**: Combine existing audio chunks to M4B
- **Option 4**: Generate JSON chunks only (no audio)
- **Option 6**: Repair/edit individual chunks
- **Option 7**: Generate audio from existing JSON

## Directory Structure

```
├── Text_Input/           # Your book text files
├── Voice_Samples/        # Voice cloning samples (.wav)
├── Audiobook/           # Generated audiobooks and processing files
├── src/chatterbox/      # Core TTS engine
├── modules/             # Processing modules
├── wrapper/             # Chunk editing tools
├── tools/               # Utility scripts
└── config/              # Configuration files
```

## Key Features

### Text Processing
- Smart sentence chunking with paragraph boundary detection
- Unicode quote normalization and abbreviation replacement  
- Punctuation-based silence insertion
- Chapter and section detection

### Audio Generation
- **In-memory processing** for faster performance
- Multi-threaded parallel TTS with dynamic worker allocation
- Real-time performance monitoring
- Model reinitialization for stability

### Quality Control
- Intelligent audio trimming using RMS energy detection
- Hum detection and noise artifact identification
- Optional ASR validation for accuracy checking
- Quarantine system for problematic chunks

### Professional Output
- M4B audiobook format with metadata
- Audio normalization and speed control (atempo)
- Cover art and book information embedding
- Chapter marking and navigation

## Configuration

Key settings in `config/config.py`:

```python
# Performance
MAX_WORKERS = 2                    # Parallel processing threads
BATCH_SIZE = 500                   # Chunks per batch before model reload

# Audio Processing  
ENABLE_AUDIO_TRIMMING = True       # Intelligent endpoint detection
ATEMPO_SPEED = 0.9                 # Playback speed (0.5-2.0)

# Silence Insertion (milliseconds)
SILENCE_COMMA = 150
SILENCE_PERIOD = 400
SILENCE_PARAGRAPH = 800
SILENCE_CHAPTER = 1500

# TTS Parameters
DEFAULT_EXAGGERATION = 0.4
DEFAULT_CFG_WEIGHT = 0.5  
DEFAULT_TEMPERATURE = 0.9
```

## Advanced Usage

### Custom TTS Parameters
The system supports per-chunk parameter adjustment based on sentiment analysis:
- **Exaggeration**: Emotional intensity (0.0-2.0)
- **CFG Weight**: Faithfulness to text (0.0-1.0)
- **Temperature**: Randomness/creativity (0.0-5.0)

### Chunk Repair Workflow
1. Generate initial audiobook
2. Use chunk repair tool to identify issues
3. Edit text or regenerate specific chunks
4. Combine repaired chunks into final audiobook

### Resume Processing
Interrupted processing can be resumed from any chunk:
```bash
# Resume from specific chunk number
python3 -c "from modules.resume_handler import resume_book_from_chunk; resume_book_from_chunk(150)"
```

## Dependencies

- Python 3.8+
- PyTorch (CUDA recommended)
- ChatterboxTTS
- FFmpeg (for audio processing)
- See `requirements.txt` for complete list

## Hardware Requirements

- **RAM**: 8GB+ recommended  
- **GPU**: NVIDIA GPU with 6GB+ VRAM (optional but recommended)
- **Storage**: 2-5GB per hour of final audio
- **macOS**: Apple Silicon (M1/M2) supported via MPS acceleration

## Troubleshooting

### Common Issues
- **Slow performance**: Reduce `MAX_WORKERS` or `BATCH_SIZE`
- **VRAM errors**: Enable `USE_DYNAMIC_WORKERS` or reduce batch size
- **Audio quality**: Adjust trimming thresholds in config
- **Text processing**: Check input encoding and formatting
- **macOS Permission Issues**: Run `sudo xcode-select --install` if encountering build errors
- **macOS FFmpeg**: Use `brew install ffmpeg` rather than other installation methods

### Performance Optimization
- Use GPU acceleration when available
- Adjust worker count based on system capabilities
- Monitor VRAM usage during processing
- Use SSD storage for better I/O performance

## Contributing

This is a fork of the original ChatterboxTTS. Contributions welcome for:
- Bug fixes and performance improvements
- Additional audio processing features
- UI/UX enhancements
- Documentation improvements

## License

[Check original ChatterboxTTS license]

## Acknowledgments

- Original ChatterboxTTS team
- OpenAI Whisper for ASR validation
- VADER sentiment analysis library
- FFmpeg for audio processing