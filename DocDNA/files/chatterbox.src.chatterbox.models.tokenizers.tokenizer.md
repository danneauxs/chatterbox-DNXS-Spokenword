# chatterbox.src.chatterbox.models.tokenizers.tokenizer

## Public API

### Classes
- **EnTokenizer**  
  Methods: check_vocabset_sot_eot, text_to_tokens, encode, decode
- **ChineseCangjieConverter** — Converts Chinese characters to Cangjie codes for tokenization.  
  Methods: (no public methods)
- **MTLTokenizer**  
  Methods: check_vocabset_sot_eot, text_to_tokens, encode, decode

### Functions
- **is_kanji** — Check if character is kanji.
- **is_katakana** — Check if character is katakana.
- **hiragana_normalize** — Japanese text normalization: converts kanji to hiragana; katakana remains the same.
- **add_hebrew_diacritics** — Hebrew text normalization: adds diacritics to Hebrew text.
- **korean_normalize** — Korean text normalization: decompose syllables into Jamo for tokenization.
- **check_vocabset_sot_eot**
- **text_to_tokens**
- **encode** — clean_text > (append `lang_id`) > replace SPACE > encode text using Tokenizer
- **decode**
- **decompose_hangul** — Decompose Korean syllable into Jamo components.
- **check_vocabset_sot_eot**
- **text_to_tokens**
- **encode**
- **decode**

## Imports (local guesses)
- dicta_onnx, huggingface_hub, json, logging, pathlib, pkuseg, pykakasi, re, tokenizers, torch, unicodedata