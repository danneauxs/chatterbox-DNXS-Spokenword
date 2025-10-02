# tools.audio_emotion_scanner

> Audio Emotion Scanner for ChatterboxTTS

## Public API

### Classes
- **TranscriptSegment** — Represents a segment of transcribed audio with timestamps.  
  Methods: (no public methods)
- **EmotionalSegment** — Represents an audio segment with emotional analysis.  
  Methods: (no public methods)
- **AudioEmotionScanner** — Main class for scanning audio files for emotional content.  
  Methods: load_whisper_model, chunk_audio, transcribe_chunk, classify_speech_pattern, classify_emotion, analyze_transcript_segments, extract_audio_segment, scan_audio_file, save_analysis_results, extract_best_segments

### Functions
- **main**
- **load_whisper_model** — Load Whisper model with VRAM optimization.
- **chunk_audio** — Split long audio into overlapping chunks for processing.
- **transcribe_chunk** — Transcribe a single audio chunk with word-level timestamps.
- **classify_speech_pattern** — Classify the speech pattern of a text segment.
- **classify_emotion** — Classify VADER sentiment score into emotional categories.
- **analyze_transcript_segments** — Analyze transcript segments for emotional content.
- **extract_audio_segment** — Extract a specific audio segment from the original file.
- **scan_audio_file** — Scan entire audio file for emotional segments.
- **save_analysis_results** — Save analysis results to JSON and text files.
- **extract_best_segments** — Extract the best audio segments for each emotion.

## Imports (local guesses)
- argparse, collections, dataclasses, gc, json, librosa, logging, numpy, os, pathlib, re, soundfile, sys, torch, typing, vaderSentiment.vaderSentiment, whisper

## Framework signals
- argparse

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block