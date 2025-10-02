"""
Terminal Output Logger
Captures all terminal output and logs it to a file for analysis
"""

import sys
import threading
from datetime import datetime
from pathlib import Path
try:
    # Respect config setting to append instead of overwriting
    from config.config import ENABLE_LOG_APPEND
except Exception:
    ENABLE_LOG_APPEND = True

class TerminalLogger:
    """Captures terminal output and logs to file"""
    
    def __init__(self, log_file="term.log", also_print=True):
        # Use absolute path for clarity and reliable updates
        self.log_file = Path(log_file).resolve()
        self.also_print = also_print
        self.lock = threading.Lock()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.enabled = False
        # Console suppression patterns
        self.suppress_console_substrings = [
            "VADER MICRO-BATCHING",
            "Processing micro-batch",
            "Waiting for micro-batch",
        ]
        # Throttle state for ETA/Chunk lines
        self._eta_every = 5
        # Per-chunk state
        self._sampling_lock = threading.Lock()
        self._batch_pos = 0
        self._batch_size = 0
        # Track latest suppressed Sampling bar values for one-shot summary
        self._last_sampling_tokens = None
        self._last_sampling_total = None
        self._last_sampling_its = None
        # Running it/s statistics (per-chunk summaries)
        self._its_sum = 0.0
        self._its_count = 0
        self._last_its_value = None
        # Cache last printed chunk summary line to avoid duplicates
        self._last_chunk_line_printed = None
        
    def start_logging(self):
        """Start capturing terminal output"""
        if self.enabled:
            return
        mode = 'a' if ENABLE_LOG_APPEND else 'w'
        with open(self.log_file, mode, encoding='utf-8') as f:
            tag = 'Continued' if mode == 'a' else 'Started'
            f.write(f"=== Terminal Log {tag}: {datetime.now()} ===\n")
        sys.stdout = self
        sys.stderr = self
        self.enabled = True
        # Reset running stats on start
        self._its_sum = 0.0
        self._its_count = 0
        self._last_its_value = None
        print(f"📝 Terminal logging started - output: {self.log_file}")
        
    def stop_logging(self):
        """Stop capturing terminal output"""
        if not self.enabled:
            return
        print("📝 Terminal logging stopped")
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        self.enabled = False
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"=== Terminal Log Ended: {datetime.now()} ===\n")

    def _emit_chunk_summary(self, num, its):
        """Internal method to format and print the per-chunk summary."""
        line = f"{num} {its} it/s\n"
        try:
            # Update running it/s statistics
            try:
                its_val = float(str(its))
                self._its_sum += its_val
                self._its_count += 1
                self._last_its_value = its_val
            except Exception:
                pass
            # Write to file and console directly, bypassing other logic
            self.original_stdout.write(line)
            self.original_stdout.flush()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(line)
                f.flush()
        except Exception:
            pass

    def emit_chunk_summary(self):
        """Public: emit exactly one per‑chunk summary using the latest Sampling values."""
        with self._sampling_lock:
            try:
                if self._last_sampling_tokens is None or self._last_sampling_its is None:
                    return  # nothing captured from Sampling yet
                self._emit_chunk_summary(self._last_sampling_tokens, self._last_sampling_its)
            finally:
                # Reset so we never print duplicates for the same chunk
                self._last_sampling_tokens = None
                self._last_sampling_total = None
                self._last_sampling_its = None

    def get_running_avg_its(self):
        """Return running average it/s across completed chunks (or None)."""
        if self._its_count > 0:
            return self._its_sum / self._its_count
        return None

    def write(self, text):
        """Write text to both file and terminal, applying filtering logic to each line."""
        with self.lock:
            # Always write the raw, unprocessed text to the log file first
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(text)
                f.flush()

            # Process the buffer line by line
            for line in text.splitlines():
                if not line:
                    continue

                clean_line = line.strip()
                suppress_original_line = False

                # Rule 1: Capture Sampling progress (suppress all lines), remember latest values
                if clean_line.startswith("Sampling:"):
                    suppress_original_line = True  # Always hide the raw tqdm line
                    try:
                        import re
                        # Example: "Sampling:  18%|#8        | 184/1000 [00:02<00:10, 77.23it/s]"
                        m_tokens = re.search(r"(\d+)\/(\d+)", clean_line)
                        m_its = re.search(r"([0-9]+\.?[0-9]*)it/s", clean_line)
                        if m_tokens:
                            current = int(m_tokens.group(1))
                            total = int(m_tokens.group(2))
                            # If a new bar starts (current small), reset stored values first
                            if self._last_sampling_tokens is None or current < (self._last_sampling_tokens or 0):
                                self._last_sampling_tokens = None
                                self._last_sampling_total = None
                                self._last_sampling_its = None
                            self._last_sampling_tokens = current
                            self._last_sampling_total = total
                        if m_its:
                            self._last_sampling_its = m_its.group(1)
                    except Exception:
                        pass  # never break logging on parse errors

                # Rule 2: Handle summary "🌀 Chunk" lines
                elif "🌀 Chunk" in clean_line:
                    # Drop any line while realtime is still calculating
                    if "Realtime: Calculating..." in clean_line:
                        suppress_original_line = True
                    else:
                        # Throttle to every N chunks (plus first and last) and dedupe identical repeats
                        try:
                            import re
                            m = re.search(r"🌀 Chunk\s+(\d+)\/(\d+)", clean_line)
                            if m:
                                cur = int(m.group(1))
                                total = int(m.group(2))
                                throttled_out = not ((cur == 1) or (cur % self._eta_every == 0) or (cur == total))
                                if throttled_out:
                                    suppress_original_line = True
                                else:
                                    if self._last_chunk_line_printed == clean_line:
                                        suppress_original_line = True
                                    else:
                                        self._last_chunk_line_printed = clean_line
                        except Exception:
                            pass

                # Rule 3: Handle other suppression patterns
                elif any(s in clean_line for s in self.suppress_console_substrings):
                    suppress_original_line = True

                # Finally, print the original line if it wasn't suppressed
                if self.also_print and not suppress_original_line:
                    # Prepend a newline to chunk summaries to separate them
                    if "🌀 Chunk" in line:
                        print("\n" + line, file=self.original_stdout)
                    else:
                        print(line, file=self.original_stdout)

            self.original_stdout.flush()
    
    def flush(self):
        """Flush output streams"""
        if self.also_print:
            self.original_stdout.flush()

    def write_file_only(self, text):
        """Write text only to the log file without echoing to terminal."""
        with self.lock:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(text)
                if not text.endswith("\n"):
                    f.write("\n")
                f.flush()

    def set_eta_frequency(self, every: int):
        with self.lock:
            try:
                self._eta_every = max(1, int(every))
            except Exception:
                self._eta_every = 5

    def set_batch_size(self, size: int):
        with self._sampling_lock:
            try:
                self._batch_size = max(0, int(size))
                self._batch_pos = 0
            except Exception:
                self._batch_size = 0
                self._batch_pos = 0

# Global logger instance
_terminal_logger = None

def start_terminal_logging(log_file="term.log"):
    """Start logging all terminal output to file"""
    global _terminal_logger
    # Always recreate logger to ensure latest suppression rules apply
    try:
        if _terminal_logger and _terminal_logger.enabled:
            _terminal_logger.stop_logging()
    except Exception:
        pass
    _terminal_logger = TerminalLogger(log_file)
    _terminal_logger.start_logging()

def stop_terminal_logging():
    """Stop logging terminal output"""
    global _terminal_logger
    if _terminal_logger:
        _terminal_logger.stop_logging()

def log_only(text: str):
    """Append a line to the terminal log without printing to the console."""
    global _terminal_logger
    if _terminal_logger is not None:
        _terminal_logger.write_file_only(text)
    else:
        # Fallback: write to default log path
        try:
            Path("term.log").open('a', encoding='utf-8').write(text + ("" if text.endswith("\n") else "\n"))
        except Exception:
            pass

def set_eta_frequency(every: int):
    global _terminal_logger
    if _terminal_logger is not None:
        _terminal_logger.set_eta_frequency(every)

def set_batch_size(size: int):
    global _terminal_logger
    if _terminal_logger is not None:
        _terminal_logger.set_batch_size(size)

def emit_chunk_summary():
    global _terminal_logger
    if _terminal_logger is not None:
        _terminal_logger.emit_chunk_summary()

def get_running_avg_its():
    """Module-level accessor for running avg it/s from per-chunk summaries."""
    global _terminal_logger
    if _terminal_logger is not None:
        try:
            return _terminal_logger.get_running_avg_its()
        except Exception:
            return None
    return None
