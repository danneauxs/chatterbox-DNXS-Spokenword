# speed.src.chatterbox.models.s3gen.transformer.embedding

> Positonal Encoding Module.

## Public API

### Classes
- **PositionalEncoding** — Positional encoding.  
  Methods: forward, position_encoding
- **RelPositionalEncoding** — Relative positional encoding module.  
  Methods: forward
- **WhisperPositionalEncoding** — Sinusoids position encoding used in openai-whisper.encoder  
  Methods: (no public methods)
- **LearnablePositionalEncoding** — Learnable position encoding used in openai-whisper.decoder  
  Methods: (no public methods)
- **NoPositionalEncoding** — No position encoding  
  Methods: forward, position_encoding
- **EspnetRelPositionalEncoding** — Relative positional encoding module (new implementation).  
  Methods: extend_pe, forward, position_encoding

### Functions
- **forward** — Add positional encoding.
- **position_encoding** — For getting encoding in a streaming fashion
- **forward** — Compute positional encoding.
- **forward** — Just return zero vector for interface compatibility
- **position_encoding**
- **extend_pe** — Reset the positional encodings.
- **forward** — Add positional encoding.
- **position_encoding** — For getting encoding in a streaming fashion

## Imports (local guesses)
- math, numpy, torch, torch.nn.functional, typing