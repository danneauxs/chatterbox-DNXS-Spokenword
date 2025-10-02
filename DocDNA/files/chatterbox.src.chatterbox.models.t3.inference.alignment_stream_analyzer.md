# chatterbox.src.chatterbox.models.t3.inference.alignment_stream_analyzer

## Public API

### Classes
- **AlignmentAnalysisResult**  
  Methods: (no public methods)
- **AlignmentStreamAnalyzer**  
  Methods: step

### Functions
- **step** — Emits an AlignmentAnalysisResult into the output queue, and potentially modifies the logits to force an EOS.
- **attention_forward_hook** — See `LlamaAttention.forward`; the output is a 3-tuple: `attn_output, attn_weights, past_key_value`.

## Imports (local guesses)
- dataclasses, logging, torch, types