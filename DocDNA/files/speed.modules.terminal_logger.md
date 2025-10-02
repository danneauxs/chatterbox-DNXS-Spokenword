# speed.modules.terminal_logger

> Terminal Output Logger

## Public API

### Classes
- **TerminalLogger** — Captures terminal output and logs to file  
  Methods: start_logging, stop_logging, emit_chunk_summary, get_running_avg_its, write, flush, write_file_only, set_eta_frequency, set_batch_size

### Functions
- **start_terminal_logging** — Start logging all terminal output to file
- **stop_terminal_logging** — Stop logging terminal output
- **log_only** — Append a line to the terminal log without printing to the console.
- **set_eta_frequency**
- **set_batch_size**
- **emit_chunk_summary**
- **get_running_avg_its** — Module-level accessor for running avg it/s from per-chunk summaries.
- **start_logging** — Start capturing terminal output
- **stop_logging** — Stop capturing terminal output
- **emit_chunk_summary** — Public: emit exactly one per‑chunk summary using the latest Sampling values.
- **get_running_avg_its** — Return running average it/s across completed chunks (or None).
- **write** — Write text to both file and terminal, applying filtering logic to each line.
- **flush** — Flush output streams
- **write_file_only** — Write text only to the log file without echoing to terminal.
- **set_eta_frequency**
- **set_batch_size**

## Imports (local guesses)
- config.config, datetime, pathlib, re, sys, threading

## Side-effect signals
- file_io