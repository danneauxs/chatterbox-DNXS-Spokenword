# modules.real_tts_optimizer

> Real TTS Performance Optimizer

## Public API

### Classes
- **RealTTSOptimizer** — Real optimizations that actually affect TTS performance  
  Methods: fp32_fallback_mode, apply_optimizations, restore_original_methods

### Functions
- **get_tts_optimizer** — Get or create the global TTS optimizer
- **optimize_chatterbox_model** — Apply real optimizations to ChatterboxTTS model
- **optimized_inference** — Context manager for optimized inference
- **fp32_fallback_mode** — Context manager to temporarily disable mixed precision for a single operation.
- **apply_optimizations** — Apply real optimizations to ChatterboxTTS model with detailed tracking
- **restore_original_methods** — Restore original methods (cleanup)
- **optimized_t3_inference**
- **optimized_s3gen_inference**

## Imports (local guesses)
- config.config, contextlib, logging, torch, traceback