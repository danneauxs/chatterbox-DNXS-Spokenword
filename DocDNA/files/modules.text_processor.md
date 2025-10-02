# modules.text_processor

> ChatterboxTTS Text Processing Module

## Public API


### Functions
- **load_abbreviations** — Load abbreviation-to-replacement mappings from external text file.
- **create_sample_abbreviations_file** — Create a sample abbreviations file with common replacements
- **preprocess_abbreviations** — Replace abbreviations with TTS-friendly versions
- **smart_punctuate** — Enhanced punctuation normalization with abbreviation replacement.
- **fix_short_sentence_artifacts** — Fix multiple short sentences that cause TTS errors.
- **sentence_chunk_text** — CRITICAL CHUNKING ALGORITHM - Heart of the TTS preprocessing system
- **break_long_sentence_backwards** — Break a long sentence working backwards from the end to find natural punctuation.
- **detect_punctuation_boundary** — Detect the ending punctuation of a text chunk for precise silence insertion.
- **detect_content_boundaries** — Detect chapter breaks and paragraph endings for appropriate silence insertion.
- **reload_abbreviations** — Reload abbreviations from file (useful for testing changes)
- **test_abbreviations** — Test abbreviation replacements on sample text
- **test_chunking** — Test the enhanced chunking with sample or custom text
- **get_chunk_bucket** — Determine which bucket a text chunk belongs to for torch.compile optimization
- **analyze_chunk_distribution** — Analyze the distribution of chunks across size buckets
- **calculate_optimization_potential** — Calculate potential optimization benefits from chunk bucketing
- **create_bucketed_chunk_groups** — Group chunks by size bucket for batch processing optimization
- **log_chunk_bucketing_stats** — Log chunk bucketing statistics for performance monitoring

## Imports (local guesses)
- config.config, logging, pathlib, re