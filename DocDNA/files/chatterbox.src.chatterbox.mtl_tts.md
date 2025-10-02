# chatterbox.src.chatterbox.mtl_tts

## Public API

### Classes
- **Conditionals** — Conditionals for T3 and S3Gen  
  Methods: to, save, load
- **ChatterboxMultilingualTTS**  
  Methods: get_supported_languages, from_local, from_pretrained, prepare_conditionals, generate

### Functions
- **punc_norm** — Quick cleanup func for punctuation from LLMs or
- **to**
- **save**
- **load**
- **get_supported_languages** — Return dictionary of supported language codes and names.
- **from_local**
- **from_pretrained**
- **prepare_conditionals**
- **generate**

## Imports (local guesses)
- dataclasses, huggingface_hub, librosa, os, pathlib, perth, safetensors.torch, torch, torch.nn.functional

## Relative imports
- .models.t3, .models.t3.modules.t3_config, .models.s3tokenizer, .models.s3gen, .models.tokenizers, .models.voice_encoder, .models.t3.modules.cond_enc