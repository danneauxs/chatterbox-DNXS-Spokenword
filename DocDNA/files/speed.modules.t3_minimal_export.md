# speed.modules.t3_minimal_export

> T3 Minimal ONNX Export - Simplified approach with working T3Cond

## Public API

### Classes
- **T3WorkingWrapper**  
  Methods: forward

### Functions
- **create_working_t3_cond** — Create T3Cond that matches working ChatterboxTTS usage
- **export_t3_minimal** — Export T3 with minimal working configuration
- **forward** — Working T3 forward with proper T3Cond

## Imports (local guesses)
- gc, modules.t3_standalone_export, numpy, onnxruntime, pathlib, src.chatterbox.models.t3.modules.cond_enc, sys, torch, torch.onnx, traceback

## Entrypoint
- Contains `if __name__ == '__main__':` block