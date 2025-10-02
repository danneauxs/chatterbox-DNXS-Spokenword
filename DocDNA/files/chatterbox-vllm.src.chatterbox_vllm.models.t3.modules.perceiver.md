# chatterbox-vllm.src.chatterbox_vllm.models.t3.modules.perceiver

## Public API

### Classes
- **RelativePositionBias**  
  Methods: forward
- **AttentionQKV**  
  Methods: setup_flash_config, forward, scaled_dot_product_attention, flash_attention, split_heads, combine_heads
- **AttentionBlock2** — An attention block that allows spatial positions to attend to each other,  
  Methods: forward
- **Perceiver** — Inspired by https://arxiv.org/abs/2103.03206  
  Methods: forward

### Functions
- **forward**
- **setup_flash_config**
- **forward**
- **scaled_dot_product_attention**
- **flash_attention**
- **split_heads**
- **combine_heads**
- **forward**
- **forward** — Forward pass of the perceiver module.

## Imports (local guesses)
- einops, math, torch, torch.nn.functional