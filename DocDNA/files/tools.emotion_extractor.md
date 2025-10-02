# tools.emotion_extractor

> Emotion Extractor for ChatterboxTTS

## Public API

### Classes
- **EmotionalSegment** — Represents an audio segment with its emotional characteristics.  
  Methods: (no public methods)
- **EmotionExtractor** — Main class for extracting emotional voice samples from TTS output.  
  Methods: classify_emotion, load_chunk_data, analyze_audio_quality, select_best_segments, combine_emotional_samples, generate_sample_report

### Functions
- **main**
- **classify_emotion** — Classify VADER sentiment score into discrete emotional states.
- **load_chunk_data** — Load and parse chunk data from JSON file.
- **analyze_audio_quality** — Analyze audio quality and return a score (0-1, higher is better).
- **select_best_segments** — Select the best segments for each emotional state.
- **combine_emotional_samples** — Combine segments into 10-second emotional voice samples.
- **generate_sample_report** — Generate a detailed report of the extraction process.
- **score_segment**

## Imports (local guesses)
- argparse, collections, dataclasses, json, librosa, numpy, os, pathlib, soundfile, sys, typing

## Framework signals
- argparse

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block