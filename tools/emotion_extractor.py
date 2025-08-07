#!/usr/bin/env python3
"""
Emotion Extractor for ChatterboxTTS
Mines existing TTS output to extract emotional voice samples from raw VADER sentiment data.

This tool:
1. Parses chunk JSON files with raw VADER sentiment scores
2. Maps sentiment to distinct emotional states  
3. Identifies best examples of each emotion
4. Extracts and combines audio segments into optimized 10-second voice samples
"""

import json
import os
import sys
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import argparse

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class EmotionalSegment:
    """Represents an audio segment with its emotional characteristics."""
    chunk_index: int
    text: str
    raw_sentiment: float
    emotional_state: str
    audio_path: str
    start_time: float = 0.0
    duration: float = 0.0
    quality_score: float = 0.0
    tts_params: Dict = None

class EmotionExtractor:
    """Main class for extracting emotional voice samples from TTS output."""
    
    # Emotional state mapping based on VADER compound scores
    EMOTION_THRESHOLDS = {
        'very_positive': 0.5,    # Joy, excitement, enthusiasm  
        'positive': 0.1,         # Happy, content, pleased
        'neutral': 0.05,         # Calm, matter-of-fact, narrative
        'negative': -0.1,        # Sad, concerned, disappointed
        'very_negative': -0.5,   # Anger, fear, despair, intense emotion
    }
    
    # Target durations for each emotional state (seconds)
    TARGET_DURATIONS = {
        'very_positive': 2.0,
        'positive': 2.0, 
        'neutral': 3.0,     # Longest - base voice characteristic
        'negative': 2.0,
        'very_negative': 1.5,  # Shortest - intense emotions
    }
    
    def __init__(self, audiobook_dir: str, min_segment_duration: float = 0.8):
        """
        Initialize the emotion extractor.
        
        Args:
            audiobook_dir: Path to audiobook directory containing TTS/ folder
            min_segment_duration: Minimum audio segment length to consider (seconds)
        """
        self.audiobook_dir = Path(audiobook_dir)
        self.min_segment_duration = min_segment_duration
        self.chunks_info_path = self.audiobook_dir / "TTS" / "text_chunks" / "chunks_info.json"
        self.audio_chunks_dir = self.audiobook_dir / "TTS" / "audio_chunks"
        
        # Verify paths exist
        if not self.chunks_info_path.exists():
            raise FileNotFoundError(f"chunks_info.json not found at {self.chunks_info_path}")
        if not self.audio_chunks_dir.exists():
            raise FileNotFoundError(f"Audio chunks directory not found at {self.audio_chunks_dir}")
    
    def classify_emotion(self, sentiment_score: float) -> str:
        """Classify VADER sentiment score into discrete emotional states."""
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
    
    def load_chunk_data(self) -> List[EmotionalSegment]:
        """Load and parse chunk data from JSON file."""
        with open(self.chunks_info_path, 'r') as f:
            chunks_data = json.load(f)
        
        segments = []
        for chunk in chunks_data:
            # Look for audio file
            chunk_idx = chunk['index']
            audio_file = self.audio_chunks_dir / f"chunk_{chunk_idx:05d}.wav"
            
            if not audio_file.exists():
                print(f"⚠️  Audio file missing for chunk {chunk_idx}: {audio_file}")
                continue
            
            # Create emotional segment
            segment = EmotionalSegment(
                chunk_index=chunk_idx,
                text=chunk['text'],
                raw_sentiment=chunk['sentiment_compound'],
                emotional_state=self.classify_emotion(chunk['sentiment_compound']),
                audio_path=str(audio_file),
                tts_params=chunk.get('tts_params', {})
            )
            
            segments.append(segment)
        
        print(f"📊 Loaded {len(segments)} audio segments from {len(chunks_data)} chunks")
        return segments
    
    def analyze_audio_quality(self, segment: EmotionalSegment) -> float:
        """
        Analyze audio quality and return a score (0-1, higher is better).
        
        Considers:
        - Audio duration (prefer 1-4 seconds)
        - RMS energy (avoid too quiet/loud)  
        - Zero-crossing rate (speech-like characteristics)
        - Spectral characteristics
        """
        try:
            audio, sr = librosa.load(segment.audio_path, sr=None)
            duration = len(audio) / sr
            segment.duration = duration
            
            # Skip too short segments
            if duration < self.min_segment_duration:
                return 0.0
            
            # Duration score (prefer 1-4 second segments)
            if 1.0 <= duration <= 4.0:
                duration_score = 1.0
            elif duration < 1.0:
                duration_score = duration / 1.0  # Linear penalty for short
            else:
                duration_score = max(0.3, 4.0 / duration)  # Penalty for long
            
            # Energy analysis
            rms = librosa.feature.rms(y=audio)[0]
            mean_rms = np.mean(rms)
            
            # Energy score (avoid very quiet or very loud)
            if 0.01 <= mean_rms <= 0.3:
                energy_score = 1.0
            elif mean_rms < 0.01:
                energy_score = mean_rms / 0.01  # Too quiet
            else:
                energy_score = max(0.2, 0.3 / mean_rms)  # Too loud
            
            # Speech characteristics (zero-crossing rate)
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            mean_zcr = np.mean(zcr)
            
            # ZCR score (speech typically 0.02-0.15)
            if 0.02 <= mean_zcr <= 0.15:
                zcr_score = 1.0
            else:
                zcr_score = max(0.3, 1.0 - abs(mean_zcr - 0.085) / 0.085)
            
            # Spectral centroid (tonal quality)
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            mean_centroid = np.mean(spectral_centroids)
            
            # Prefer human speech range (roughly 500-4000 Hz)
            if 500 <= mean_centroid <= 4000:
                spectral_score = 1.0
            else:
                spectral_score = max(0.2, 1.0 - abs(mean_centroid - 2250) / 2250)
            
            # Combined quality score (weighted average)
            quality_score = (
                duration_score * 0.3 +
                energy_score * 0.3 +
                zcr_score * 0.2 +
                spectral_score * 0.2
            )
            
            segment.quality_score = quality_score
            return quality_score
            
        except Exception as e:
            print(f"⚠️  Error analyzing audio quality for chunk {segment.chunk_index}: {e}")
            return 0.0
    
    def select_best_segments(self, segments: List[EmotionalSegment], max_per_emotion: int = 10) -> Dict[str, List[EmotionalSegment]]:
        """
        Select the best segments for each emotional state.
        
        Args:
            segments: List of all segments
            max_per_emotion: Maximum segments to keep per emotion
            
        Returns:
            Dictionary mapping emotion -> list of best segments
        """
        # Group by emotion
        emotion_groups = defaultdict(list)
        for segment in segments:
            # Analyze audio quality
            quality = self.analyze_audio_quality(segment)
            if quality > 0.2:  # Only keep decent quality segments
                emotion_groups[segment.emotional_state].append(segment)
        
        # Select best segments for each emotion
        best_segments = {}
        for emotion, emotion_segments in emotion_groups.items():
            # Sort by quality score (descending) and sentiment extremity
            def score_segment(seg):
                # Favor extreme sentiment values for their categories
                sentiment_extremity = abs(seg.raw_sentiment)
                return seg.quality_score * 0.7 + sentiment_extremity * 0.3
            
            emotion_segments.sort(key=score_segment, reverse=True)
            best_segments[emotion] = emotion_segments[:max_per_emotion]
            
            print(f"🎭 {emotion}: {len(best_segments[emotion])}/{len(emotion_segments)} segments selected")
            for i, seg in enumerate(best_segments[emotion][:3]):  # Show top 3
                print(f"   #{i+1}: chunk_{seg.chunk_index:05d} | sentiment: {seg.raw_sentiment:+.3f} | quality: {seg.quality_score:.2f} | \"{seg.text[:50]}...\"")
        
        return best_segments
    
    def combine_emotional_samples(self, emotion_segments: Dict[str, List[EmotionalSegment]], output_dir: str) -> Dict[str, str]:
        """
        Combine segments into 10-second emotional voice samples.
        
        Args:
            emotion_segments: Dictionary of emotion -> segments
            output_dir: Directory to save combined samples
            
        Returns:
            Dictionary mapping emotion -> output file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        combined_samples = {}
        
        for emotion, segments in emotion_segments.items():
            if not segments:
                print(f"⚠️  No segments available for {emotion}")
                continue
            
            target_duration = self.TARGET_DURATIONS[emotion]
            combined_audio = []
            current_duration = 0.0
            used_segments = []
            
            # Add segments until we reach target duration
            for segment in segments:
                if current_duration >= target_duration:
                    break
                
                try:
                    audio, sr = librosa.load(segment.audio_path, sr=22050)  # Standardize sample rate
                    segment_duration = len(audio) / sr
                    
                    # Trim if needed to not exceed target
                    remaining_time = target_duration - current_duration
                    if segment_duration > remaining_time:
                        samples_needed = int(remaining_time * sr)
                        audio = audio[:samples_needed]
                        segment_duration = remaining_time
                    
                    combined_audio.extend(audio)
                    current_duration += segment_duration
                    used_segments.append(segment)
                    
                except Exception as e:
                    print(f"⚠️  Error loading audio for chunk {segment.chunk_index}: {e}")
                    continue
            
            if not combined_audio:
                print(f"⚠️  No audio could be combined for {emotion}")
                continue
            
            # Pad with silence if under target duration
            if current_duration < target_duration:
                silence_duration = target_duration - current_duration
                silence_samples = int(silence_duration * sr)
                combined_audio.extend([0.0] * silence_samples)
            
            # Save combined sample
            combined_audio = np.array(combined_audio)
            output_file = output_dir / f"voice_sample_{emotion}.wav"
            sf.write(output_file, combined_audio, sr)
            
            combined_samples[emotion] = str(output_file)
            
            print(f"💾 {emotion}: {len(used_segments)} segments combined → {output_file}")
            print(f"   Duration: {len(combined_audio)/sr:.1f}s | Segments: {[s.chunk_index for s in used_segments]}")
        
        return combined_samples
    
    def generate_sample_report(self, segments: List[EmotionalSegment], best_segments: Dict[str, List[EmotionalSegment]], output_samples: Dict[str, str], output_dir: str):
        """Generate a detailed report of the extraction process."""
        report_file = Path(output_dir) / "emotion_extraction_report.txt"
        
        with open(report_file, 'w') as f:
            f.write("# Emotion Extraction Report\n\n")
            f.write(f"Source: {self.audiobook_dir}\n")
            f.write(f"Total segments analyzed: {len(segments)}\n")
            f.write(f"Min segment duration: {self.min_segment_duration}s\n\n")
            
            # Emotion distribution
            f.write("## Emotion Distribution\n\n")
            emotion_counts = defaultdict(int)
            for seg in segments:
                emotion_counts[seg.emotional_state] += 1
            
            for emotion, count in sorted(emotion_counts.items()):
                percentage = (count / len(segments)) * 100
                f.write(f"- {emotion}: {count} segments ({percentage:.1f}%)\n")
            
            f.write("\n## Selected Segments\n\n")
            for emotion, selected in best_segments.items():
                f.write(f"### {emotion.upper()}\n")
                for i, seg in enumerate(selected):
                    f.write(f"{i+1:2d}. chunk_{seg.chunk_index:05d} | sentiment: {seg.raw_sentiment:+.3f} | quality: {seg.quality_score:.2f}\n")
                    f.write(f"    \"{seg.text}\"\n")
                f.write("\n")
            
            f.write("## Generated Voice Samples\n\n")
            for emotion, file_path in output_samples.items():
                f.write(f"- {emotion}: {file_path}\n")
        
        print(f"📄 Report saved: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract emotional voice samples from ChatterboxTTS output")
    parser.add_argument("audiobook_dir", help="Path to audiobook directory containing TTS/ folder")
    parser.add_argument("-o", "--output", default="extracted_samples", help="Output directory for voice samples")
    parser.add_argument("--min-duration", type=float, default=0.8, help="Minimum segment duration (seconds)")
    parser.add_argument("--max-per-emotion", type=int, default=10, help="Maximum segments per emotion")
    
    args = parser.parse_args()
    
    try:
        print(f"🎭 Starting emotion extraction from {args.audiobook_dir}")
        
        # Initialize extractor
        extractor = EmotionExtractor(args.audiobook_dir, args.min_duration)
        
        # Load and analyze segments
        segments = extractor.load_chunk_data()
        if not segments:
            print("❌ No valid segments found")
            return 1
        
        # Select best segments
        best_segments = extractor.select_best_segments(segments, args.max_per_emotion)
        
        # Combine into voice samples
        output_samples = extractor.combine_emotional_samples(best_segments, args.output)
        
        # Generate report
        extractor.generate_sample_report(segments, best_segments, output_samples, args.output)
        
        print(f"\n✅ Emotion extraction complete!")
        print(f"📁 Output directory: {args.output}")
        print(f"🎯 Generated {len(output_samples)} emotional voice samples")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())