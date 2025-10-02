#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch

# Ensure repo root is on sys.path (tools/ is one level under root)
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args():
    ap = argparse.ArgumentParser(description="Run a single TTS session over sample texts and report timings")
    ap.add_argument("--voice", type=str, required=True, help="Path to voice sample")
    ap.add_argument("--texts-file", type=str, default="", help="Path to a text file with one line per sample")
    ap.add_argument("--trt", choices=["auto", "on", "off"], default="auto", help="Enable TensorRT path (env override)")
    ap.add_argument("--warmup", type=int, default=1, help="Number of warmup runs before timing")
    ap.add_argument("--samples", type=int, default=5, help="Number of default samples to use if no file provided")
    return ap.parse_args()


def set_trt_env(mode: str):
    # Only influence this process; modules read at load time
    if mode == "on":
        os.environ["GENTTS_ENABLE_T3_TRT"] = "1"
    elif mode == "off":
        os.environ["GENTTS_ENABLE_T3_TRT"] = "0"
    else:
        os.environ.pop("GENTTS_ENABLE_T3_TRT", None)


def default_texts(n=5):
    base = [
        "Hello there. This is a quick test.",
        "Once upon a time, in a quiet village, a curious child asked a simple question.",
        "Technical narration: The algorithm iteratively refines the estimate using gradient updates.",
        "Dialogue: \"Are you sure?\" she asked, frowning. \"Absolutely,\" he replied.",
        "Longer line for pacing and breath control, ensuring the model hits natural prosody across clauses and commas.",
    ]
    return base[:max(1, min(n, len(base)))]


def main():
    args = parse_args()
    set_trt_env(args.trt)

    # Defer heavy imports until after env is set
    from modules.tts_engine import load_optimized_model, get_autocast

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model (includes guarded TRT enable when device is CUDA, if your code supports it)
    t0 = time.time()
    model = load_optimized_model(device)
    t_load = time.time() - t0

    # Prepare voice
    model.prepare_conditionals(args.voice)

    # Prepare texts
    texts = []
    if args.texts_file:
        p = Path(args.texts_file)
        if not p.exists():
            print(json.dumps({"error": f"texts-file not found: {p}"}))
            sys.exit(2)
        texts = [ln.strip() for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
    else:
        texts = default_texts(args.samples)

    # Warmup
    with torch.no_grad():
        with get_autocast():
            for _ in range(max(0, args.warmup)):
                _ = model.generate("Warmup line.")

    # Timed runs
    per_sample = []
    total_audio_sec = 0.0
    for i, txt in enumerate(texts):
        t1 = time.time()
        with torch.no_grad():
            with get_autocast():
                wav = model.generate(txt)
        dt = time.time() - t1
        # wav is numpy-like or tensor; infer duration if possible
        sr = getattr(model, 'sr', 24000)
        nsmps = int(wav.shape[-1]) if hasattr(wav, 'shape') else 0
        dur = float(nsmps) / float(sr) if nsmps > 0 else 0.0
        total_audio_sec += dur
        per_sample.append({
            "idx": i,
            "text_chars": len(txt),
            "audio_sec": round(dur, 3),
            "time_sec": round(dt, 3),
        })

    out = {
        "device": device,
        "trt_mode": args.trt,
        "model_load_sec": round(t_load, 3),
        "samples": per_sample,
        "total_time_sec": round(sum(s["time_sec"] for s in per_sample), 3),
        "total_audio_sec": round(total_audio_sec, 3),
    }
    # Print a single JSON line; prefix with a marker to help callers parse amid noisy stdout
    print("JSON_RESULT " + json.dumps(out))


if __name__ == "__main__":
    main()
