# speed.src.chatterbox.text_utils

> Text processing utility functions

## Public API


### Functions
- **detect_language** — Simple language detection based on character patterns
- **get_sentence_separators** — Get sentence separator pattern for different languages
- **get_punctuation_pattern** — Get punctuation pattern for word boundary splitting
- **split_by_word_boundary** — Split text by word boundaries to ensure words are not broken in the middle
- **merge_short_sentences** — Merge short sentences to the next sentence, ensuring not to exceed maximum length limit
- **split_text_into_segments** — Split text into segments suitable for TTS processing

## Imports (local guesses)
- logging, re, typing