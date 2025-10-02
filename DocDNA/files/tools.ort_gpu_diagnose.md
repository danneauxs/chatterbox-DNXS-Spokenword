# tools.ort_gpu_diagnose

> ORT/Torch GPU environment diagnostic.

## Public API


### Functions
- **print_header**
- **find_shadowing_modules**
- **show_python_env**
- **show_shadowing**
- **try_import_onnxruntime**
- **try_torch_cuda**
- **try_nvidia_smi**
- **maybe_run_onnx_test**
- **print_next_steps_hint**
- **main**

## Imports (local guesses)
- __future__, argparse, importlib, importlib.util, onnxruntime, os, shutil, site, subprocess, sys, textwrap, torch, typing

## Framework signals
- argparse

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block