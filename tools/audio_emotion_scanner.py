#!/usr/bin/env python3
"""
Audio Emotion Scanner for ChatterboxTTS
Scans long audio files to extract emotive speech segments using ASR and sentiment analysis.

This tool:
1. Uses Whisper ASR with word-level timestamps 
2. Analyzes text for emotional content using VADER
3. Identifies questions and speech patterns
4. Maps emotions back to audio timestamps
5. Extracts audio segments for voice sample creation
6. Optimized for 8GB VRAM with chunked processing
"""

import json
import os
import sys
import whisper
import torch
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import argparse
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import gc
from collections import defaultdict
import logging

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TranscriptSegment(NamedTuple):
    """Represents a segment of transcribed audio with timestamps."""
    text: str
    start_time: float
    end_time: float
    confidence: float = 1.0

@dataclass
class EmotionalSegment:
    """Represents an audio segment with emotional analysis."""
    text: str
    start_time: float
    end_time: float
    duration: float
    emotion_type: str
    sentiment_score: float
    confidence: float
    speech_pattern: str  # 'statement', 'question', 'exclamation', etc.
    quality_score: float = 0.0

class AudioEmotionScanner:
    """Main class for scanning audio files for emotional content."""
    
    # Emotional classification thresholds
    EMOTION_THRESHOLDS = {
        'very_positive': 0.5,
        'positive': 0.1,
        'neutral': 0.05,
        'negative': -0.1,
        'very_negative': -0.5,
    }
    
    # Speech patterns to detect
    QUESTION_PATTERNS = [
        r'^(what|how|why|when|where|who|which|whose|whom)\b',
        r'^(do|does|did|will|would|could|should|can|may|might)\b',
        r'^(is|are|was|were|am|has|have|had)\b',
        r'\?$'
    ]
    
    EXCLAMATION_PATTERNS = [
        r'\!$',
        r'^(wow|amazing|incredible|fantastic|terrible|awful|horrible)\b',
    ]
    
    def __init__(self, chunk_duration: int = 600, overlap_duration: int = 30):
        """
        Initialize the audio emotion scanner.
        
        Args:
            chunk_duration: Audio chunk size in seconds (default 600 = 10 minutes)
            overlap_duration: Overlap between chunks in seconds (default 30)
        """
        self.chunk_duration = chunk_duration
        self.overlap_duration = overlap_duration
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.whisper_model = None
        
    def load_whisper_model(self, model_size: str = "large-v3"):
        """
        Load Whisper model with VRAM optimization.
        
        Args:
            model_size: Whisper model size ('large-v3', 'large', 'medium', 'small')
        """
        try:
            logging.info(f"Loading Whisper model: {model_size}")
            
            # Clear VRAM first
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Load model with optimization for 8GB VRAM
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.whisper_model = whisper.load_model(model_size, device=device)
            
            logging.info(f"Whisper model loaded on {device}")
            
            # Check VRAM usage
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated() / 1024**3
                logging.info(f"VRAM allocated: {memory_allocated:.2f} GB")
                
        except Exception as e:
            logging.error(f"Failed to load Whisper model: {e}")
            # Fallback to smaller model
            if model_size == "large-v3":
                logging.info("Falling back to large model")
                return self.load_whisper_model("large")
            elif model_size == "large":
                logging.info("Falling back to medium model")  
                return self.load_whisper_model("medium")
            else:
                raise e
    
    def chunk_audio(self, audio_path: str) -> List[Tuple[np.ndarray, float, float]]:
        """
        Split long audio into overlapping chunks for processing.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of (audio_chunk, start_time, end_time) tuples
        """
        logging.info(f"Loading audio file: {audio_path}")
        
        # Load full audio file
        audio, sr = librosa.load(audio_path, sr=16000)  # Whisper expects 16kHz
        total_duration = len(audio) / sr
        
        logging.info(f"Audio duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        
        chunks = []
        start_time = 0.0
        
        while start_time < total_duration:
            end_time = min(start_time + self.chunk_duration, total_duration)
            
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            
            chunk_audio = audio[start_sample:end_sample]
            chunks.append((chunk_audio, start_time, end_time))
            
            logging.info(f"Created chunk: {start_time:.1f}s - {end_time:.1f}s ({len(chunk_audio)/sr:.1f}s)")
            
            # Move to next chunk with overlap
            start_time += self.chunk_duration - self.overlap_duration
            
            if end_time >= total_duration:
                break
        
        return chunks
    
    def transcribe_chunk(self, audio_chunk: np.ndarray, chunk_start_time: float) -> List[TranscriptSegment]:
        """
        Transcribe a single audio chunk with word-level timestamps.
        
        Args:
            audio_chunk: Audio data
            chunk_start_time: Global start time of chunk
            
        Returns:
            List of transcript segments with timestamps
        """
        try:
            # Clear VRAM before processing
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Transcribe with word-level timestamps
            result = self.whisper_model.transcribe(
                audio_chunk,
                word_timestamps=True,
                verbose=False
            )
            
            segments = []
            for segment in result.get('segments', []):
                # Extract words with timestamps
                words = segment.get('words', [])
                if not words:
                    # Fallback to segment-level timestamps
                    segments.append(TranscriptSegment(
                        text=segment['text'].strip(),
                        start_time=chunk_start_time + segment['start'],
                        end_time=chunk_start_time + segment['end'],
                        confidence=segment.get('avg_logprob', 0.0)
                    ))
                else:
                    # Group words into sentences for better analysis
                    current_sentence = []
                    sentence_start = None
                    
                    for word in words:
                        if sentence_start is None:
                            sentence_start = word['start']
                        
                        current_sentence.append(word['word'])
                        
                        # End sentence on punctuation or long pause
                        if (word['word'].rstrip().endswith(('.', '!', '?')) or 
                            (len(current_sentence) > 1 and 
                             word.get('end', 0) - words[words.index(word)-1].get('end', 0) > 1.0)):
                            
                            sentence_text = ''.join(current_sentence).strip()
                            if sentence_text:
                                segments.append(TranscriptSegment(
                                    text=sentence_text,
                                    start_time=chunk_start_time + sentence_start,
                                    end_time=chunk_start_time + word['end'],
                                    confidence=segment.get('avg_logprob', 0.0)
                                ))
                            
                            current_sentence = []
                            sentence_start = None
                    
                    # Handle remaining words
                    if current_sentence:
                        sentence_text = ''.join(current_sentence).strip()
                        if sentence_text:
                            segments.append(TranscriptSegment(
                                text=sentence_text,
                                start_time=chunk_start_time + sentence_start,
                                end_time=chunk_start_time + words[-1]['end'],
                                confidence=segment.get('avg_logprob', 0.0)
                            ))
            
            return segments
            
        except Exception as e:
            logging.error(f"Error transcribing chunk: {e}")
            return []
    
    def classify_speech_pattern(self, text: str) -> str:
        """Classify the speech pattern of a text segment."""
        text_lower = text.lower().strip()
        
        # Check for questions
        for pattern in self.QUESTION_PATTERNS:
            if re.search(pattern, text_lower):
                return 'question'
        
        # Check for exclamations
        for pattern in self.EXCLAMATION_PATTERNS:
            if re.search(pattern, text_lower):
                return 'exclamation'
        
        return 'statement'
    
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
    
    def analyze_transcript_segments(self, segments: List[TranscriptSegment]) -> List[EmotionalSegment]:
        """Analyze transcript segments for emotional content."""
        emotional_segments = []
        
        for segment in segments:
            if len(segment.text.strip()) < 10:  # Skip very short segments
                continue
            
            # Sentiment analysis
            sentiment_scores = self.sentiment_analyzer.polarity_scores(segment.text)
            sentiment_score = sentiment_scores['compound']
            
            # Classify emotion and speech pattern
            emotion_type = self.classify_emotion(sentiment_score)
            speech_pattern = self.classify_speech_pattern(segment.text)
            
            # Create emotional segment
            emotional_seg = EmotionalSegment(
                text=segment.text,
                start_time=segment.start_time,
                end_time=segment.end_time,
                duration=segment.end_time - segment.start_time,
                emotion_type=emotion_type,
                sentiment_score=sentiment_score,
                confidence=segment.confidence,
                speech_pattern=speech_pattern
            )
            
            emotional_segments.append(emotional_seg)
        
        return emotional_segments
    
    def extract_audio_segment(self, audio_path: str, start_time: float, end_time: float, 
                            output_path: str, fade_duration: float = 0.1) -> bool:
        """
        Extract a specific audio segment from the original file.
        
        Args:
            audio_path: Original audio file path
            start_time: Start time in seconds
            end_time: End time in seconds  
            output_path: Output file path
            fade_duration: Fade in/out duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load segment with some padding
            padding = 0.2  # 200ms padding
            padded_start = max(0, start_time - padding)
            padded_end = end_time + padding
            
            audio, sr = librosa.load(audio_path, sr=22050, 
                                   offset=padded_start, 
                                   duration=padded_end - padded_start)
            
            # Trim to exact segment
            actual_start = padding if start_time >= padding else start_time
            actual_end = actual_start + (end_time - start_time)
            
            start_sample = int(actual_start * sr)
            end_sample = int(actual_end * sr)
            
            if end_sample > len(audio):
                end_sample = len(audio)
            
            segment_audio = audio[start_sample:end_sample]
            
            # Apply fade in/out
            fade_samples = int(fade_duration * sr)
            if len(segment_audio) > fade_samples * 2:
                # Fade in
                fade_in = np.linspace(0, 1, fade_samples)
                segment_audio[:fade_samples] *= fade_in
                
                # Fade out
                fade_out = np.linspace(1, 0, fade_samples)
                segment_audio[-fade_samples:] *= fade_out
            
            # Save segment
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, segment_audio, sr)
            
            return True
            
        except Exception as e:
            logging.error(f"Error extracting audio segment {start_time}-{end_time}: {e}")
            return False
    
    def scan_audio_file(self, audio_path: str, output_dir: str) -> Dict[str, List[EmotionalSegment]]:
        """
        Scan entire audio file for emotional segments.
        
        Args:
            audio_path: Path to audio file
            output_dir: Directory for output files
            
        Returns:
            Dictionary mapping emotion types to segments
        """
        logging.info(f"Starting audio scan: {audio_path}")
        
        # Load Whisper model
        if self.whisper_model is None:
            self.load_whisper_model()
        
        # Chunk audio for processing
        audio_chunks = self.chunk_audio(audio_path)
        
        all_segments = []
        
        # Process each chunk
        for i, (chunk_audio, start_time, end_time) in enumerate(audio_chunks):
            logging.info(f"Processing chunk {i+1}/{len(audio_chunks)}: {start_time:.1f}s - {end_time:.1f}s")
            
            # Transcribe chunk
            transcript_segments = self.transcribe_chunk(chunk_audio, start_time)
            
            # Analyze for emotions
            emotional_segments = self.analyze_transcript_segments(transcript_segments)
            all_segments.extend(emotional_segments)
            
            logging.info(f"Found {len(emotional_segments)} emotional segments in chunk {i+1}")
            
            # Clear VRAM between chunks
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
        
        # Group segments by emotion type
        emotion_groups = defaultdict(list)
        for segment in all_segments:
            emotion_groups[segment.emotion_type].append(segment)
        
        # Sort segments by sentiment extremity within each emotion
        for emotion_type, segments in emotion_groups.items():
            segments.sort(key=lambda x: abs(x.sentiment_score), reverse=True)
        
        # Save analysis results
        self.save_analysis_results(all_segments, emotion_groups, audio_path, output_dir)
        
        return dict(emotion_groups)
    
    def save_analysis_results(self, all_segments: List[EmotionalSegment], 
                            emotion_groups: Dict[str, List[EmotionalSegment]],
                            audio_path: str, output_dir: str):
        """Save analysis results to JSON and text files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save detailed segment analysis
        segments_data = []
        for i, segment in enumerate(all_segments):
            segments_data.append({
                "index": i,
                "text": segment.text,
                "start_time": round(segment.start_time, 2),
                "end_time": round(segment.end_time, 2),
                "duration": round(segment.duration, 2),
                "emotion_type": segment.emotion_type,
                "sentiment_score": round(segment.sentiment_score, 3),
                "speech_pattern": segment.speech_pattern,
                "confidence": round(segment.confidence, 3)
            })
        
        with open(output_dir / "emotional_segments.json", 'w') as f:
            json.dump(segments_data, f, indent=2)
        
        # Save summary report
        with open(output_dir / "emotion_analysis_report.txt", 'w') as f:
            f.write(f"# Emotion Analysis Report\n\n")
            f.write(f"Source: {audio_path}\n")
            f.write(f"Total segments found: {len(all_segments)}\n\n")
            
            # Emotion distribution
            f.write("## Emotion Distribution\n\n")
            for emotion, segments in emotion_groups.items():
                percentage = (len(segments) / len(all_segments)) * 100
                f.write(f"- {emotion}: {len(segments)} segments ({percentage:.1f}%)\n")
            
            # Speech pattern distribution
            f.write("\n## Speech Pattern Distribution\n\n")
            pattern_counts = defaultdict(int)
            for segment in all_segments:
                pattern_counts[segment.speech_pattern] += 1
            
            for pattern, count in pattern_counts.items():
                percentage = (count / len(all_segments)) * 100
                f.write(f"- {pattern}: {count} segments ({percentage:.1f}%)\n")
            
            # Top segments for each emotion
            f.write("\n## Top Emotional Segments\n\n")
            for emotion, segments in emotion_groups.items():
                f.write(f"### {emotion.upper()}\n")
                for i, segment in enumerate(segments[:5]):  # Top 5
                    f.write(f"{i+1}. [{segment.start_time:.1f}s-{segment.end_time:.1f}s] "
                           f"sentiment: {segment.sentiment_score:+.3f} | "
                           f"pattern: {segment.speech_pattern}\n")
                    f.write(f"   \"{segment.text}\"\n")
                f.write("\n")
        
        logging.info(f"Analysis results saved to {output_dir}")
    
    def extract_best_segments(self, emotion_groups: Dict[str, List[EmotionalSegment]], 
                            audio_path: str, output_dir: str, 
                            max_per_emotion: int = 5) -> Dict[str, List[str]]:
        """
        Extract the best audio segments for each emotion.
        
        Args:
            emotion_groups: Grouped emotional segments
            audio_path: Original audio file path
            output_dir: Output directory for extracted segments
            max_per_emotion: Maximum segments to extract per emotion
            
        Returns:
            Dictionary mapping emotion -> list of extracted file paths
        """
        output_dir = Path(output_dir)
        extracted_files = defaultdict(list)
        
        for emotion, segments in emotion_groups.items():
            emotion_dir = output_dir / f"segments_{emotion}"
            emotion_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract top segments
            for i, segment in enumerate(segments[:max_per_emotion]):
                output_file = emotion_dir / f"{emotion}_{i+1:02d}_{segment.start_time:.1f}s.wav"
                
                success = self.extract_audio_segment(
                    audio_path, 
                    segment.start_time,
                    segment.end_time,
                    str(output_file)
                )
                
                if success:
                    extracted_files[emotion].append(str(output_file))
                    logging.info(f"Extracted {emotion} segment: {output_file.name}")
        
        return dict(extracted_files)

def main():
    parser = argparse.ArgumentParser(description="Scan audio files for emotional speech segments")
    parser.add_argument("audio_file", help="Path to audio file (20+ minutes recommended)")
    parser.add_argument("-o", "--output", default="emotion_scan_output", help="Output directory")
    parser.add_argument("--chunk-duration", type=int, default=600, help="Chunk duration in seconds (default: 600)")
    parser.add_argument("--model-size", default="large-v3", choices=["tiny", "base", "small", "medium", "large", "large-v3"], help="Whisper model size")
    parser.add_argument("--max-segments", type=int, default=5, help="Max segments to extract per emotion")
    parser.add_argument("--extract-audio", action="store_true", help="Extract best audio segments")
    
    args = parser.parse_args()
    
    try:
        print(f"🎭 Starting emotion scan of {args.audio_file}")
        
        # Initialize scanner
        scanner = AudioEmotionScanner(chunk_duration=args.chunk_duration)
        
        # Scan audio file
        emotion_groups = scanner.scan_audio_file(args.audio_file, args.output)
        
        # Extract audio segments if requested
        if args.extract_audio:
            print("🎵 Extracting best audio segments...")
            extracted_files = scanner.extract_best_segments(
                emotion_groups, args.audio_file, args.output, args.max_segments
            )
            
            print(f"✅ Extracted segments for {len(extracted_files)} emotions")
            for emotion, files in extracted_files.items():
                print(f"   {emotion}: {len(files)} files")
        
        print(f"\n✅ Emotion scan complete!")
        print(f"📁 Results saved to: {args.output}")
        print(f"🎯 Found segments for {len(emotion_groups)} emotion types")
        
        for emotion, segments in emotion_groups.items():
            print(f"   {emotion}: {len(segments)} segments")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.exception("Full error details:")
        return 1

if __name__ == "__main__":
    sys.exit(main())