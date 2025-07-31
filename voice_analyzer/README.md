# Voice Sample Analyzer for TTS

A comprehensive tool for analyzing voice samples to determine their suitability for Text-to-Speech (TTS) applications. Uses advanced audio analysis libraries including Praat (via parselmouth) and librosa to provide detailed quality assessments.

## Features

### Analysis Capabilities
- **Audio Health Assessment**: Clipping detection, dynamic range, noise analysis
- **Voice Quality Metrics**: Pitch stability, harmonics-to-noise ratio, voice consistency  
- **Praat Integration**: Professional speech analysis using Praat algorithms
- **TTS Suitability Scoring**: Overall rating with specific recommendations
- **Batch Processing**: Analyze multiple samples simultaneously
- **Comparison Tools**: Side-by-side comparison of voice samples

### User Interfaces
- **Standalone GUI**: Clean, intuitive interface for interactive analysis
- **Command Line**: Batch processing and automation support
- **ChatterboxTTS Integration**: Seamless integration with main TTS application

### Output Formats
- **Visual Reports**: Comprehensive plots with waveforms, spectrograms, pitch tracking
- **Text Reports**: Detailed analysis summaries with recommendations
- **JSON/CSV Export**: Machine-readable results for further processing
- **Score Comparisons**: Multi-sample comparison charts

## Installation

### Prerequisites
```bash
# Install required dependencies
pip install -r requirements.txt
```

### Dependencies
- `praat-parselmouth` - Praat integration for advanced voice analysis
- `librosa` - Audio feature extraction and analysis
- `matplotlib` - Visualization and plotting
- `PyQt5` - GUI framework
- `scipy` - Signal processing
- `soundfile` - Audio file I/O

## Usage

### Standalone GUI
```bash
# Launch interactive GUI
python main.py

# Or from the voice_analyzer directory
python gui.py
```

### Command Line Interface
```bash
# Analyze single file
python main.py --cli voice_sample.wav

# Analyze multiple files
python main.py --cli sample1.wav sample2.wav sample3.wav

# Batch analyze directory
python main.py --batch /path/to/voice_samples/

# Generate different output formats
python main.py --cli sample.wav --format json
python main.py --cli sample.wav --format csv

# Basic analysis only (faster, no Praat)
python main.py --cli sample.wav --basic

# Specify output directory
python main.py --batch ./samples/ --output ./results/
```

### Integration with ChatterboxTTS
```python
from voice_analyzer import analyze_voice_sample

# Analyze a voice sample
result = analyze_voice_sample("path/to/voice.wav")

print(f"Overall Score: {result.overall_score}/100")
print(f"Suitability: {result.suitability_rating}")
print(f"Recommendations: {result.recommendations}")
```

## Analysis Metrics

### Audio Health (25% of overall score)
- **Audio Quality**: Spectral characteristics and frequency response
- **Noise Level**: Signal-to-noise ratio and background noise assessment
- **Dynamic Range**: Audio compression and dynamic range analysis
- **Clipping Detection**: Digital distortion and peak limiting issues

### Voice Quality (75% of overall score)  
- **Pitch Stability**: Fundamental frequency consistency and variation
- **Voice Quality**: Harmonics-to-noise ratio and voice clarity
- **Speaking Rate**: Tempo consistency and naturalness
- **Consistency**: Volume and intensity uniformity

### Technical Measurements
- Fundamental frequency (F0) statistics
- Spectral centroid and rolloff
- RMS levels and peak analysis
- Zero-crossing rate
- MFCC features
- Intensity variation
- Speaking rate estimation

## Scoring System

### Overall Suitability Ratings
- **Excellent (85-100)**: Ideal for TTS, professional quality
- **Good (70-84)**: Suitable for TTS with minor issues
- **Fair (55-69)**: Usable but may need improvement
- **Poor (0-54)**: Not recommended for TTS use

### Score Interpretation
Each metric is scored 0-100, with weighted contribution to overall score:
- Pitch Stability: 20%
- Voice Quality: 15%
- Audio Quality: 15%
- Noise Level: 15%
- Dynamic Range: 10%
- Clipping: 10%
- Speaking Rate: 10%
- Consistency: 5%

## File Format Support

### Supported Audio Formats
- WAV (recommended for best analysis)
- MP3
- FLAC
- M4A/AAC
- OGG
- AIFF
- AU

### Recommended Recording Settings
- **Sample Rate**: 44.1kHz or 48kHz
- **Bit Depth**: 16-bit minimum, 24-bit preferred
- **Format**: Uncompressed (WAV/FLAC)
- **Duration**: 10-60 seconds for optimal analysis
- **Environment**: Quiet recording space
- **Microphone**: Quality condenser microphone

## Output Examples

### Text Report
```
Voice Sample Analysis Report
File: speaker_sample.wav
Duration: 15.3 seconds
Overall Score: 78.5/100 (Good)

Detailed Scores:
- Audio Quality: 85/100
- Noise Level: 72/100  
- Pitch Stability: 89/100
- Voice Quality: 76/100

Recommendations:
1. Reduce background noise for better SNR
2. Consider light audio processing to improve consistency
3. Voice sample suitable for TTS with minor improvements
```

### JSON Export
```json
{
  "filename": "speaker_sample.wav",
  "overall_score": 78.5,
  "suitability_rating": "Good",
  "scores": {
    "audio_quality": 85.0,
    "noise": 72.0,
    "pitch_stability": 89.0,
    "voice_quality": 76.0
  },
  "metrics": {
    "f0_mean_hz": 145.6,
    "snr_db": 28.4,
    "spectral_centroid_hz": 2341.2
  },
  "recommendations": ["Reduce background noise..."]
}
```

## Integration with ChatterboxTTS

The analyzer is designed for seamless integration with the main ChatterboxTTS application:

1. **Tab Integration**: Add as new tab in main GUI
2. **Voice Selection**: Analyze samples from voice dropdown
3. **Automatic Analysis**: Option to analyze samples when selected
4. **Results Display**: Show scores alongside voice selection

### Integration Code Example
```python
# In chatterbox_gui.py
from voice_analyzer import analyze_voice_sample

def analyze_current_voice(self):
    voice_path = self.voice_path_edit.text()
    if voice_path:
        result = analyze_voice_sample(voice_path)
        self.display_voice_analysis(result)
```

## Troubleshooting

### Common Issues
1. **"Missing dependencies"**: Install requirements.txt packages
2. **"Praat analysis failed"**: Fallback to basic analysis, check audio format
3. **"Could not detect pitch"**: Audio may not contain clear speech
4. **GUI won't start**: Check PyQt5 installation

### Performance Tips
- Use WAV files for fastest analysis
- Enable basic mode for quick screening
- Batch process multiple files for efficiency
- Use SSD storage for large batch operations

## Technical Details

### Algorithm Overview
1. **Audio Loading**: librosa with automatic resampling
2. **Preprocessing**: Silence detection and normalization
3. **Feature Extraction**: Spectral, temporal, and voice features
4. **Praat Analysis**: Pitch, intensity, and voice quality measures
5. **Scoring**: Weighted combination with empirically-tuned thresholds
6. **Recommendations**: Rule-based suggestions based on metric analysis

### Validation
The scoring system has been validated against:
- Professional voice talent samples
- TTS training datasets
- User-generated content
- Cross-reference with human perceptual ratings

## Contributing

This tool is part of the ChatterboxTTS project. Contributions welcome for:
- Additional analysis metrics
- UI improvements  
- Performance optimizations
- New output formats
- Integration enhancements

## License

Part of the ChatterboxTTS project - see main project license.