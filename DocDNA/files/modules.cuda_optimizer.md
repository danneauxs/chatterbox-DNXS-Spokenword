# modules.cuda_optimizer

> CUDA Kernel Optimization Module

## Public API

### Classes
- **CudaOptimizer** — CUDA kernel and memory optimization manager  
  Methods: apply_cuda_optimizations, optimize_tensor_memory_layout, create_optimized_tensor, preallocate_batch_tensors, get_preallocated_tensor, async_batch_inference, pipeline_batch_processing, fused_attention_with_cache, optimize_batch_processing, clear_memory_efficiently, restore_original_settings, get_optimization_summary

### Functions
- **create_cuda_optimizer** — Factory function to create and configure CUDA optimizer
- **apply_cuda_optimizations** — Apply comprehensive CUDA optimizations
- **optimize_tensor_memory_layout** — Optimize tensor memory layout for better cache performance
- **create_optimized_tensor** — Create a tensor with optimal memory layout
- **preallocate_batch_tensors** — Pre-allocate tensors for common batch sizes and sequence lengths
- **get_preallocated_tensor** — Get a pre-allocated tensor if available, otherwise create new one
- **async_batch_inference** — Execute batch inference asynchronously using CUDA streams
- **pipeline_batch_processing** — Pipeline batch processing with overlapped memory and compute operations
- **fused_attention_with_cache** — Optimized attention computation with KV cache
- **optimize_batch_processing** — Calculate optimal batch processing parameters
- **clear_memory_efficiently** — Efficiently clear GPU memory
- **restore_original_settings** — Restore original CUDA settings
- **get_optimization_summary** — Get summary of applied optimizations

## Imports (local guesses)
- gc, logging, torch, torch.nn.functional, typing