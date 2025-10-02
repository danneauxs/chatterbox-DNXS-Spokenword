# modules.vram_bandwidth_monitor

> VRAM Bandwidth Monitor for T3 Bottleneck Analysis

## Public API

### Classes
- **VRAMSnapshot**  
  Methods: (no public methods)
- **VRAMBandwidthMonitor** — Monitor VRAM bandwidth and usage during TTS inference  
  Methods: start_monitoring, stop_monitoring, print_analysis

### Functions
- **start_vram_monitoring** — Start global VRAM monitoring
- **stop_vram_monitoring_and_analyze** — Stop monitoring and print analysis
- **monitor_t3_bandwidth** — Decorator to monitor VRAM bandwidth during T3 operations
- **start_monitoring** — Start continuous VRAM monitoring
- **stop_monitoring** — Stop monitoring and return analysis
- **print_analysis** — Print detailed bandwidth analysis
- **wrapper**
- **monitor_loop**

## Imports (local guesses)
- dataclasses, datetime, re, subprocess, threading, time, typing

## Side-effect signals
- subprocess