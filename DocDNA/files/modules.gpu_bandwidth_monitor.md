# modules.gpu_bandwidth_monitor

> GPU Memory Bandwidth Monitor

## Public API

### Classes
- **GPUSample** — Single GPU measurement sample  
  Methods: (no public methods)
- **GPUBandwidthMonitor** — Monitor GPU memory bandwidth utilization using nvidia-smi.  
  Methods: run, stop, get_statistics, print_report

### Functions
- **run** — Main monitoring loop
- **stop** — Stop monitoring
- **get_statistics** — Calculate statistics from collected samples
- **print_report** — Print formatted statistics report

## Imports (local guesses)
- dataclasses, logging, subprocess, threading, time, typing

## Side-effect signals
- subprocess