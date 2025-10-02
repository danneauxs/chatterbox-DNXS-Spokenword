# modules.bandwidth_monitor

> Real-time Memory Bandwidth Monitor for TTS Inference

## Public API

### Classes
- **RealTimeBandwidthMonitor** — Monitor GPU memory bandwidth during TTS inference  
  Methods: start_monitoring, stop_monitoring
- **TTSBandwidthProfiler** — Profile memory bandwidth during TTS operations  
  Methods: profile_tts_generation

### Functions
- **monitor_tts_bandwidth** — Convenience function to monitor TTS bandwidth
- **start_monitoring** — Start real-time bandwidth monitoring
- **stop_monitoring** — Stop monitoring and return results
- **profile_tts_generation** — Profile bandwidth during TTS generation

## Imports (local guesses)
- pathlib, psutil, queue, subprocess, threading, time

## Side-effect signals
- subprocess