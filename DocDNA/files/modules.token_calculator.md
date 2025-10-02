# modules.token_calculator

> Token Calculator for T3 TTS Analysis

## Public API

### Classes
- **TokenAnalysis**  
  Methods: (no public methods)
- **TTSTokenCalculator** — Calculate actual token usage vs reservations for TTS  
  Methods: analyze_chunks, analyze_single_chunk, print_analysis_summary, print_real_audiobook_analysis

### Functions
- **analyze_real_audiobook_chunks** — Analyze real audiobook chunks from JSON file
- **analyze_test_chunks** — Analyze the standard test chunks (fallback)
- **analyze_chunks** — Analyze token usage for multiple text chunks
- **analyze_single_chunk** — Analyze token usage for a single text chunk
- **print_analysis_summary** — Print detailed token waste analysis
- **print_real_audiobook_analysis** — Enhanced analysis for real audiobook chunks with VADER context

## Imports (local guesses)
- dataclasses, json, torch, typing