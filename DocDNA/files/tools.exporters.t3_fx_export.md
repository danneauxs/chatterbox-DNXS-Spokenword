# tools.exporters.t3_fx_export

> Phase 1: FX trace + operator inventory for one T3 decoder block.

## Public API

### Classes
- **BlockWrapper**  
  Methods: forward
- **RoPETracer**  
  Methods: is_leaf_module

### Functions
- **trace_block**
- **op_histogram**
- **main**
- **forward**
- **is_leaf_module**

## Imports (local guesses)
- __future__, argparse, config.config, json, os, pathlib, safetensors.torch, src.chatterbox.models.t3, src.chatterbox.models.t3.llama_configs, sys, torch, torch.fx, typing

## Framework signals
- argparse

## Entrypoint
- Contains `if __name__ == '__main__':` block