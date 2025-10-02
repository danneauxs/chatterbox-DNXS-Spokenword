# speed.src.chatterbox.models.s3gen.hifigan

> HIFI-GAN

## Public API

### Classes
- **Snake** — Implementation of a sine-based periodic activation function  
  Methods: forward
- **ResBlock** — Residual block module in HiFiGAN/BigVGAN.  
  Methods: forward, remove_weight_norm
- **SineGen** — Definition of sine generator  
  Methods: forward
- **SourceModuleHnNSF** — SourceModule for hn-nsf  
  Methods: forward
- **HiFTGenerator** — HiFTNet Generator: Neural Source Filter + ISTFTNet  
  Methods: remove_weight_norm, decode, forward, inference

### Functions
- **get_padding**
- **init_weights**
- **forward** — Forward pass of the function.
- **forward**
- **remove_weight_norm**
- **forward** — :param f0: [B, 1, sample_len], Hz
- **forward** — Sine_source, noise_source = SourceModuleHnNSF(F0_sampled)
- **remove_weight_norm**
- **decode**
- **forward**
- **inference**

## Imports (local guesses)
- numpy, scipy.signal, torch, torch.distributions.uniform, torch.nn, torch.nn.functional, torch.nn.utils, torch.nn.utils.parametrizations, typing