# speed.src.chatterbox.models.t3.modules.cond_enc

## Public API

### Classes
- **T3Cond** — Dataclass container for most / all conditioning info.  
  Methods: to, save, load
- **T3CondEnc** — Handle all non-text conditioning, like speaker embeddings / prompts, CLAP, emotion, etc.  
  Methods: forward

### Functions
- **to** — Cast to a device and dtype. Dtype casting is ignored for long/int tensors.
- **save**
- **load**
- **forward**

## Imports (local guesses)
- dataclasses, torch, typing

## Relative imports
- .perceiver, .t3_config