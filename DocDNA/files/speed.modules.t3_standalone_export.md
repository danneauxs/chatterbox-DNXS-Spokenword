# speed.modules.t3_standalone_export

> T3 Standalone ONNX Export - Memory-efficient T3 ONNX conversion

## Public API

### Classes
- **T3MinimalWrapper**  
  Methods: forward

### Functions
- **find_cached_model_files** — Find cached ChatterboxTTS model files
- **load_t3_minimal** — Load ONLY T3 model with minimal VRAM usage
- **create_minimal_t3_wrapper** — Create minimal T3 ONNX wrapper without complex conditioning
- **export_t3_standalone** — Export T3 to ONNX with minimal memory footprint
- **forward** — Simplified T3 forward for ONNX export

## Imports (local guesses)
- gc, glob, logging, numpy, onnxruntime, os, pathlib, safetensors, src.chatterbox.models.t3.modules.cond_enc, src.chatterbox.models.t3.t3, src.chatterbox.models.tokenizers.tokenizer, sys, time, torch, torch.onnx, traceback

## Entrypoint
- Contains `if __name__ == '__main__':` block