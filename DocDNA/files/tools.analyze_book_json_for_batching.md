# tools.analyze_book_json_for_batching

> Book JSON Batching Analyzer

## Public API

### Classes
- **ChunkInfo** — Information about a single text chunk  
  Methods: (no public methods)
- **BatchGroup** — Group of chunks with identical TTS parameters  
  Methods: (no public methods)

### Functions
- **parse_book_json** — Parse book JSON file and extract chunk information
- **group_chunks_by_tts_params** — Group chunks by identical TTS parameters
- **calculate_batch_benefit** — Calculate potential benefit score for batching this group
- **analyze_batching_potential** — Analyze the overall batching potential
- **print_analysis_report** — Print detailed analysis report
- **create_batching_plan** — Create concrete batching implementation plan
- **save_analysis_results** — Save analysis results to file
- **main**

## Imports (local guesses)
- collections, dataclasses, json, pathlib, sys, time, torch, typing

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block