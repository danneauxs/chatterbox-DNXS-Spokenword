# src.chatterbox.models.s3gen.matcha.text_encoder

> from https://github.com/jaywalnut310/glow-tts 

## Public API

### Classes
- **LayerNorm**  
  Methods: forward
- **ConvReluNorm**  
  Methods: forward
- **DurationPredictor**  
  Methods: forward
- **RotaryPositionalEmbeddings** — ## RoPE module  
  Methods: forward
- **MultiHeadAttention**  
  Methods: forward, attention
- **FFN**  
  Methods: forward
- **Encoder**  
  Methods: forward
- **TextEncoder**  
  Methods: forward

### Functions
- **sequence_mask**
- **forward**
- **forward**
- **forward**
- **forward** — * `x` is the Tensor at the head of a key or a query with shape `[seq_len, batch_size, n_heads, d]`
- **forward**
- **attention**
- **forward**
- **forward**
- **forward** — Run forward pass to the transformer based encoder and duration predictor

## Imports (local guesses)
- einops, math, torch, torch.nn