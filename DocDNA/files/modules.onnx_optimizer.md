# modules.onnx_optimizer

> ONNX Optimization Module for ChatterboxTTS T3 Model

## Public API

### Classes
- **T3ONNXOptimizer** — Convert T3 model to ONNX for maximum inference speed  
  Methods: convert_t3_to_onnx, onnx_inference, benchmark_onnx_vs_pytorch
- **T3InferenceWrapper**  
  Methods: forward

### Functions
- **optimize_model_with_onnx** — Main function to apply ONNX optimization to ChatterboxTTS
- **convert_t3_to_onnx** — Convert T3 inference to optimized ONNX model
- **onnx_inference** — Run ultra-fast ONNX inference
- **benchmark_onnx_vs_pytorch** — Benchmark ONNX vs PyTorch performance
- **onnx_wrapped_inference**
- **forward**

## Imports (local guesses)
- numpy, onnx, onnxruntime, onnxruntime.tools, os, pathlib, tempfile, time, torch