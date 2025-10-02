# speed.src.chatterbox.models.s3gen.transformer.upsample_encoder

> Encoder definition.

## Public API

### Classes
- **Upsample1D** — A 1D upsampling layer with an optional convolution.  
  Methods: forward
- **PreLookaheadLayer**  
  Methods: forward
- **UpsampleConformerEncoder**  
  Methods: output_size, forward, forward_layers, forward_up_layers

### Functions
- **forward**
- **forward** — inputs: (batch_size, seq_len, channels)
- **output_size**
- **forward** — Embed positions in tensor.
- **forward_layers**
- **forward_up_layers**

## Imports (local guesses)
- torch, torch.nn, typing

## Relative imports
- .convolution, .encoder_layer, .positionwise_feed_forward, ..utils.class_utils, ..utils.mask, ..utils.mask