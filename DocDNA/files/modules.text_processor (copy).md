# modules.text_processor (copy)

> Text Processing Module

## Public API


### Functions
- **load_abbreviations** — Load abbreviation replacements from external file
- **create_sample_abbreviations_file** — Create a sample abbreviations file with common replacements
- **preprocess_abbreviations** — Replace abbreviations with TTS-friendly versions
- **smart_punctuate** — Enhanced punctuation normalization with abbreviation replacement.
- **fix_short_sentence_artifacts** — Fix multiple short sentences that cause TTS errors.
- **sentence_chunk_text** — Enhanced sentence chunking that respects paragraph boundaries and punctuation rules.
- **break_long_sentence_backwards** — Break a long sentence working backwards from the end to find natural punctuation.
- **detect_content_boundaries** — Detect chapter breaks and paragraph endings for appropriate silence insertion.
- **reload_abbreviations** — Reload abbreviations from file (useful for testing changes)
- **test_abbreviations** — Test abbreviation replacements on sample text
- **test_chunking** — Test the enhanced chunking with sample or custom text

## Imports (local guesses)
- config.config, logging, pathlib, re