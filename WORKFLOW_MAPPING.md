# ChatterboxTTS Workflow Mapping: GUI ↔ CLI Functions
## Complete Function Reference for Developers and Users

---

## 📋 **OVERVIEW**

This document maps all GUI interfaces to their corresponding CLI functions, providing developers and users with complete understanding of how to access ChatterboxTTS features through different interfaces.

**Interface Types:**
- **GUI**: Graphical interfaces (PyQt5 desktop app, Gradio web interface)
- **CLI**: Command-line tools and scripts
- **API**: Direct Python module/function calls

---

## 🎯 **MAIN ENTRY POINTS**

### Desktop GUI Application
```bash
# PyQt5 Desktop Application
python3 chatterbox_gui.py
./launch_gui.sh                    # Enhanced launcher with PyQt5 detection
```

### Web Interface (Gradio)
```bash
# Local Gradio Interface
python3 gradio_main_interface.py

# HuggingFace Spaces (auto-configured)
python3 app.py                     # Auto-installs dependencies + launches
```

### Command Line Interface
```bash
# Main CLI launcher menu
python3 main_launcher.py           # Interactive menu system

# Direct generation (bypass menu)
python3 GenTTS_Claude.py          # Main TTS processing pipeline
```

---

## 📚 **CORE AUDIOBOOK GENERATION WORKFLOWS**

### 1. COMPLETE AUDIOBOOK GENERATION

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **PyQt5 Tab 1** | `python3 main_launcher.py` → Option 4 | Text → JSON conversion | Preprocess text into chunks with metadata |
| **PyQt5 Tab 1** | `python3 GenTTS_Claude.py` | JSON → Audio conversion | Generate audio from processed chunks |
| **Gradio Tab 1** | `python3 gradio_tabs/tab1_convert_book.py` | Web-based conversion | Complete web interface for generation |

**Detailed CLI Workflow:**
```bash
# Step 1: Text Preprocessing (GUI: Tab 1 "Generate JSON")
python3 main_launcher.py
# Select Option 4: Generate chunks JSON
# Input: Text_Input/[book_name].txt
# Output: Text_Input/[book_name]_chunks.json

# Step 2: TTS Generation (GUI: Tab 1 "Convert to Audio") 
python3 GenTTS_Claude.py [book_name]
# Input: Text_Input/[book_name]_chunks.json + Voice_Samples/[voice].wav
# Output: Audiobook/[book_name]/[book_name].m4b
```

### 2. JSON-BASED REGENERATION

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **PyQt5 Tab 8** | `python3 utils/generate_from_json.py` | Direct JSON processing | Regenerate audio from existing JSON |
| **Manual editing** | Text editor → JSON file | Parameter tuning | Edit TTS parameters per chunk |

**CLI Usage:**
```bash
# Direct generation from edited JSON (faster, no text processing)
python3 utils/generate_from_json.py
# Input: Pre-existing chunks_info.json with custom TTS parameters
# Output: audio_chunks/ directory with individual WAV files
```

---

## 🔧 **CHUNK EDITING AND REPAIR TOOLS**

### 3. CHUNK-LEVEL OPERATIONS

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **PyQt5 Tab 7** | `python3 wrapper/chunk_tool.py` | Interactive chunk editor | Edit, play, regenerate individual chunks |
| **Future Gradio Tab 7** | `python3 wrapper/chunk_*.py` | Modular chunk tools | Specialized chunk operations |

**CLI Chunk Tools:**
```bash
# Interactive chunk repair interface
python3 wrapper/chunk_tool.py
# Functions: Edit text, regenerate audio, play chunks, batch operations

# Individual chunk operations
python3 wrapper/chunk_editor.py      # Edit chunk text
python3 wrapper/chunk_player.py      # Play/preview chunks  
python3 wrapper/chunk_synthesizer.py # Regenerate specific chunks
python3 wrapper/chunk_loader.py      # Load/manage chunk data
```

---

## 🎵 **AUDIO PROCESSING AND ENHANCEMENT**

### 4. AUDIO TOOLS AND ENHANCEMENT

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **Future PyQt5 Tab 5** | `tools/emotional_audio_enhancer.py` | GUI audio enhancement | Emotional processing of TTS output |
| **Future Gradio Tab 5** | `tools/audio_emotion_scanner.py` | Audio analysis | Scan existing audio for emotions |
| **Manual CLI** | `tools/combine_only.py` | Audio combination | Combine chunks without TTS |

**CLI Audio Tools:**
```bash
# GUI-based emotional audio enhancement
python3 tools/emotional_audio_enhancer.py
# Features: Pitch shift, formant change, compression, EQ, effects

# Command-line audio analysis
python3 tools/audio_emotion_scanner.py [audiobook_directory]
# Analyzes existing audio for emotional content and timestamps

# Simple chunk combination
python3 tools/combine_only.py [audio_chunks_directory]
# Combines existing chunks into final audiobook
```

---

## 🎭 **VOICE ANALYSIS AND TRAINING**

### 5. VOICE PROCESSING TOOLS

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **PyQt5 Voice Analyzer** | `voice_analyzer/` modules | Voice analysis | Real-time voice sample analysis |
| **Future Tab 8** | `tools/emotion_extractor.py` | Emotion extraction | Extract emotional samples from TTS |
| **Future Tab 8** | `tools/xtts_finetune_extractor.py` | Model extraction | Extract voice data from XTTS models |

**CLI Voice Tools:**
```bash
# Extract emotional voice samples from existing TTS output
python3 tools/emotion_extractor.py [audiobook_directory]
# Output: Organized emotional voice samples

# Extract voice data from XTTS-finetune models  
python3 tools/xtts_finetune_extractor.py [model_directory]
# Output: Compatible voice samples for ChatterboxTTS
```

---

## ⚙️ **CONFIGURATION AND SETTINGS**

### 6. SYSTEM CONFIGURATION

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **PyQt5 Tab 6** | `config/config.py` | Configuration file | Edit settings manually |
| **Gradio Tab 6** | `gradio_tabs/tab6_settings.py` | Web settings interface | Live configuration management |
| **System Info** | `status_check.py` | System status | Check project health |

**CLI Configuration:**
```bash
# Manual configuration editing
nano config/config.py             # Direct config file editing

# System status and health check  
python3 status_check.py            # Project status analysis

# Configuration backup/restore (via web interface)
# Access Gradio Tab 6 for GUI-based config management
```

---

## 📊 **MONITORING AND DEBUGGING**

### 7. SYSTEM MONITORING

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **Future Tab 9** | `modules/progress_tracker.py` | Performance monitoring | Real-time processing metrics |
| **Console output** | Log files in `Audiobook/*/` | Processing logs | Detailed operation logs |
| **VRAM monitoring** | Built into all TTS scripts | Memory monitoring | Prevent VRAM exhaustion |

**CLI Monitoring:**
```bash
# All TTS scripts include built-in monitoring:
# - Real-time progress with ETA
# - VRAM usage tracking  
# - Performance metrics (realtime factor)
# - Error logging and recovery

# Log locations:
# Audiobook/[book_name]/processing.log    # Main processing log
# Audiobook/[book_name]/chunk_validation.log  # Chunk-level details
```

---

## 🔄 **RESUME AND RECOVERY**

### 8. INTERRUPTED PROCESSING RECOVERY

| GUI Location | CLI Equivalent | Function | Purpose |
|-------------|---------------|----------|---------|
| **Auto-resume in GUI** | `modules/resume_handler.py` | Resume logic | Continue interrupted processing |
| **Resume options** | CLI prompts in main scripts | Interactive resume | Choose resume vs restart |

**CLI Resume Operations:**
```bash
# All main processing scripts support auto-resume:
python3 GenTTS_Claude.py [book_name]
# Automatically detects existing chunks and offers resume

# Manual resume analysis
python3 -c "
from modules.resume_handler import analyze_existing_chunks
from pathlib import Path
chunks_dir = Path('Audiobook/[book]/TTS/audio_chunks')  
resume_point, missing = analyze_existing_chunks(chunks_dir)
print(f'Resume from chunk: {resume_point}')
print(f'Missing chunks: {missing}')
"
```

---

## 📁 **FILE STRUCTURE AND DATA FLOW**

### 9. DIRECTORY ORGANIZATION

```
ChatterboxTTS/
├── Text_Input/              # Source text files and generated JSON
│   ├── [book_name].txt     # Raw text input  
│   └── [book_name]_chunks.json  # Processed chunks with metadata
├── Voice_Samples/           # Voice cloning samples (24kHz WAV)
├── Audiobook/              # Processing workspace
│   └── [book_name]/
│       ├── TTS/
│       │   ├── text_chunks/     # Text chunk files
│       │   └── audio_chunks/    # Individual WAV chunks
│       ├── [book_name].m4b      # Final audiobook
│       ├── processing.log       # Main processing log
│       └── chunk_validation.log # Detailed chunk logs
└── Output/                 # Final audiobook copies
```

### 10. DATA FLOW MAPPING

```
GUI Action                    →  CLI Command                    →  File Operations
─────────────────────────────────────────────────────────────────────────────────
Load Text File               →  File dialog/path selection     →  Text_Input/book.txt
Generate JSON                →  main_launcher.py Option 4      →  Text_Input/book_chunks.json  
Select Voice Sample          →  list_voice_samples()           →  Voice_Samples/*.wav
Convert to Audio            →  GenTTS_Claude.py               →  Audiobook/*/TTS/audio_chunks/
Chunk Editing               →  wrapper/chunk_tool.py          →  Individual chunk modification
Audio Enhancement           →  tools/emotional_audio_enhancer.py  →  Enhanced audio files
Final Export                →  Automatic M4B creation         →  Output/book.m4b
```

---

## 🚀 **PERFORMANCE OPTIMIZATION FEATURES**

### 11. ADVANCED PROCESSING FEATURES

| Feature | GUI Access | CLI Implementation | Performance Benefit |
|---------|------------|-------------------|-------------------|
| **Voice Embedding Caching** | Automatic in all GUIs | Built into TTS engine | 5-10% speed improvement |
| **Producer-Consumer Pipeline** | Transparent | Threading in TTS scripts | Parallel processing |
| **Memory-Optimized Processing** | VRAM monitoring displays | Automatic memory management | Prevents crashes |
| **GPU Persistence Mode** | Auto-enabled | GPU optimization in scripts | Faster model loading |
| **In-Memory Processing** | Default mode | No temp files created | Faster I/O |

---

## 🔍 **TROUBLESHOOTING QUICK REFERENCE**

### 12. COMMON ISSUES AND SOLUTIONS

| Problem | GUI Indicators | CLI Diagnostics | Solution |
|---------|---------------|-----------------|----------|
| **VRAM Exhaustion** | Progress stops, error messages | "CUDA out of memory" | Reduce MAX_WORKERS, restart |
| **Missing Dependencies** | Import errors on startup | ModuleNotFoundError | Run app.py or install manually |
| **Chunk Processing Errors** | Individual chunk failures | Check chunk_validation.log | Use chunk repair tools |
| **Voice Sample Issues** | Voice selection errors | Compatibility warnings | Use 24kHz WAV samples |
| **Resume Failures** | Restart from beginning | analyze_existing_chunks() | Check chunk directory integrity |

---

## 📖 **DEVELOPER INTEGRATION EXAMPLES**

### 13. PROGRAMMATIC ACCESS

```python
# Direct module usage for custom integrations

# Text processing
from modules.text_processor import sentence_chunk_text, smart_punctuate
chunks = sentence_chunk_text(text, max_words=20, min_words=4)

# TTS processing  
from modules.tts_engine import load_optimized_model, process_one_chunk
model = load_optimized_model("voice_sample.wav")
audio = process_one_chunk(chunk_text, model, tts_params)

# Progress tracking
from modules.progress_tracker import PerformanceTracker
tracker = PerformanceTracker()
tracker.log_chunk_completion(chunk_index, audio_duration)

# Resume handling
from modules.resume_handler import analyze_existing_chunks
resume_point, missing = analyze_existing_chunks(audio_dir)
```

---

## 🎯 **QUICK COMMAND REFERENCE**

### 14. MOST COMMON OPERATIONS

```bash
# Complete audiobook generation (most common workflow)
python3 main_launcher.py          # Interactive menu
python3 GenTTS_Claude.py [book]    # Direct processing

# Quick GUI interfaces
./launch_gui.sh                    # PyQt5 desktop app
python3 gradio_main_interface.py   # Web interface

# Chunk-level operations
python3 wrapper/chunk_tool.py      # Interactive chunk editor
python3 utils/generate_from_json.py # JSON-based regeneration

# Audio enhancement and analysis
python3 tools/emotional_audio_enhancer.py    # GUI audio effects
python3 tools/emotion_extractor.py [dir]     # Extract emotional samples

# System utilities
python3 status_check.py            # System health check
python3 app.py                     # HuggingFace Spaces launcher
```

---

This comprehensive mapping ensures developers and users can efficiently navigate between GUI and CLI interfaces, understanding the complete ChatterboxTTS ecosystem and choosing the best tools for their specific needs.