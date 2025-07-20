import os
import shutil
from pathlib import Path
from config.config import AUDIOBOOK_ROOT
base = AUDIOBOOK_ROOT


def accept_revision(index, audio_dir):
    """
    Archive original chunk and replace with revised version.
    Assumes revised version is saved as: chunk_XXXXX_rev.wav
    """
    base = Path(audio_dir)
    # Use 1-based indexing and 5-digit format
    original = base / f"chunk_{index+1:05d}.wav"
    revised = base / f"chunk_{index+1:05d}_rev.wav"
    archive_dir = base.parent.parent / "Audio_Revisions"
    archive_dir.mkdir(exist_ok=True)

    if not revised.exists():
        print("❌ No revised file found. Cannot accept.")
        return

    # Archive original if exists
    if original.exists():
        archived = archive_dir / f"chunk_{index+1:05d}_orig.wav"
        shutil.move(str(original), str(archived))
        print(f"📦 Original chunk archived to {archived.name}")
    else:
        print(f"⚠️ Original chunk missing — no archive created.")

    # Move revised chunk to main filename
    shutil.move(str(revised), str(original))
    print(f"✅ Revised chunk accepted as {original.name}")
