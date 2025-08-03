# 🎤 resemble-ai/ChatterboxTTS

# * DNXS-Spokenword *

# Complete Audiobook Generation System

A comprehensive TTS audiobook production system built on ChatterboxTTS with multiple interfaces and deployment options.

## 🚀 Quick Start Options

Choose your preferred interface:

- **🖥️ GUI Interface** - Stupidly Full-featured desktop application (PyQt5)
- 
- <img width="1202" height="804" alt="tab1" src="https://github.com/user-attachments/assets/d22d6744-f799-4faa-aa7c-3ffb2ec2d861" />

- **💻 CLI Interface** - Command-line tool for automation and full featured
- 
-<img width="614" height="376" alt=" cli" src="https://github.com/user-attachments/assets/4af986db-2587-48d5-bdf9-15d0928e3a1b" />
- 
- **🌐 Local Gradio** - Web interface for local use - Book conversion only
- **☁️ Cloud Deployment** - Deploy to HuggingFace Spaces or RunPod book conversion on

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)
- Virtual environment (recommended)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ChatterboxTTS-DNXS-Spokenword
cd ChatterboxTTS-DNXS-Spokenword

# Run automated setup
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🖥️ GUI Interface (Desktop Application)

**Best for:** Interactive use, visual workflow, beginners, Power Users /Production Team

### Launch GUI

```bash
# Using launcher script (recommended)
./launch_gui.sh

# Or direct Python 
source venv/bin/activate
python3 main_launcher_gui.py
```

### Features

10 Tabs for dedicated features.

- ✅ Visual book/voice selection
- ✅ Real-time progress monitoring  
- ✅ Chunk repair tools
- ✅ Parameter adjustment interface
- ✅ Integrated audio player

---

## 💻 CLI Interface (Command Line)

**Best for:** Automation, scripting, headless servers

Full featured as the GUI, no messy mouse clicks, FAST simple single key strokes

### Launch CLI

```bash
# Using launcher script (recommended)  
./launch.sh

# Or direct Python
source venv/bin/activate
python3 main_launcher.py

# Or simple menu
python3 start.py
```

### CLI Features

- ✅ Interactive menu system
- ✅ Batch processing (set it up to run multiple books)
- ✅ Resume functionality
- ✅ Combine-only mode (combine repaired chunks)
- ✅ Chunk repair tools (fix one bad chunk & save the whole book)

---

## 🌐 Local Gradio Interface (Web)

**Best for:** Local web access, remote browser use

### Launch Local Gradio

```bash
# Using launcher script (recommended)
./launch_gradio.sh

# Or direct Python  
source venv/bin/activate
python3 gradio_main_interface.py
```

### Access

- **Local:** http://localhost:7860
- **Network:** http://your-ip:7860 (if enabled)

### Gradio Features

( limited do to lack of development - only book convrsion at this time )

- ✅ Web-based interface
- ✅ File upload/download
- ✅ Real-time progress tracking (kinda)
- ✅ Auto-completion detection
- ✅ Adjustable worker controls (# of parallel threads)

---

## ☁️ Cloud Deployment

### 🤗 HuggingFace Spaces Deployment

**Deploy the optimized HF version for public use:**

#### Step 1: Prepare HF Deployment

```bash
# The HF Deploy folder contains the optimized version
cd "HF Deploy"
ls  # You should see: app.py, requirements.txt, gradio_main_interface.py, etc.
```

#### Step 2: Create HuggingFace Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose:
   - **SDK:** Gradio
   - **Hardware:** CPU (free) or GPU (recommended: A10G Small)
   - **Visibility:** Public or Private

#### Step 3: Deploy to HF Spaces

```bash
# Clone your empty HF space  
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy ONLY the HF Deploy contents (NOT the entire repo)
cp -r ../path/to/ChatterboxTTS-DNXS-Spokenword/"HF Deploy"/* .

# Deploy to HF
git add .
git commit -m "Deploy ChatterboxTTS to HuggingFace Spaces"
git push
```

**⚠️ Important:** Only copy the contents of `HF Deploy/` folder, not the entire repository. This keeps the deployment lean and fast.

#### Step 4: Monitor Build

- HF will automatically build and deploy (5-10 minutes)
- Check build logs for any errors
- Your space will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

### ⚡ RunPod Deployment

**Deploy on RunPod for dedicated GPU access:**

#### Step 1: Prepare RunPod Deployment

```bash
# The RunPod Deploy folder contains the containerized version
cd "RunPod Deploy"
ls  # You should see optimized files for RunPod environment
```

#### Step 2: Upload to RunPod

1. Create a new RunPod instance with good GPU Pytorch 2.2 (2.8 will have to downgrade then install 2.2 - LOOOONG time to do)

2. **Upload all files** from `RunPod Deploy/` folder to your RunPod instance

3. Connect via SSH or web terminal

4. Run the installation script:
   
   ```bash
   chmod +x *.sh
   ./install.sh
   ```

#### Step 3: Access Interface

- RunPod will provide connection details
- Interface typically available on port 7860
- Use provided URL or tunnel for access

#### RunPod Features

- ✅ Dedicated GPU access
- ✅ High-performance processing
- ✅ Pay-per-use pricing
- ✅ Persistent storage options

---

## 🎯 Hardware Recommendations

### Local Development

- **CPU:** 4+ cores recommended
- **RAM:** 16GB+ (8GB minimum)
- **Storage:** 10GB+ free space
- **GPU:** Optional (CUDA-compatible for faster processing) 4-6GB VARAM

### Cloud Deployment

#### HuggingFace Spaces

- **CPU Tier:** Works but slower processing
- **Nvidia 4T Small (16GB):** Recommended for Cost Effective performance
- **A100 (40GB):** Overkill but fastest processing

#### RunPod

- **RTX 3090/4090:** Excellent price/performance
- **A6000/A100:** Professional grade
- **V100:** Good for experimentation

---

## 📁 Directory Structure

```
ChatterboxTTS-DNXS-Spokenword/
├── 📱 GUI Interface
│   ├── main_launcher_gui.py       # GUI application
│   └── launch_gui.sh              # GUI launcher
├── 💻 CLI Interface  
│   ├── main_launcher.py           # CLI application
│   ├── start.py                   # Simple CLI menu
│   └── launch.sh                  # CLI launcher
├── 🌐 Local Gradio
│   ├── gradio_main_interface.py   # Local web interface
│   └── launch_gradio_local.sh     # Local Gradio launcher
├── ☁️ Cloud Deployment
│   ├── HF Deploy/                 # HuggingFace Spaces version
│   └── RunPod Deploy/             # RunPod container version
├── 🔧 Core System
│   ├── modules/                   # Core processing modules
│   ├── src/                       # ChatterboxTTS source
│   ├── config/                    # Configuration files
│   └── wrapper/                   # Chunk tools
└── 📊 Data Directories
    ├── Text_Input/                # Source books (.txt files)
    ├── Voice_Samples/             # Voice cloning samples
    ├── Audiobook/                 # Generated audiobooks
    └── Output/                    # Final output location
```

---

## 🔧 Configuration

### Key Settings (config/config.py)

```python
# Worker Settings
MAX_WORKERS = 2                    # Parallel processing workers

# Quality Control  
ENABLE_ASR = False                 # Automatic Speech Recognition
ENABLE_REGENERATION_LOOP = True    # Auto-retry failed chunks
MAX_REGENERATION_ATTEMPTS = 3      # Max retry attempts

# Audio Processing
ENABLE_HUM_DETECTION = True        # Audio quality filtering
QUALITY_THRESHOLD = 0.7            # Minimum quality score
```

### Performance Tuning

- **Increase workers** for faster processing (monitor CPU/GPU usage)
- **Enable ASR** for quality validation (slower but higher quality)
- **Adjust quality thresholds** based on your standards

---

## 🚨 Troubleshooting

### Common Issues

#### "No module named 'chatterbox'"

```bash
# Install ChatterboxTTS
pip install chatterbox-tts

# Or install locally
pip install -e .
```

#### "CUDA out of memory"

```bash
# Reduce workers in config.py
MAX_WORKERS = 1

# Or use CPU mode
device = "cpu"
```

#### "PyQt5 not found" (GUI only)

```bash
# Install PyQt5
pip install PyQt5

# Or system-wide (Ubuntu)
sudo apt install python3-pyqt5
```

### Performance Issues

- **Slow processing:** Increase `MAX_WORKERS` (monitor resources)
- **Memory errors:** Decrease `MAX_WORKERS` or use CPU mode
- **Quality issues:** Enable ASR validation, adjust quality thresholds

---

## 📚 Usage Examples

### Basic Workflow

1. **Prepare content:**
   
   - Add `.txt` file 
     
     in Text_Input/` (GUI/CLI mode only)
     
     Gradio uses upload from local
   
   - Add voice sample (24kHz WAV recommended)
     
     GUI/CLI use local file, Gradio uses upload

2. **Choose interface:**
   
   - GUI: `./launch_gui.sh`
   - CLI: `./launch.sh` 
   - Web: `./launch_gradio_local.sh`

3. **Process book:**
   
   - Select text file and voice
   - Adjust parameters as needed
   - Start conversion
   - Monitor progress

4. **Get results:**
   
   - Final audiobook in `Output/`
   - Processing logs in `Audiobook/[BookName]/`

### Advanced Features

- **Resume processing:** Use resume tools for interrupted jobs
- **Chunk repair:** Fix individual problematic chunks
- **Batch processing:** Queue multiple books
- **Quality control:** ASR validation and regeneration

---

## 🌟 Key Features

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
- Audio normalization and speed control
- Cover art and book information embedding
- Chapter marking and navigation

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)  
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ChatterboxTTS** - Base TTS engine by Resemble AI
- **VADER Sentiment** - Sentiment analysis for dynamic parameters
- **Gradio** - Web interface framework
- **PyQt5** - Desktop GUI framework

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/ChatterboxTTS-DNXS-Spokenword/issues)
- **Documentation:** [Wiki](https://github.com/yourusername/ChatterboxTTS-DNXS-Spokenword/wiki)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/ChatterboxTTS-DNXS-Spokenword/discussions)

---

*Built with ❤️ for the audiobook community

***You are responsible for how you use this tool.  Don't do bad / illegal things.**
