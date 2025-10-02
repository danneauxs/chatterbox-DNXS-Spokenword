# modules.token_usage_logger

> Token Usage Logger for T3 Performance Analysis

## Public API

### Classes
- **TokenUsageLogger** — Log token usage per chunk for performance analysis  
  Methods: start_chunk, log_chunk_completion, log_chunk_data, get_log_summary, print_summary

### Functions
- **initialize_token_logging** — Initialize global token usage logging
- **start_chunk_logging** — Start logging for a new chunk
- **log_chunk_tokens** — Log token usage for current chunk
- **log_chunk_data_direct** — Log chunk data directly
- **print_token_usage_summary** — Print summary of token usage
- **get_token_logger** — Get global token logger instance
- **start_chunk** — Mark the start of a new chunk
- **log_chunk_completion** — Log completion of current chunk with token usage
- **log_chunk_data** — Direct logging method for when data is already calculated
- **get_log_summary** — Get summary statistics from current log
- **print_summary** — Print summary of logged data

## Imports (local guesses)
- datetime, os, threading, time, typing