# tools.xtts_finetune_extractor

> XTTS-Finetune Audio Extractor for ChatterboxTTS

## Public API

### Classes
- **XTTSAudioFile** — Represents an audio file from XTTS-finetune data.  
  Methods: (no public methods)
- **XTTSFinetuneExtractor** — Main class for extracting audio from XTTS-finetune model data.  
  Methods: analyze_directory_structure, load_metadata, analyze_audio_file, assess_audio_quality, classify_emotion, extract_audio_files, select_best_samples, create_voice_samples, generate_report
- **SentimentIntensityAnalyzer** — Fallback sentiment analyzer when VADER is not available.  
  Methods: polarity_scores

### Functions
- **main**
- **analyze_directory_structure** — Analyze the XTTS-finetune directory structure.
- **load_metadata** — Load metadata from various formats.
- **analyze_audio_file** — Analyze a single audio file for quality and emotional content.
- **assess_audio_quality** — Assess audio quality using various metrics.
- **classify_emotion** — Classify VADER sentiment score into emotional categories.
- **extract_audio_files** — Extract and analyze all audio files.
- **select_best_samples** — Select the best audio samples for each emotion.
- **create_voice_samples** — Create combined voice samples for each emotion.
- **generate_report** — Generate a detailed extraction report.
- **polarity_scores**
- **score_file**

## Imports (local guesses)
- argparse, collections, csv, dataclasses, json, librosa, logging, numpy, os, pathlib, re, soundfile, sys, typing, vaderSentiment.vaderSentiment

## Framework signals
- argparse

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block