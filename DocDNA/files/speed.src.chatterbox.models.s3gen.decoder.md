# speed.src.chatterbox.models.s3gen.decoder

## Public API

### Classes
- **Transpose**  
  Methods: forward
- **CausalBlock1D**  
  Methods: forward
- **CausalResnetBlock1D**  
  Methods: (no public methods)
- **CausalConv1d**  
  Methods: forward
- **ConditionalDecoder**  
  Methods: initialize_weights, forward

### Functions
- **mask_to_bias**
- **forward**
- **forward**
- **forward**
- **initialize_weights**
- **forward** — Forward pass of the UNet1DConditional model.

## Imports (local guesses)
- einops, torch, torch.nn, torch.nn.functional

## Relative imports
- .utils.mask, .matcha.decoder, .matcha.transformer