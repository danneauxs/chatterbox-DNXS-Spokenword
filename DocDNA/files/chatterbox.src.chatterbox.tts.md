# chatterbox.src.chatterbox.tts

## Public API

### Classes
- **Conditionals** — Conditionals for T3 and S3Gen  
  Methods: to, save, load
- **ChatterboxTTS**  
  Methods: from_local, from_pretrained, prepare_conditionals, generate

### Functions
- **punc_norm** — Quick cleanup func for punctuation from LLMs or
- **to**
- **save**
- **load**
- **from_local**
- **from_pretrained**
- **prepare_conditionals**
- **generate**

## Imports (local guesses)
- dataclasses, huggingface_hub, librosa, pathlib, perth, safetensors.torch, torch, torch.nn.functional

## Relative imports
- .models.t3, .models.s3tokenizer, .models.s3gen, .models.tokenizers, .models.voice_encoder, .models.t3.modules.cond_enc