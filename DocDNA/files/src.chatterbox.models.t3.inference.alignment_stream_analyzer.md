# src.chatterbox.models.t3.inference.alignment_stream_analyzer

## Public API

### Classes
- **AlignmentAnalysisResult**  
  Methods: (no public methods)
- **AlignmentStreamAnalyzer**  
  Methods: step, close

### Functions
- **step** — Emits an AlignmentAnalysisResult into the output queue, and potentially modifies the logits to force an EOS.
- **close** — Remove hooks and restore original forward to prevent accumulation across generations.
- **attention_forward_hook** — See `LlamaAttention.forward`; the output is a 3-tuple: `attn_output, attn_weights, past_key_value`.
- **patched_forward**

## Imports (local guesses)
- dataclasses, logging, torch, types