# lora

## Public API

### Classes
- **MetricsTracker**  
  Methods: add_metrics, stop
- **LoRALayer** — LoRA adapter layer  
  Methods: forward
- **AudioSample** — Container for audio sample data  
  Methods: (no public methods)
- **TTSDataset** — Dataset handling  
  Methods: (no public methods)

### Functions
- **inject_lora_layers**
- **prepare_batch_conditionals**
- **compute_loss**
- **main** — Main training function
- **load_audio_samples** — Load audio files and generate transcripts using Whisper
- **save_checkpoint** — Save training checkpoint
- **merge_lora_weights** — Merge LoRA weights into the base model
- **save_lora_adapter** — Save LoRA adapter weights and configuration
- **load_lora_adapter** — Load LoRA adapter weights
- **collate_fn** — Custom collate function for DataLoader
- **add_metrics** — Add metrics to the tracker
- **stop** — Stop the metrics tracker
- **forward**
- **make_new_forward**
- **new_forward**

## Imports (local guesses)
- chatterbox.models.s3gen, chatterbox.models.s3tokenizer, chatterbox.models.t3.modules.cond_enc, chatterbox.models.tokenizers, chatterbox.models.voice_encoder, chatterbox.tts, collections, dataclasses, datetime, huggingface_hub, json, librosa, matplotlib, matplotlib.patches, matplotlib.pyplot, numpy, os, pathlib, random, shutil, threading, time, torch, torch.nn, torch.nn.functional, torch.optim, torch.optim.lr_scheduler, torch.utils.data, tqdm, transformers, typing, warnings

## Entrypoint
- Contains `if __name__ == '__main__':` block