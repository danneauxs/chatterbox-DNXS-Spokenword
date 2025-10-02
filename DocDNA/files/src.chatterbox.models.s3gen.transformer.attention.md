# src.chatterbox.models.s3gen.transformer.attention

> Multi-Head Attention layer definition.

## Public API

### Classes
- **MultiHeadedAttention** — Multi-Head Attention layer.  
  Methods: forward_qkv, forward_attention, forward
- **RelPositionMultiHeadedAttention** — Multi-Head Attention layer with relative position encoding.  
  Methods: rel_shift, forward

### Functions
- **forward_qkv** — Transform query, key and value.
- **forward_attention** — Compute attention context vector.
- **forward** — Compute scaled dot product attention.
- **rel_shift** — Compute relative positional encoding.
- **forward** — Compute 'Scaled Dot Product Attention' with rel. positional encoding.

## Imports (local guesses)
- math, torch, typing