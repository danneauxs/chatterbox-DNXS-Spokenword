from pathlib import Path
from config.config import AUDIOBOOK_ROOT

def get_book_paths(book_name):
    """Return standardized paths for a given book name"""
    base = AUDIOBOOK_ROOT / book_name
    tts_dir = base / "TTS"
    return {
        "book_folder": base,
        "tts_dir": tts_dir,
        "text_chunks": tts_dir / "text_chunks",
        "audio_chunks": tts_dir / "audio_chunks",
        "combined_wav": base / f"{book_name}.wav",
        "final_m4b": base / f"{book_name}.m4b",
        "concat_list": tts_dir / "audio_chunks" / "concat.txt",
        "quarantine": tts_dir / "audio_chunks" / "quarantine",
        "run_log": base / "run.log",
        "chunk_log": base / "chunk_validation.log"
    }
