# src.chatterbox.models.s3tokenizer.s3tokenizer

## Public API

### Classes
- **S3Tokenizer** — s3tokenizer.S3TokenizerV2 with the following changes:  
  Methods: pad, forward, log_mel_spectrogram

### Functions
- **pad** — Given a list of wavs with the same `sample_rate`, pad them so that the length is multiple of 40ms (S3 runs at 25 token/sec).
- **forward** — NOTE: mel-spec has a hop size of 160 points (100 frame/sec).
- **log_mel_spectrogram** — Compute the log-Mel spectrogram of

## Imports (local guesses)
- librosa, numpy, s3tokenizer.model_v2, s3tokenizer.utils, torch, torch.nn.functional, typing