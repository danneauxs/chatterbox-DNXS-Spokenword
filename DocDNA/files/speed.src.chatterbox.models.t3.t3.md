# speed.src.chatterbox.models.t3.t3

## Public API

### Classes
- **AttrDict**  
  Methods: (no public methods)
- **T3** — Token-To-Token (T3) TTS model using huggingface transformer models as backbones,  
  Methods: device, prepare_conditioning, prepare_input_embeds, forward, loss, inference

### Functions
- **device**
- **prepare_conditioning** — Token cond data needs to be embedded, so that needs to be here instead of in `T3CondEnc`.
- **prepare_input_embeds**
- **forward**
- **loss** — training method
- **inference** — Args:

## Imports (local guesses)
- logging, os, torch, torch.nn.functional, tqdm, transformers, transformers.generation.logits_process, typing

## Relative imports
- .modules.learned_pos_emb, .modules.cond_enc, .modules.t3_config, .llama_configs, .inference.t3_hf_backend, .inference.alignment_stream_analyzer