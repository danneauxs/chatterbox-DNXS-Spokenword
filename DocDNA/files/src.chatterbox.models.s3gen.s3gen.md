# src.chatterbox.models.s3gen.s3gen

## Public API

### Classes
- **S3Token2Mel** — CosyVoice2's CFM decoder maps S3 speech tokens to mel-spectrograms.  
  Methods: device, embed_ref, forward
- **S3Token2Wav** — The decoder of CosyVoice2 is a concat of token-to-mel (CFM) and a mel-to-waveform (HiFiGAN) modules.  
  Methods: forward, flow_inference, hift_inference, inference

### Functions
- **drop_invalid_tokens**
- **get_resampler**
- **device**
- **embed_ref**
- **forward** — Generate waveforms from S3 speech tokens and a reference waveform, which the speaker timbre is inferred from.
- **forward**
- **flow_inference**
- **hift_inference**
- **inference**

## Imports (local guesses)
- functools, logging, numpy, omegaconf, torch, torchaudio, typing

## Relative imports
- ..s3tokenizer, .const, .flow, .xvector, .utils.mel, .f0_predictor, .hifigan, .transformer.upsample_encoder, .flow_matching, .decoder