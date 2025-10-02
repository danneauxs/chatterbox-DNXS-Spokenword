# src.chatterbox.models.t3.inference.t3_hf_backend

## Public API

### Classes
- **T3HuggingfaceBackend** — Override some HuggingFace interface methods so we can use the standard `generate` method with our  
  Methods: prepare_inputs_for_generation, forward

### Functions
- **prepare_inputs_for_generation** — This is a method used by huggingface's generate() method.
- **forward** — This is a method used by huggingface's generate() method.

## Imports (local guesses)
- torch, transformers, transformers.modeling_outputs, typing