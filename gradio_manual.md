# ChatterboxTTS Gradio Web Interface - Complete User Manual

(Gradio Still under Development)

**Version**: 0.02  
**Date**: 2025-08-09  
**Interface Type**: Web-based Gradio Application  

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Tab 1: Convert Book](#tab-1-convert-book)
3. [Tab 2: Configuration Settings](#tab-2-configuration-settings)
4. [Tab 3: Voice Analysis (Placeholder)](#tab-3-voice-analysis-placeholder)
5. [Tab 4: Combine Audio](#tab-4-combine-audio)
6. [Tab 5: Prepare Text](#tab-5-prepare-text)
7. [Tab 6: Settings](#tab-6-settings)
8. [Tab 7: Chunk Tools](#tab-7-chunk-tools)
9. [Tab 8: JSON Generate](#tab-8-json-generate)
10. [Tab 9: System Monitor (Placeholder)](#tab-9-system-monitor-placeholder)
11. [Tab 10: About (Placeholder)](#tab-10-about-placeholder)
12. [Troubleshooting](#troubleshooting)
13. [Best Practices](#best-practices)

---

## Getting Started

### System Requirements

- Web browser with JavaScript enabled
- Internet connection (for initial loading)
- ChatterboxTTS backend system properly installed

### Launching the Interface

1. Navigate to the project directory
2. Run: `./launch_gradio_local.sh OR python3 gradio_main_interface.py` 
3. Open your web browser to: `http://localhost:7860`
4. The interface will display available tabs and their status

### Interface Overview

- **Modular Design**: Each major function is a separate tab
- **Real-time Status**: All operations show progress and status updates
- **Error Handling**: Clear error messages and recovery guidance
- **Web Compatibility**: Works on desktop and mobile browsers

---

## Tab 1: Convert Book

**Purpose**: Main audiobook generation interface - converts text files into complete audiobooks with voice cloning.

### Step-by-Step Instructions

#### 1. **Select Your Book**

- Use the dropdown to browse for available books  
- Books should be in subdirectories: /BookName/book.txt`
- The interface will display book information once selected

#### 2. **Choose Voice Sample**

- Select a voice from the "Voice Sample" dropdown
- Supported formats: `.wav` files (24kHz recommended)
- Preview voice information if available

#### 3. **Configure TTS Parameters**

- **Temperature**: Controls randomness/creativity (0.0-2.0)
  - Lower = more consistent
  - Higher = more varied expression (above 1.0 unpredictable)
- **CFG Weight**: Guidance strength (0.0-1.0)
  - Higher = lower value is closer to orginal text. May aslo slow down output
    
    m4b can be regenerated at slower speed if need be, so set this as you like.
- **Exaggeration**: Speech intensity (0.0-2.0)
  - Higher = more dramatic delivery ( 0.8 is probably the limit unless you desire utter hallucinations)

#### 4. **Advanced Options**

- **Enable VADER**: Sentiment-based parameter adjustment (sets per chunk TTS params)
- **Min P**: Minimum probability threshold
- **Top P**: Nucleus sampling parameter
- **Repetition Penalty**: Reduces repetitive speech

#### 5. **Start Generation**

- Click "🎤 Generate Audiobook"
- Monitor progress through the progress bar
- View detailed logs in the output area
- Generation may take 30 minutes to several hours depending on book length

#### 6. **Results**

- Completed audiobook saved to `Output/BookName/`
- Individual chunks in `Audiobook/BookName/TTS/audio_chunks/`
- Processing logs in `Audiobook/BookName/run.log`

#### 7. **Important: Refresh After Completion**

**⚠️ After audiobook generation completes, you MUST click "🔄 Refresh Results" to see the new M4B file in the dropdown!**

- The generated audiobook won't appear automatically
- Click the blue "🔄 Refresh Results" button after completion
- This will update both the playback and regeneration dropdowns
- Your new audiobook will then be available for playback

### Expected Outputs

- `BookName_combined.wav`: Uncompressed audio
- `BookName_combined.m4b`: Audiobook format with metadata
- Processing logs and statistics

---

## Tab 2: Configuration Settings

**Purpose**: System-wide configuration and parameter management for optimal TTS performance.

### Step-by-Step Instructions

#### 1. **Workers & Batch Settings**

- **Workers**: Set parallel processing threads (1-8)
  - **Recommendation**: Start with 2, increase only if GPU/VRAM usage < 60%
  - **More workers = faster processing but higher memory usage**
- **Batch Size**: Chunks processed before model reload (50-500)
  - **Higher values = better efficiency but more VRAM usage**
  - **Lower values = more stable for limited VRAM**

#### 2. **Chunk Word Limits**

- **Min Words**: Minimum words per chunk (1-50)
  - **Recommendation**: 5-10 words minimum
- **Max Words**: Maximum words per chunk (10-100)
  - **Recommendation**: 20-30 words maximum
  - **Too many words can lead to poor TTS quality**

#### 3. **Audio Processing**

- **Audio Normalization**: Enable loudness normalization
  - **Target LUFS**: Loudness level (-30 to -6 dB)
  - **Recommendation**: -16 LUFS for audiobooks
- **Automatic Audio Trimming**: Remove silence from chunks
  - **Speech Threshold**: Detection sensitivity (0.001-0.1)
  - **Buffer**: Silence buffer after speech (0-500ms)

#### 4. **TTS Parameter Limits**

Set upper and lower bounds for automatic parameter adjustment:

- **Exaggeration Min/Max**: Range for VADER adjustments
- **CFG Min/Max**: CFG weight boundaries
- **Temperature Min/Max**: Temperature variation limits

#### 5. **TTS Defaults**

Base values before VADER adjustments:

- **Default Exaggeration**: 0.50 (recommended)
- **Default CFG Weight**: 0.50 (recommended)
- **Default Temperature**: 0.80 (recommended)

#### 6. **VADER Sensitivity**

Control how much sentiment affects TTS parameters:

- **Exaggeration Sensitivity**: 0.30 (recommended)
- **CFG Sensitivity**: 0.30 (recommended)
- **Temperature Sensitivity**: 0.30 (recommended)
- **Higher values = more dramatic sentiment-based changes**

#### 7. **Silence Settings**

Configure pauses for natural speech flow:

- **Chapter Start/End**: 1000-1500ms (recommended)
- **Section Break**: 800ms (recommended)
- **Paragraph End**: 500ms (recommended)
- **Punctuation**: 200-500ms based on punctuation type

#### 8. **Save Configuration**

- **Save Configuration**: Apply and store current settings
- **Reset to Defaults**: Restore original values
- **Reload Configuration**: Load settings from file

### Usage Tips

- **Start with defaults** and adjust gradually
- **Monitor VRAM usage** when increasing workers/batch size
- **Test with short samples** before processing full books
- **Higher sensitivity = more variation** in speech

---

## Tab 3: Voice Analysis (Placeholder)

**Purpose**: This tab is a placeholder and not currently implemented.

**Status**: Coming in future updates  
**Planned Features**: 

- Voice sample analysis and quality assessment
- Frequency analysis and compatibility checking
- Voice cloning optimization recommendations

---

## Tab 4: Combine Audio

**Purpose**: Combine existing audio chunks into final audiobook without regenerating TTS.

### Step-by-Step Instructions

#### 1. **Select Book to Combine**

- **Available Books**: Dropdown shows books with processed audio chunks
- **Display Format**: "BookName (X chunks, HH:MM:SS duration)"
- **Manual Path**: Advanced users can enter custom paths
- **Book Info**: Detailed analysis appears when book is selected

#### 2. **Review Book Information**

The interface displays:

- **Total Chunks**: Number of audio segments
- **Total Duration**: Estimated playback time
- **Average Chunk**: Duration per segment
- **Existing Files**: Previously combined audiobooks
- **Location**: Directory path for verification

#### 3. **Optional Voice Naming**

- **Voice Name**: Optional identifier for output filename
- **If empty**: Uses "_combined" suffix
- **With name**: Creates "BookName [VoiceName].m4b"

#### 4. **Start Combination Process**

- Click "🔗 Combine Audio Chunks"
- **Background Processing**: Operation runs in separate thread
- **Progress Monitoring**: Real-time status updates
- **Stop Option**: Cancel operation if needed

#### 5. **Monitor Progress**

- **Status Display**: Current operation status
- **Progress Percentage**: Completion indicator
- **Current Book**: Shows which book is processing
- **Operation Time**: Elapsed time counter

#### 6. **Generated Files**

After completion:

- **WAV File**: Uncompressed audio (BookName_combined.wav)
- **M4B File**: Audiobook format with metadata
- **File Sizes**: Displayed in megabytes
- **Output Location**: `Audiobook/BookName/` directory

### Prerequisites

- Book must have processed audio chunks in `TTS/audio_chunks/`
- Chunk files named: `chunk_00001.wav`, `chunk_00002.wav`, etc.
- Metadata files (book.nfo, cover image) for M4B generation

### Expected Results

- High-quality combined audiobook
- Proper metadata and chapter marks
- Compatible with all audiobook players

---

## Tab 5: Prepare Text

**Purpose**: Prepare and analyze text files with VADER sentiment analysis for optimal TTS parameter assignment.

### Step-by-Step Instructions

#### 1. **Select Text File**

- **File Dropdown**: Shows available text files from `Text_Input/`
- **Display Format**: "BookName/filename.txt (XkB)"
- **Manual Path**: Direct file path input for advanced users
- **Refresh Button**: Update file list

#### 2. **Review File Analysis**

When file is selected, see:

- **Content Statistics**: Characters, words, lines, paragraphs
- **Estimated Chunks**: Approximate number of segments
- **Processing Status**: Ready/already processed indicator
- **Existing Files**: Previous processing results if any

#### 3. **Configure Base TTS Parameters**

Set baseline values for VADER adjustments:

- **Enable VADER**: Sentiment-based parameter modification
- **Base Exaggeration**: Starting exaggeration level (0.0-2.0)
- **Base CFG Weight**: Starting CFG guidance (0.0-1.0)
- **Base Temperature**: Starting randomness (0.0-2.0)
- **Min P, Top P, Repetition Penalty**: Advanced sampling parameters

#### 4. **Sentiment Analysis Settings**

Configure VADER processing:

- **Enable Sentiment Smoothing**: Smooth sentiment across chunks
  - **Smoothing Window**: Number of chunks to average (1-10)
  - **Smoothing Method**: Algorithm (gaussian/moving_average/exponential)

#### 5. **VADER Sensitivity Settings**

Control sentiment impact on TTS parameters:

- **Exaggeration Sensitivity**: How much sentiment affects drama (0.0-1.0)
- **CFG Sensitivity**: Sentiment impact on guidance (0.0-1.0)
- **Temperature Sensitivity**: Sentiment effect on randomness (0.0-1.0)
- **Higher values = more dramatic changes**

#### 6. **Start Text Preparation**

- Click "📝 Prepare Text for Chunking"
- **Progress Tracking**: Real-time status and progress bar
- **Background Processing**: Non-blocking operation
- **Stop Option**: Cancel if needed

#### 7. **Monitor Processing**

Watch for these stages:

1. **Analyzing text**: Reading and parsing content
2. **VADER sentiment analysis**: Applying sentiment scoring
3. **Generating enriched chunks**: Creating metadata
4. **Saving JSON**: Writing chunks_info.json

#### 8. **Results and Next Steps**

After completion:

- **Generated JSON**: `Audiobook/BookName/TTS/text_chunks/chunks_info.json`
- **Chunk Count**: Number of generated segments
- **Next Steps Guide**: Instructions for audiobook generation

#### 9. **Follow-up Options**

Use prepared text with:

- **Tab 1 (Convert Book)**: Full audiobook generation
- **Tab 8 (JSON Generate)**: Direct JSON-to-audio conversion

### Key Benefits

- **VADER Analysis**: Emotion-based TTS parameter adjustment
- **Optimized Chunks**: Smart text segmentation
- **Metadata Rich**: Per-chunk TTS parameters
- **Faster Generation**: Skip text processing in future runs

### Parameter Recommendations

- **First-time users**: Start with default values
- **Emotional content**: Higher VADER sensitivity (0.4-0.6)
- **Technical content**: Lower sensitivity (0.1-0.3)
- **Smooth delivery**: Enable sentiment smoothing

---

## Tab 6: Settings

**Purpose**: System settings and configuration management (simplified interface).

### Step-by-Step Instructions

#### 1. **Basic Configuration**

- **Model Settings**: Basic TTS model parameters
- **Output Settings**: File format and quality options
- **System Settings**: Performance and memory configuration

#### 2. **Apply Changes**

- Configure desired settings
- Click "Apply" to save changes
- Restart may be required for some settings

**Note**: This is a simplified settings interface. For comprehensive configuration, use **Tab 2: Configuration Settings**.

---

## Tab 7: Chunk Tools

**Purpose**: Interactive chunk editing, search, and audio regeneration for fine-tuning audiobook quality.

### Step-by-Step Instructions

#### 1. **Select Book for Editing**

- **Book Dropdown**: Shows books with processed chunks
- **Display Format**: "BookName (TTS: X chunks)" or "BookName (Text_Input: X chunks)"
- **Voice Detection**: Automatically detects candidate voices
- **Refresh Books**: Update available books list

#### 2. **Voice Selection**

After book selection:

- **Voice Candidates**: Shows detected voices with detection method
- **Selection Required**: Must select voice before resynthesizing audio
- **Re-detect Voices**: Refresh voice candidate list

#### 3. **Search for Chunks**

- **Search Text**: Enter text fragment to find
- **Search Button**: Execute search through all chunks
- **Results Display**: Shows matching chunks with previews
- **Chunk Dropdown**: Select specific chunk from results

#### 4. **Edit Selected Chunk**

When chunk is selected:

- **Chunk Information**: Index, boundary type, word count, sentiment, TTS params
- **Text Editor**: Modify chunk text content
- **Boundary Type**: Select chunk classification (paragraph_end, chapter_start, etc.)
- **TTS Parameters**: Adjust exaggeration, CFG weight, temperature

#### 5. **Audio Operations**

Available actions:

- **🔊 Play Original**: Play current chunk audio
- **💾 Save Changes**: Save text and parameter modifications
- **🎤 Resynthesize**: Generate new audio with updated parameters
- **🔊 Play Revised**: Play newly generated audio
- **✅ Accept Revision**: Confirm changes and update chunk

#### 6. **Resynthesis Process**

When regenerating audio:

1. Select voice from dropdown (required)
2. Modify text and/or TTS parameters
3. Click "🎤 Resynthesize"
4. Wait for generation completion
5. Use "🔊 Play Revised" to preview
6. Click "✅ Accept Revision" if satisfied

#### 7. **Operation Status**

Monitor operations through:

- **Status Display**: Current operation and results
- **Error Messages**: Clear problem descriptions
- **Success Confirmations**: Operation completion notices

### Use Cases

- **Fix Mispronunciations**: Edit text and regenerate specific chunks
- **Adjust Emotion**: Modify TTS parameters for better expression
- **Character Voices**: Apply different settings for dialogue
- **Quality Issues**: Identify and fix problematic audio segments

### Tips for Effective Editing

- **Small Changes**: Make incremental adjustments for better results
- **Test First**: Use short chunks to test parameter combinations
- **Voice Consistency**: Use same voice throughout book for consistency
- **Save Progress**: Save changes frequently to avoid data loss

---

## Tab 8: JSON Generate

**Purpose**: Generate audiobooks directly from preprocessed JSON files with advanced controls.

### Step-by-Step Instructions

#### 1. **Select JSON File**

- **JSON Dropdown**: Shows available chunk files
- **Display Format**: "BookName (X chunks)" from TTS or Text_Input directories
- **Manual Path**: Direct file path input
- **File Analysis**: Detailed JSON content information when selected

#### 2. **Review JSON Information**

File selection displays:

- **Source Location**: TTS processing or Text_Input directory
- **Content Analysis**: Total chunks, words, estimated duration
- **Processing Status**: Existing audio chunk count
- **Generation Ready**: Confirmation of JSON validity

#### 3. **Select Voice Sample**

- **Voice Dropdown**: Available voices from `Voice_Samples/` directory
- **Display Format**: "VoiceName (filename.wav)"
- **Refresh Voices**: Update voice sample list
- **Selection Required**: Must choose voice before generation

#### 4. **Generation Parameters**

- **Temperature Override**: Optional TTS temperature setting (0.0-2.0)
  - **0 = Use JSON values**: Preserves individual chunk parameters
  - **>0 = Global override**: Applies same temperature to all chunks

#### 5. **Start Generation**

- Click "🎵 Generate Audiobook from JSON"
- **Background Processing**: Non-blocking operation
- **Progress Tracking**: Real-time status and percentage
- **Stop Option**: Cancel generation if needed

#### 6. **Monitor Progress**

Track generation through:

- **Status Display**: Current operation phase
- **Progress Bar**: Completion percentage
- **Current File**: Selected JSON and voice information
- **Operation Status**: Ready/Processing/Completed state

#### 7. **Generated Output**

After completion:

- **Audiobook Files**: WAV and M4B formats
- **Output Location**: `Output/BookName/` directory
- **File Information**: Generated file paths and sizes
- **Access Instructions**: Download and playback guidance

#### 8. **File Access**

Generated files are saved to:

- **Individual Chunks**: `Audiobook/BookName/TTS/audio_chunks/`
- **Combined Audio**: `Output/BookName/BookName_combined.wav`
- **Audiobook Format**: `Output/BookName/BookName_combined.m4b`

### Advantages of JSON Generation

- **Speed**: Bypasses text processing and chunking
- **Precision**: Uses exact parameters from JSON
- **Flexibility**: Easy parameter editing in JSON files
- **Debugging**: Test specific chunks with custom settings
- **Reproducibility**: Identical results from same JSON/voice combination

### When to Use JSON Generate

- **Parameter Testing**: Experiment with TTS settings
- **Selective Regeneration**: Update specific sections
- **Advanced Users**: Direct control over generation process
- **Debugging**: Isolate and fix problematic chunks

### Temperature Override Usage

- **Leave at 0**: Use individual chunk parameters from JSON
- **Set to specific value**: Apply same temperature to entire audiobook
- **Useful for**: Testing global temperature effects on voice consistency

---

## Tab 9: System Monitor (Placeholder)

**Purpose**: This tab is a placeholder and not currently implemented.

**Status**: Coming in future updates  
**Planned Features**: 

- Real-time system performance monitoring
- GPU/VRAM usage tracking
- Processing queue status
- System resource optimization recommendations

---

## Tab 10: About (Placeholder)

**Purpose**: This tab is a placeholder and not currently implemented.

**Status**: Coming in future updates  
**Planned Features**: 

- Application version and build information
- Credits and acknowledgments
- License information
- Documentation links and support resources

---

## Troubleshooting

### Common Issues and Solutions

#### "Tab Not Available" Errors

**Problem**: Tab shows as "❌ Not Available"  
**Solutions**:

- Check that all backend modules are properly installed
- Verify Python environment and dependencies
- Review console output for specific import errors
- Ensure configuration files are present

#### File Selection Issues

**Problem**: Files don't appear in dropdowns  
**Solutions**:

- Check directory structure: `Text_Input/BookName/book.txt`
- Verify file permissions and accessibility
- Use "Refresh" buttons to update file lists
- Check file formats (TXT for books, WAV for voices)

#### Processing Failures

**Problem**: Generation stops or fails with errors  
**Solutions**:

- Check available disk space and memory
- Monitor GPU/VRAM usage during processing
- Reduce batch size or workers if memory issues
- Verify voice sample quality and format

#### Audio Quality Issues

**Problem**: Poor audio quality or artifacts  
**Solutions**:

- Check voice sample quality (24kHz recommended)
- Adjust TTS parameters (lower temperature for consistency)
- Verify chunk text doesn't have formatting issues
- Use chunk editing tools to fix specific segments

#### Web Interface Problems

**Problem**: Interface doesn't load or responds slowly  
**Solutions**:

- Refresh browser page
- Clear browser cache and cookies
- Check browser JavaScript console for errors
- Try different web browser
- Verify server is running on correct port

### Getting Help

- Review console output for detailed error messages
- Check processing logs in `Audiobook/BookName/run.log`
- Use chunk tools to isolate and debug specific issues
- Verify all prerequisites and system requirements

---

## Best Practices

### Workflow Recommendations

#### 1. **Preparation Workflow**

**For first-time users**:

1. Start with **Tab 2: Configuration** to set optimal parameters
2. Use **Tab 5: Prepare Text** to analyze and chunk your text
3. Generate audiobook with **Tab 1: Convert Book**
4. Use **Tab 4: Combine Audio** if you need different combinations
5. Fine-tune with **Tab 7: Chunk Tools** if needed

#### 2. **Quality Optimization**

**For best results**:

- Use high-quality voice samples (24kHz, clear speech, minimal background noise)
- Start with default parameters and adjust gradually
- Test short sections before processing entire books
- Use VADER analysis for emotional content
- Apply sentiment smoothing for consistent delivery

#### 3. **Performance Optimization**

**For faster processing**:

- Monitor VRAM usage and adjust workers accordingly
- Use higher batch sizes if memory permits
- Consider text preparation first for multiple generation runs
- Use JSON generation for parameter testing and debugging

#### 4. **File Organization**

**Recommended structure**:

```
Text_Input/
├── BookName1/
│   ├── book.txt
│   ├── cover.jpg (optional)
│   └── book.nfo (optional)
├── BookName2/
│   └── book.txt
Voice_Samples/
├── voice1.wav
├── voice2.wav
Output/
├── BookName1/
│   ├── BookName1_combined.wav
│   └── BookName1_combined.m4b
```

### Parameter Guidelines

#### **TTS Parameters**

- **Temperature**: 0.6-1.0 for most content, 0.8 recommended
- **CFG Weight**: 0.4-0.6 for balanced guidance
- **Exaggeration**: 0.4-0.6 for natural speech, higher for dramatic content

#### **VADER Settings**

- **Sensitivity**: 0.2-0.4 for subtle adjustments, 0.1-0.2 for minimal variation
- **Smoothing**: Enable for consistent emotional flow
- **Window Size**: 3-5 chunks for most content

#### **System Settings**

- **Workers**: Start with 2, increase if VRAM usage < 60%
- **Batch Size**: 100-200 for most systems
- **Memory**: Monitor usage and adjust if processing fails

### Quality Assurance

#### **Before Generation**

- Verify text file quality (proper punctuation, no formatting artifacts)
- Test voice sample quality and compatibility
- Configure parameters appropriate for content type
- Ensure sufficient disk space for output files

#### **During Generation**

- Monitor progress and system resources
- Watch for consistent processing speed
- Check for error messages or warnings
- Be prepared to stop and adjust if issues arise

#### **After Generation**

- Listen to sample sections for quality assessment
- Check file completeness and proper duration
- Verify metadata and chapter marks in M4B files
- Use chunk tools to fix any identified issues

### Maintenance and Updates

#### **Regular Maintenance**

- Clear temporary files periodically
- Update voice samples as needed
- Review and adjust configuration based on results
- Keep backups of successful parameter combinations

#### **Performance Monitoring**

- Track processing times and resource usage
- Note successful parameter combinations for future use
- Document any custom settings or optimizations
- Regular testing with small samples to verify system health

This comprehensive manual provides step-by-step instructions for every functional tab in the ChatterboxTTS Gradio interface. Each section includes detailed procedures, troubleshooting guidance, and best practices for optimal results.