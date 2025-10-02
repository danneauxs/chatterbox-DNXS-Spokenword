"""Chatterbox package init (kept minimal to avoid heavy side effects on import).

Import submodules explicitly, e.g.:
  from src.chatterbox.tts import ChatterboxTTS
  from src.chatterbox.vc import ChatterboxVC
"""

from .tts import ChatterboxTTS
from .vc import ChatterboxVC
from .text_utils import split_text_into_segments, split_by_word_boundary, merge_short_sentences

__all__ = []
