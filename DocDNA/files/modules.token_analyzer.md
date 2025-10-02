# modules.token_analyzer

> Token Analyzer Module

## Public API

### Classes
- **TokenAnalyzer** — Analyzes chunks to predict optimal token requirements  
  Methods: predict_chunk_tokens, analyze_chunks_json, update_max_tokens_config

### Functions
- **get_token_analyzer** — Get global token analyzer instance
- **analyze_and_optimize_tokens** — Analyze chunks JSON and optionally update MAX_NEW_TOKENS
- **format_analysis_summary** — Format analysis results for GUI display
- **predict_chunk_tokens** — Predict token usage for a single chunk
- **analyze_chunks_json** — Analyze chunks JSON file and return token statistics
- **update_max_tokens_config** — Update MAX_NEW_TOKENS in config

## Imports (local guesses)
- config.config, json, logging, numpy, pathlib, re, typing