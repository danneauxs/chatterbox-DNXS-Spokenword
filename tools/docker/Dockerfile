FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TRANSFORMERS_NO_ADVISORY_WARNINGS=1 \
    HF_HUB_DISABLE_SYMLINKS_WARNING=1

WORKDIR /workspace

# Minimal OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Known-good exporter toolchain (CPU)
RUN python -m pip install --upgrade pip && \
    python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu \
        torch==2.0.1+cpu \
        transformers==4.31.0 \
        onnx==1.14.0 \
        safetensors==0.4.2 \
        numpy==1.26.4 \
        protobuf==4.25.3 \
        packaging==24.1 \
        sympy==1.12 \
        networkx==3.2.1 \
        einops==0.8.1

# Default command: export full ONNX
ENV PYTHONPATH=/workspace:/workspace/Chatterbox_API
CMD ["bash", "-lc", "python tools/export_t3_onnx.py"]
