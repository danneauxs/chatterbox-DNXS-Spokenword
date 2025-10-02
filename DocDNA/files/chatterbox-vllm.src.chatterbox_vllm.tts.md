# chatterbox-vllm.src.chatterbox_vllm.tts

## Public API

### Classes
- **Conditionals** — Conditionals for T3 and S3Gen  
  Methods: to, load
- **ChatterboxTTS**  
  Methods: sr, from_local, from_pretrained, get_audio_conditionals, update_exaggeration, generate, generate_with_conds, shutdown

### Functions
- **to**
- **load**
- **sr** — Sample rate of synthesized audio
- **from_local**
- **from_pretrained**
- **get_audio_conditionals**
- **update_exaggeration**
- **generate**
- **generate_with_conds**
- **shutdown**

## Imports (local guesses)
- chatterbox_vllm.models.t3.modules.t3_config, dataclasses, functools, huggingface_hub, librosa, pathlib, safetensors.torch, time, torch, torch.nn.functional, typing, vllm

## Relative imports
- .models.s3tokenizer, .models.s3gen, .models.voice_encoder, .models.t3, .models.t3.modules.cond_enc, .models.t3.modules.learned_pos_emb, .text_utils