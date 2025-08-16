# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Chatterbox is a modular TTS (Text-to-Speech) audiobook production system built on ChatterboxTTS. The project combines two main components:

1. **ChatterboxTTS Core** (`src/chatterbox/`) - The underlying TTS engine with models for speech synthesis and voice conversion
2. **GenTTS Pipeline** - A comprehensive audiobook generation system with chunking, quality control, and repair tools

## Development Commands

### Running the System

```bash
# Activate virtual environment first (required for voice analyzer)
source venv/bin/activate

# Main GUI with voice analyzer support
python3 chatterbox_gui.py

# Main launcher with interactive menu
python3 main_launcher.py

# Direct GenTTS pipeline
python3 GenTTS_Claude.py

# Simple start script
python3 start.py
```

### Python Environment

The project uses a virtual environment located at `venv/`. Activate it with:
```bash
source venv/bin/activate
```

### No Build/Test/Lint Commands

This project does not appear to have standard build, test, or lint commands configured. Testing is done through the interactive tools and manual validation.

## Architecture

### Core TTS Engine (`src/chatterbox/`)

- **`tts.py`** - Main TTS interface with ChatterboxTTS class for text-to-speech generation
- **`vc.py`** - Voice conversion functionality with ChatterboxVC class
- **`models/`** - Neural network models:
  - `t3/` - T3 model for text processing and alignment
  - `s3gen/` - S3Gen model for speech generation
  - `s3tokenizer/` - Speech tokenization
  - `voice_encoder/` - Voice embedding and encoding
  - `tokenizers/` - Text tokenization utilities

### GenTTS Pipeline

- **`GenTTS_Claude.py`** - Main audiobook generation script with advanced quality control
- **`main_launcher.py`** - Unified CLI launcher for various operations
- **`modules/`** - Modular processing components:
  - `text_processor.py` - Text chunking and preprocessing
  - `tts_engine.py` - TTS interface and model management
  - `audio_processor.py` - Audio quality validation and processing
  - `file_manager.py` - File operations and directory management
  - `progress_tracker.py` - Progress monitoring and logging
  - `resume_handler.py` - Resume functionality for interrupted jobs
- **`wrapper/`** - Chunk editing and repair tools:
  - `chunk_tool.py` - Interactive chunk repair interface
  - `chunk_loader.py` - Chunk data management
  - `chunk_editor.py` - Chunk text editing
  - `chunk_player.py` - Audio playback utilities
  - `chunk_synthesizer.py` - Individual chunk TTS generation
- **`tools/`** - Utility scripts for combining audio chunks
- **`config/`** - Configuration files and settings

### Directory Structure

```
Text_Input/          # Source books (.txt files, metadata, cover images)
Voice_Samples/       # Voice cloning samples (24kHz WAV files)
Audiobook/          # Generated audiobooks and processing logs
├── TTS/            # Intermediate processing files
│   ├── text_chunks/    # Segmented text files
│   └── audio_chunks/   # Generated audio segments
└── [Book Name]/    # Final audiobook files and logs
InputAudio/         # Input audio files for processing
InputVoice/         # Voice samples for training
Output/             # Final output audiobooks
audio_chunks/       # Intermediate audio chunk storage
```

## Key Features

### Text Processing
- Smart sentence chunking with paragraph boundary detection
- JSON-driven preprocessing workflow with metadata
- Boundary type detection (chapter_start, chapter_end, paragraph_end, section_break)
- Unicode quote normalization (smart quotes → ASCII)
- Abbreviation replacement system
- Punctuation normalization for TTS compatibility

### Audio Generation - **IN-MEMORY PROCESSING SYSTEM**
- **Memory-based TTS processing** - eliminates temp file I/O for faster performance
- Multi-threaded parallel TTS processing
- Real-time performance monitoring with realtime factor calculation
- Memory management preventing VRAM fragmentation
- Model reinitialization every 500 chunks for stability
- Single disk write per chunk (final output only)

### Quality Control
- TTS hum detection with frequency analysis
- Audio health validation (clipping, silence, flatness detection)
- Optional ASR validation with similarity checking
- Quarantine system for problematic chunks

### Repair and Revision Tools
- Interactive chunk repair interface
- Individual chunk re-synthesis
- Audio playback and validation
- Batch repair operations

## Configuration

Key configuration parameters are typically defined in:
- `config/config.py` - Main configuration settings
- Individual module files contain inline configuration constants

Important settings:
- `MAX_WORKERS` - Parallel processing threads (default: 2)
- `VRAM_SAFETY_THRESHOLD` - Memory limit trigger (default: 6.5GB)
- `CHUNK_WORDS` - Text segmentation parameters
- Hum detection frequency ranges and thresholds
- Silence insertion durations for chapters and paragraphs

## Dependencies

Core dependencies include:
- `torch` and `torchaudio` - PyTorch for neural networks
- `librosa` - Audio processing
- `huggingface_hub` - Model downloading
- `safetensors` - Model loading
- `soundfile` - Audio I/O
- `pydub` - Audio manipulation
- `whisper` - Optional ASR validation
- `pynvml` - GPU monitoring
- `ffmpeg` - Audio processing (system dependency)

## Session Continuity

### Quick Project Status
Run the status checker to get immediate context:
```bash
python3 status_check.py
```

### Session State Tracking
- `SESSION_STATE.md` - Current development status and priorities
- `status_check.py` - Automated project state analysis
- Regular git commits recommended for checkpoint tracking

### Development Workflow
1. Run `python3 status_check.py` to assess current state
2. Review `SESSION_STATE.md` for context and priorities
3. Update session state file when starting/ending significant work
4. Create git commits at logical development milestones

## Usage Patterns

### **UPDATED WORKFLOW - JSON-Driven Processing**

### Basic Audiobook Generation
1. Place text file in `Text_Input/`
2. Add voice sample to `Voice_Samples/`  
3. Run `python3 main_launcher.py` and select Option 4: "Generate chunks JSON"
4. JSON file with metadata created in `Text_Input/[book]_chunks.json`
5. Select TTS conversion option - **now uses JSON for optimized processing**
6. Monitor progress (in-memory processing = faster, fewer temp files)
7. Final audiobook generated in `Output/`

### **Architecture: Text → JSON → TTS Pipeline**
- **Step 1:** Text processing creates JSON with boundary detection and metadata
- **Step 2:** TTS engine reads JSON and processes audio entirely in memory  
- **Step 3:** Single disk write per chunk (final output only)

### Chunk Repair Workflow
1. Use chunk repair tool to identify problematic chunks
2. Edit text or regenerate audio as needed
3. Validate repairs and continue processing
4. Combine repaired chunks into final audiobook

### Resume Operations
- Use `resume_handler.py` to continue from specific chunk numbers
- Particularly useful for long books or after interruptions
- Maintains processing state and progress tracking

## Memories

### Development Notes
- Tab #1 is currently the only functional tab in the system
- Other tabs are not relevant at this time
- Confirmed that tab 5 is not needed and can be disregarded

### Memory Management Notes
- 7 NO, only 4GB of 24 used. The others possibly. how can we determine which it is?

### Performance Optimization Notes
- 5 already tried. 1 worker runs slightly faster than multiple.