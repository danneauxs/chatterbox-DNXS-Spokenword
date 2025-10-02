# chatterbox.src.chatterbox.models.s3gen.transformer.subsampling

> Subsampling layer definition.

## Public API

### Classes
- **BaseSubsampling**  
  Methods: position_encoding
- **EmbedinigNoSubsampling** — Embedding input without subsampling  
  Methods: forward
- **LinearNoSubsampling** — Linear transform the input without subsampling  
  Methods: forward
- **Conv1dSubsampling2** — Convolutional 1D subsampling (to 1/2 length).  
  Methods: forward
- **Conv2dSubsampling4** — Convolutional 2D subsampling (to 1/4 length).  
  Methods: forward
- **Conv2dSubsampling6** — Convolutional 2D subsampling (to 1/6 length).  
  Methods: forward
- **Conv2dSubsampling8** — Convolutional 2D subsampling (to 1/8 length).  
  Methods: forward
- **LegacyLinearNoSubsampling** — Linear transform the input without subsampling  
  Methods: forward

### Functions
- **position_encoding**
- **forward** — Input x.
- **forward** — Input x.
- **forward** — Subsample x.
- **forward** — Subsample x.
- **forward** — Subsample x.
- **forward** — Subsample x.
- **forward** — Input x.

## Imports (local guesses)
- torch, typing