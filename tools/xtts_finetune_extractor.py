#!/usr/bin/env python3
"""
XTTS-Finetune Audio Extractor for ChatterboxTTS
Extracts emotive audio samples from XTTS-finetune model data.

This tool:
1. Analyzes XTTS-finetune directory structure  
2. Extracts and analyzes WAV files for emotional content
3. Uses vocab/metadata if available
4. Creates optimized voice samples for ChatterboxTTS cloning

Note: XTTS-finetune models are not compatible with ChatterboxTTS, but we can
extract the training audio data for voice sample creation.
"""

import json
import os
import sys
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import argparse
import re
from collections import defaultdict
import logging

# Try to import VADER, use fallback if not available
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    print("⚠️  VADER not available - using basic emotional analysis")
    VADER_AVAILABLE = False
    
    class SentimentIntensityAnalyzer:
        """Fallback sentiment analyzer when VADER is not available."""
        def polarity_scores(self, text):
            # Basic keyword-based sentiment analysis
            positive_words = ['happy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'love', 'joy']
            negative_words = ['sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'disgusting', 'horrible']
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                compound = min(0.8, pos_count * 0.3)
            elif neg_count > pos_count:
                compound = max(-0.8, -neg_count * 0.3)
            else:
                compound = 0.0
            
            return {'compound': compound}

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class XTTSAudioFile:
    """Represents an audio file from XTTS-finetune data."""
    file_path: str
    text: Optional[str] = None
    duration: float = 0.0
    sample_rate: int = 0
    emotion_score: float = 0.0
    emotion_type: str = "neutral"
    quality_score: float = 0.0
    speaker_id: Optional[str] = None

class XTTSFinetuneExtractor:
    """Main class for extracting audio from XTTS-finetune model data."""
    
    # Emotional classification thresholds (using VADER)
    EMOTION_THRESHOLDS = {
        'very_positive': 0.5,
        'positive': 0.1,
        'neutral': 0.05,
        'negative': -0.1,
        'very_negative': -0.5,
    }
    
    # Expected XTTS-finetune file patterns
    COMMON_PATTERNS = {
        'vocab': ['vocab.json', 'vocabulary.json', 'tokens.json'],
        'model': ['model.pth', 'checkpoint.pth', 'pytorch_model.bin'],
        'config': ['config.json', 'speaker_config.json', 'training_config.json'],
        'audio': ['wavs/', 'audio/', 'samples/', 'training_data/'],
        'metadata': ['metadata.csv', 'train.txt', 'filelist.txt', 'speakers.json']
    }
    
    def __init__(self, xtts_dir: str):
        """
        Initialize the XTTS-finetune extractor.
        
        Args:
            xtts_dir: Path to XTTS-finetune model directory
        """
        self.xtts_dir = Path(xtts_dir)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.audio_files = []
        self.metadata = {}
        
        if not self.xtts_dir.exists():
            raise FileNotFoundError(f"XTTS directory not found: {self.xtts_dir}")
    
    def analyze_directory_structure(self) -> Dict[str, List[str]]:
        """
        Analyze the XTTS-finetune directory structure.
        
        Returns:
            Dictionary mapping file types to found files
        """
        found_files = {key: [] for key in self.COMMON_PATTERNS.keys()}
        
        logging.info(f"Analyzing directory structure: {self.xtts_dir}")
        
        # Walk through all files and directories
        for root, dirs, files in os.walk(self.xtts_dir):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                file_lower = file.lower()
                
                # Check for vocab files
                if any(pattern in file_lower for pattern in self.COMMON_PATTERNS['vocab']):
                    found_files['vocab'].append(str(file_path))
                
                # Check for model files
                elif any(pattern in file_lower for pattern in self.COMMON_PATTERNS['model']):
                    found_files['model'].append(str(file_path))
                
                # Check for config files
                elif any(pattern in file_lower for pattern in self.COMMON_PATTERNS['config']):
                    found_files['config'].append(str(file_path))
                
                # Check for metadata files (including _train.csv, _eval.csv patterns)
                elif (any(pattern in file_lower for pattern in self.COMMON_PATTERNS['metadata']) or
                      file_lower.endswith('_train.csv') or file_lower.endswith('_eval.csv') or
                      'metadata' in file_lower):
                    found_files['metadata'].append(str(file_path))
                
                # Check for audio files
                elif file_lower.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                    found_files['audio'].append(str(file_path))
            
            # Check for audio directories
            for dir_name in dirs:
                if any(pattern.rstrip('/') in dir_name.lower() for pattern in self.COMMON_PATTERNS['audio']):
                    audio_dir = root_path / dir_name
                    # Find audio files in this directory
                    for audio_file in audio_dir.rglob('*.wav'):
                        found_files['audio'].append(str(audio_file))
        
        # Log findings
        for file_type, files in found_files.items():
            if files:
                logging.info(f"Found {len(files)} {file_type} files")
                for file in files[:3]:  # Show first 3
                    logging.info(f"  - {file}")
                if len(files) > 3:
                    logging.info(f"  ... and {len(files) - 3} more")
        
        return found_files
    
    def load_metadata(self, metadata_files: List[str]) -> Dict[str, str]:
        """
        Load metadata from various formats.
        
        Args:
            metadata_files: List of metadata file paths
            
        Returns:
            Dictionary mapping audio filename to text content
        """
        text_mapping = {}
        
        for metadata_file in metadata_files:
            try:
                logging.info(f"Loading metadata from: {metadata_file}")
                
                if metadata_file.endswith('.json'):
                    # JSON format
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict):
                        # Direct mapping format
                        for key, value in data.items():
                            if isinstance(value, str):
                                text_mapping[key] = value
                            elif isinstance(value, dict) and 'text' in value:
                                text_mapping[key] = value['text']
                
                elif metadata_file.endswith('.csv'):
                    # CSV format (common in TTS datasets)
                    import csv
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if len(row) >= 2:
                                filename = row[0]
                                text = row[1] if len(row) > 1 else ""
                                text_mapping[filename] = text
                
                elif metadata_file.endswith('.txt'):
                    # Text filelist format (filename|text)
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if '|' in line:
                                parts = line.split('|', 1)
                                filename = parts[0].strip()
                                text = parts[1].strip() if len(parts) > 1 else ""
                                text_mapping[filename] = text
                
                logging.info(f"Loaded {len(text_mapping)} text mappings from {metadata_file}")
                
            except Exception as e:
                logging.warning(f"Could not load metadata from {metadata_file}: {e}")
        
        return text_mapping
    
    def analyze_audio_file(self, audio_path: str, text: Optional[str] = None) -> XTTSAudioFile:
        """
        Analyze a single audio file for quality and emotional content.
        
        Args:
            audio_path: Path to audio file
            text: Associated text content (if available)
            
        Returns:
            XTTSAudioFile object with analysis results
        """
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            
            # Create base file object
            audio_file = XTTSAudioFile(
                file_path=audio_path,
                text=text,
                duration=duration,
                sample_rate=sr
            )
            
            # Quality analysis
            audio_file.quality_score = self.assess_audio_quality(audio, sr)
            
            # Emotional analysis (if text available)
            if text:
                sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
                audio_file.emotion_score = sentiment_scores['compound']
                audio_file.emotion_type = self.classify_emotion(audio_file.emotion_score)
            
            return audio_file
            
        except Exception as e:
            logging.warning(f"Error analyzing {audio_path}: {e}")
            return XTTSAudioFile(file_path=audio_path, text=text)
    
    def assess_audio_quality(self, audio: np.ndarray, sr: int) -> float:
        """
        Assess audio quality using various metrics.
        
        Args:
            audio: Audio data
            sr: Sample rate
            
        Returns:
            Quality score (0-1, higher is better)
        """
        scores = []
        
        # Duration score (prefer 2-10 second clips)
        duration = len(audio) / sr
        if 2.0 <= duration <= 10.0:
            duration_score = 1.0
        elif duration < 2.0:
            duration_score = duration / 2.0
        else:
            duration_score = max(0.3, 10.0 / duration)
        scores.append(duration_score)
        
        # RMS energy score
        rms = librosa.feature.rms(y=audio)[0]
        mean_rms = np.mean(rms)
        if 0.01 <= mean_rms <= 0.5:
            rms_score = 1.0
        else:
            rms_score = max(0.2, min(1.0, mean_rms / 0.3))
        scores.append(rms_score)
        
        # Zero-crossing rate (speech characteristics)
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        mean_zcr = np.mean(zcr)
        if 0.02 <= mean_zcr <= 0.15:
            zcr_score = 1.0
        else:
            zcr_score = max(0.3, 1.0 - abs(mean_zcr - 0.085) / 0.085)
        scores.append(zcr_score)
        
        # Spectral centroid (tonal quality)
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        mean_centroid = np.mean(spectral_centroids)
        if 500 <= mean_centroid <= 4000:
            spectral_score = 1.0
        else:
            spectral_score = max(0.2, 1.0 - abs(mean_centroid - 2250) / 2250)
        scores.append(spectral_score)
        
        # Combined score
        return np.mean(scores)
    
    def classify_emotion(self, sentiment_score: float) -> str:
        """Classify VADER sentiment score into emotional categories."""
        if sentiment_score >= self.EMOTION_THRESHOLDS['very_positive']:
            return 'very_positive'
        elif sentiment_score >= self.EMOTION_THRESHOLDS['positive']:
            return 'positive'
        elif sentiment_score >= self.EMOTION_THRESHOLDS['neutral']:
            return 'neutral'
        elif sentiment_score >= self.EMOTION_THRESHOLDS['negative']:
            return 'negative'
        else:
            return 'very_negative'
    
    def extract_audio_files(self, audio_files: List[str], text_mapping: Dict[str, str]) -> List[XTTSAudioFile]:
        """
        Extract and analyze all audio files.
        
        Args:
            audio_files: List of audio file paths
            text_mapping: Dictionary mapping filenames to text
            
        Returns:
            List of analyzed XTTSAudioFile objects
        """
        analyzed_files = []
        
        logging.info(f"Analyzing {len(audio_files)} audio files...")
        
        for i, audio_path in enumerate(audio_files):
            if i % 50 == 0:
                logging.info(f"Progress: {i}/{len(audio_files)} files analyzed")
            
            # Find associated text
            filename = Path(audio_path).stem
            text = None
            
            # Try various filename matching strategies
            for key in text_mapping.keys():
                if key == filename or key == Path(audio_path).name or filename in key:
                    text = text_mapping[key]
                    break
            
            # Analyze the audio file
            analyzed_file = self.analyze_audio_file(audio_path, text)
            analyzed_files.append(analyzed_file)
        
        logging.info(f"Analysis complete. {len(analyzed_files)} files processed.")
        return analyzed_files
    
    def select_best_samples(self, audio_files: List[XTTSAudioFile], max_per_emotion: int = 5) -> Dict[str, List[XTTSAudioFile]]:
        """
        Select the best audio samples for each emotion.
        
        Args:
            audio_files: List of analyzed audio files
            max_per_emotion: Maximum samples per emotion
            
        Returns:
            Dictionary mapping emotion types to best samples
        """
        # Filter by quality threshold
        quality_files = [f for f in audio_files if f.quality_score > 0.3]
        
        logging.info(f"Selected {len(quality_files)}/{len(audio_files)} files above quality threshold")
        
        # Group by emotion
        emotion_groups = defaultdict(list)
        for file in quality_files:
            emotion_groups[file.emotion_type].append(file)
        
        # Select best samples for each emotion
        best_samples = {}
        for emotion, files in emotion_groups.items():
            # Sort by combined quality and sentiment extremity
            def score_file(f):
                sentiment_extremity = abs(f.emotion_score)
                return f.quality_score * 0.7 + sentiment_extremity * 0.3
            
            files.sort(key=score_file, reverse=True)
            best_samples[emotion] = files[:max_per_emotion]
            
            logging.info(f"Selected {len(best_samples[emotion])} best samples for {emotion}")
        
        return best_samples
    
    def create_voice_samples(self, best_samples: Dict[str, List[XTTSAudioFile]], output_dir: str) -> Dict[str, str]:
        """
        Create combined voice samples for each emotion.
        
        Args:
            best_samples: Dictionary of emotion -> best audio files
            output_dir: Output directory for voice samples
            
        Returns:
            Dictionary mapping emotion -> output file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        voice_samples = {}
        target_duration = 10.0  # 10 second samples
        
        for emotion, files in best_samples.items():
            if not files:
                continue
            
            combined_audio = []
            current_duration = 0.0
            used_files = []
            
            # Combine audio files until we reach target duration
            for audio_file in files:
                if current_duration >= target_duration:
                    break
                
                try:
                    audio, sr = librosa.load(audio_file.file_path, sr=22050)
                    file_duration = len(audio) / sr
                    
                    # Trim if needed
                    remaining_time = target_duration - current_duration
                    if file_duration > remaining_time:
                        samples_needed = int(remaining_time * sr)
                        audio = audio[:samples_needed]
                        file_duration = remaining_time
                    
                    combined_audio.extend(audio)
                    current_duration += file_duration
                    used_files.append(audio_file)
                    
                except Exception as e:
                    logging.warning(f"Error loading {audio_file.file_path}: {e}")
                    continue
            
            if not combined_audio:
                continue
            
            # Pad with silence if needed
            if current_duration < target_duration:
                silence_duration = target_duration - current_duration
                silence_samples = int(silence_duration * sr)
                combined_audio.extend([0.0] * silence_samples)
            
            # Save combined sample
            combined_audio = np.array(combined_audio)
            output_file = output_dir / f"xtts_voice_sample_{emotion}.wav"
            sf.write(output_file, combined_audio, sr)
            
            voice_samples[emotion] = str(output_file)
            
            logging.info(f"Created {emotion} voice sample: {output_file}")
            logging.info(f"  Duration: {len(combined_audio)/sr:.1f}s | Files used: {len(used_files)}")
        
        return voice_samples
    
    def generate_report(self, structure: Dict[str, List[str]], audio_files: List[XTTSAudioFile], 
                       best_samples: Dict[str, List[XTTSAudioFile]], voice_samples: Dict[str, str], 
                       output_dir: str):
        """Generate a detailed extraction report."""
        report_file = Path(output_dir) / "xtts_extraction_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("# XTTS-Finetune Audio Extraction Report\n\n")
            f.write(f"Source Directory: {self.xtts_dir}\n")
            f.write(f"Total Audio Files Found: {len(audio_files)}\n\n")
            
            # Directory structure
            f.write("## Directory Structure Analysis\n\n")
            for file_type, files in structure.items():
                f.write(f"**{file_type.title()}**: {len(files)} files\n")
                for file in files[:3]:
                    f.write(f"  - {file}\n")
                if len(files) > 3:
                    f.write(f"  ... and {len(files) - 3} more\n")
                f.write("\n")
            
            # Audio analysis
            f.write("## Audio Analysis Summary\n\n")
            quality_files = [af for af in audio_files if af.quality_score > 0.3]
            with_text = [af for af in audio_files if af.text]
            
            f.write(f"- High quality files (>0.3): {len(quality_files)}\n")
            f.write(f"- Files with text: {len(with_text)}\n")
            f.write(f"- Average duration: {np.mean([af.duration for af in audio_files]):.1f}s\n")
            f.write(f"- Average quality score: {np.mean([af.quality_score for af in audio_files]):.2f}\n\n")
            
            # Emotion distribution
            f.write("## Emotion Distribution\n\n")
            emotion_counts = defaultdict(int)
            for audio_file in audio_files:
                emotion_counts[audio_file.emotion_type] += 1
            
            for emotion, count in emotion_counts.items():
                percentage = (count / len(audio_files)) * 100
                f.write(f"- {emotion}: {count} files ({percentage:.1f}%)\n")
            
            # Best samples
            f.write("\n## Selected Best Samples\n\n")
            for emotion, samples in best_samples.items():
                f.write(f"### {emotion.upper()}\n")
                for i, sample in enumerate(samples):
                    f.write(f"{i+1}. {Path(sample.file_path).name} | quality: {sample.quality_score:.2f} | "
                           f"sentiment: {sample.emotion_score:+.3f}\n")
                    if sample.text:
                        f.write(f"   \"{sample.text[:80]}...\"\n")
                f.write("\n")
            
            # Generated samples
            f.write("## Generated Voice Samples\n\n")
            for emotion, file_path in voice_samples.items():
                f.write(f"- {emotion}: {file_path}\n")
        
        logging.info(f"Report saved: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract emotive audio from XTTS-finetune model data")
    parser.add_argument("xtts_dir", help="Path to XTTS-finetune model directory")
    parser.add_argument("-o", "--output", default="xtts_extracted_samples", help="Output directory")
    parser.add_argument("--max-per-emotion", type=int, default=5, help="Max samples per emotion")
    
    args = parser.parse_args()
    
    try:
        print(f"🎭 Starting XTTS-finetune audio extraction from {args.xtts_dir}")
        
        # Initialize extractor
        extractor = XTTSFinetuneExtractor(args.xtts_dir)
        
        # Analyze directory structure
        structure = extractor.analyze_directory_structure()
        
        # Load metadata
        text_mapping = extractor.load_metadata(structure.get('metadata', []))
        
        # Extract and analyze audio files
        audio_files = extractor.extract_audio_files(structure.get('audio', []), text_mapping)
        
        if not audio_files:
            print("❌ No audio files found in the directory")
            return 1
        
        # Select best samples
        best_samples = extractor.select_best_samples(audio_files, args.max_per_emotion)
        
        # Create voice samples
        voice_samples = extractor.create_voice_samples(best_samples, args.output)
        
        # Generate report
        extractor.generate_report(structure, audio_files, best_samples, voice_samples, args.output)
        
        print(f"\n✅ XTTS extraction complete!")
        print(f"📁 Output directory: {args.output}")
        print(f"🎯 Generated {len(voice_samples)} emotional voice samples")
        
        for emotion, path in voice_samples.items():
            print(f"   {emotion}: {Path(path).name}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.exception("Full error details:")
        return 1

if __name__ == "__main__":
    sys.exit(main())