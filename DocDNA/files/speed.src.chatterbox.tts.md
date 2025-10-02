# speed.src.chatterbox.tts

## Public API

### Classes
- **Conditionals** — Conditionals for T3 and S3Gen  
  Methods: to, save, load
- **ChatterboxTTS**  
  Methods: from_local, from_pretrained, prepare_conditionals, generate, generate_batch

### Functions
- **punc_norm** — Quick cleanup func for punctuation from LLMs or
- **parse_pause_tags** — Parse pause tags in text and return text segments with corresponding pause durations
- **create_silence** — Create silence of specified duration
- **to**
- **save**
- **load**
- **from_local**
- **from_pretrained**
- **prepare_conditionals**
- **generate**
- **generate_batch** — Batch generation for multiple texts sharing the same params/voice.
- **generate_worker**

## Imports (local guesses)
- concurrent.futures, config.config, dataclasses, huggingface_hub, librosa, numpy, os, pathlib, perth, queue, re, safetensors.torch, subprocess, tempfile, threading, torch, torch.nn.functional, torchaudio

## Relative imports
- .models.t3, .models.s3tokenizer, .models.s3gen, .models.tokenizers, .models.voice_encoder, .models.t3.modules.cond_enc, .text_utils

## Side-effect signals
- subprocess