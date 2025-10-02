# modules.sequence_batch_processor

> True Sequence-Level Batch Processor

## Public API

### Classes
- **SequenceBatchProcessor** — True sequence-level batch processor that uses ChatterboxTTS.generate_batch()  
  Methods: analyze_batching_potential, process_chunks_with_sequence_batching

### Functions
- **create_sequence_batch_processor** — Factory function to create optimized sequence batch processor
- **analyze_batching_potential** — Analyze the batching potential of a chunk list
- **process_chunks_with_sequence_batching** — Process chunks using true sequence-level batching

## Imports (local guesses)
- collections, logging, time, torch, typing