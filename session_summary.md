# Session Summary - ChatterboxTTS Enhancement Discussion
**Date**: 2025-01-15  
**Focus**: Voice Sample Enhancement & Emotional Range Improvement

## Key Problem Identified
- Current ChatterboxTTS uses single static voice samples for all emotional content
- Manual curation of emotional voice samples from narrators is impractical 
- Need automated system to create emotional voice libraries for better audiobook authenticity

## Major Decision: Voice Sample Switching vs Hybrid TTS System

### **XTTS v2 Hybrid System - REJECTED**
**Why considered**: User has custom XTTS v2 trained models (model.pth, vocab.json, ref.wav)
**Why rejected**: 
- Non-commercial licensing restrictions (vs ChatterboxTTS MIT license)
- Architectural incompatibility (.pth vs .safetensors formats)
- Added complexity without clear benefits for English-only use case
- Current ChatterboxTTS + VADER system already sophisticated and working

### **Voice Sample Switching System - SELECTED** ✅
**Approach**: Create emotional voice sample libraries, switch samples based on content emotion
**Benefits**: Keep existing architecture, dramatic quality improvement, manageable complexity

## Multi-Tier Voice Sample System Architecture

### **Tier 1: Automated Extraction (Best Quality)**
- **Input**: 30-120 min audiobook + optional ebook text
- **Method**: Audio emotion recognition + forced alignment or Whisper ASR
- **Output**: 6-8 emotional voice samples (10 sec each)
- **Target**: Professional audiobook narrations

### **Tier 2: Existing Clip Analysis (Fallback)**
- **Input**: Static 5-10 minute voice samples
- **Method**: Analyze existing samples for emotional segments
- **Output**: Best available emotional clips with confidence scoring
- **Target**: Limited sample sets

### **Tier 3: Sample Alteration (Enhancement)**
- **Method**: Prosodic manipulation of existing samples
- **Techniques**: Pitch shifting (±10-15%), tempo adjustment (±15-20%), formant shifting
- **Advanced**: Partial sentence manipulation (beginning/middle/end emotional shaping)
- **Target**: Fill gaps in emotional range

### **Tier 4: Synthetic Generation (Direct TTS Control)** ⭐
- **Method**: Skip sentiment analysis entirely, use direct TTS parameter control
- **Approach**: Preset emotional parameters + real-time tuning + A/B testing
- **Integration**: Use dnxs-spokenword for consistent voice characteristics
- **Target**: Always available fallback with full control

## Tier 4 Breakthrough Insight
**User's Key Realization**: "We probably do not want to use sentiment smoothing for these chunks. Do we even need VADER or whatever we replace VADER with. Possibly the raw TTS params and ChatterboxTTS's built-in parser would work for individual sentiment."

**Implementation**:
- Emotional preset parameters for happy, sad, angry, fearful, thoughtful, excited
- Interactive UI with parameter spinners for real-time adjustment
- Direct TTS generation using optimized emotional text prompts
- A/B testing system to compare parameter combinations
- Save optimal combinations to voice library

## Technical Implementation Details

### **Hardware Constraints & Solutions**
- **Hardware**: NVIDIA 4060 with 8GB VRAM
- **Challenge**: Whisper large-v3 requires more VRAM than available
- **Solution**: Apply XTTS fine-tuning batch optimization approach
  - Chunked processing: 10-15 minute audio segments
  - Memory management: torch.cuda.empty_cache() between chunks
  - Progressive fallback: 15min → 10min → 5min if OOM
  - Expected performance: 0.05-0.1x realtime (2hr book = 20-40 minutes)

### **Audio Quality Pipeline**
- **Input formats**: 64-192kbps, various sample rates (22kHz, 44.1kHz, 48kHz)
- **Quality assessment**: SNR, dynamic range, clipping detection, noise floor
- **Conservative cleanup**: DC removal, gentle normalization, high-pass filtering
- **Fallback strategy**: Use original audio if cleanup fails

### **Text Source Strategy**
- **Preferred**: Audiobook + matching ebook (forced alignment for best quality)
- **Alternative**: Whisper large-v3 ASR with chunked processing
- **Manual tools**: Dialogue formatting assistance for ASR output
- **Decision**: Ebook+audiobook approach superior to ASR-only

## Current ChatterboxTTS Integration Points

### **Model Architecture Analysis**
- **Loading**: `ChatterboxTTS.from_pretrained()` and `from_local()` (src/chatterbox/tts.py:138-189)
- **Voice conditioning**: `prepare_conditionals(wav_fpath)` - single file only, 10-second limit
- **Memory limits**: ENC_COND_LEN = 6 seconds, DEC_COND_LEN = 10 seconds
- **No multiple file support**: Architecture expects single reference sample

### **Current VADER System**
- **Location**: modules/tts_engine.py:416-567
- **Sophistication**: Already implements smoothing, parameter adjustment, JSON-driven processing
- **Enhancement opportunity**: Replace VADER (1 dimension) with GoEmotions (27 categories)

## Standalone Program Design Decision

### **Architecture**: `chatterbox-voice-extractor`
- **Deployment**: Separate git repository for sharing
- **Integration**: Invokable from main program, but standalone capable
- **Modularity**: Can be used independently or integrated
- **Focus**: Specialized voice sample preparation system

### **Program Structure**
```
chatterbox-voice-extractor/
├── src/
│   ├── audio_analysis.py       # Quality assessment, cleanup
│   ├── emotion_extraction.py   # Advanced emotion detection
│   ├── whisper_chunked.py      # 8GB VRAM optimized transcription
│   ├── sample_alteration.py    # Pitch/tempo/formant manipulation
│   └── synthetic_generation.py # Direct TTS parameter control
├── ui/
│   ├── synthetic_generator.py  # GUI for parameter tuning
│   └── sample_manager.py       # Voice library management
├── config/
│   ├── emotion_prompts.json    # Text prompts for synthetic generation
│   ├── tts_presets.json       # Base parameters for each emotion
│   └── extraction_params.json # Default processing parameters
└── integration_api.py          # API for main program
```

## Implementation Priority

### **Immediate Next Steps** (High Priority)
1. **Design Tier 4 synthetic generation system** - Most accessible, immediate results
2. **Create preset emotional parameter library** - Foundation for all approaches
3. **Build parameter tuning UI** - Real-time feedback and optimization
4. **Test with dnxs-spokenword integration** - Validate approach with existing TTS

### **Medium-Term Development**
1. **Implement Tier 3 sample alteration** - Prosodic manipulation techniques
2. **Design Tier 2 existing clip analysis** - For limited sample scenarios
3. **Advanced emotion analysis beyond VADER** - GoEmotions integration

### **Long-Term Goals**
1. **Complete Tier 1 automated extraction** - Full audiobook processing pipeline
2. **8GB VRAM-optimized Whisper implementation** - Chunked processing system
3. **Standalone program deployment** - Separate repository and distribution

## Key Insights & Decisions

### **User Requirements**
- **Quality over speed for voice preparation** - One-time investment acceptable
- **English-only focus** - No multilingual requirements
- **Existing hardware constraints** - 8GB VRAM optimization essential
- **Integration with current workflow** - Preserve existing interfaces (Gradio, CLI, GUI)

### **Strategic Approach**
- **Multi-tier fallback system** - Always have emotional samples regardless of input
- **Direct parameter control** - Skip complex analysis for synthetic generation
- **Reusable voice libraries** - One-time setup, ongoing benefits
- **Modular architecture** - Standalone program with integration capability

## Files Updated
- **`todo.txt`**: Complete todo list with new high-priority sections + user thought process documentation
- **`enhancement.txt`**: Comprehensive technical architecture and implementation details
- **`session_summary.md`**: This summary for session continuity

## Current Status
- **Architecture designed** ✅
- **Technical approach validated** ✅
- **Implementation plan created** ✅
- **Documentation complete** ✅
- **Ready for development** ✅

## Next Session Goals
1. **Start with Tier 4 implementation** - Synthetic generation system
2. **Create emotional parameter presets** - Based on ChatterboxTTS capabilities
3. **Build basic parameter tuning interface** - Real-time adjustment and testing
4. **Validate approach with test samples** - Confirm emotional authenticity improvement

---
*Session captured terminal transcript for complete technical discussion context*