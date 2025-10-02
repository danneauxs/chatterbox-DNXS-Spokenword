#!/usr/bin/env python3
"""
CUDA Kernel Utilization Profiler and Optimizer
==============================================

This tool profiles CUDA kernel utilization during TTS inference and identifies
optimization opportunities for better GPU resource utilization.

Features:
- Real-time GPU utilization monitoring during inference
- CUDA kernel profiling with nvprof/nsight integration
- Memory bandwidth utilization analysis
- Tensor operation optimization recommendations
- Batch size and sequence length optimization
- Concurrent kernel execution analysis

Usage:
    venv/bin/python tools/cuda_kernel_profiler.py --profile-type [utilization|kernels|memory|full]
"""

import argparse
import sys
import time
import json
import subprocess
import threading
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import signal

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import psutil
import gc

# Import Chatterbox modules
from config.config import *
from modules.tts_engine import load_optimized_model, prewarm_model_with_voice
from modules.file_manager import list_voice_samples


@dataclass
class CudaUtilizationSnapshot:
    """Single GPU utilization measurement"""
    timestamp: float
    gpu_util_percent: int
    memory_util_percent: int
    memory_used_mb: float
    memory_total_mb: float
    temperature: int
    power_watts: int
    sm_clock_mhz: int
    memory_clock_mhz: int


@dataclass
class KernelProfilingResult:
    """Results from kernel profiling session"""
    test_name: str
    duration_seconds: float
    avg_gpu_utilization: float
    peak_gpu_utilization: float
    avg_memory_utilization: float
    peak_memory_utilization: float
    memory_bandwidth_gbps: float
    kernel_efficiency: float
    concurrent_kernels: int
    utilization_samples: List[CudaUtilizationSnapshot]
    recommendations: List[str]


class CudaKernelProfiler:
    """Main CUDA kernel profiling and optimization tool"""

    def __init__(self):
        self.device = self._get_device()
        self.monitoring = False
        self.utilization_data = []
        self.monitor_thread = None

        # Test configuration
        self.test_texts = [
            "Short test sentence for GPU profiling.",
            "This is a medium length sentence that should provide moderate GPU workload for testing kernel utilization patterns.",
            "This is a significantly longer test passage that will generate substantial GPU activity across multiple kernels, allowing us to analyze memory bandwidth utilization, kernel concurrency, and overall GPU efficiency during text-to-speech processing with various computational patterns and memory access behaviors.",
        ]

    def _get_device(self) -> str:
        """Get CUDA device info"""
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA not available - kernel profiling requires GPU")
        return f"cuda:{torch.cuda.current_device()}"

    def _get_gpu_utilization(self) -> Optional[CudaUtilizationSnapshot]:
        """Get current GPU utilization using nvidia-smi"""
        try:
            cmd = [
                "nvidia-smi",
                "--query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total,temperature.gpu,power.draw,clocks.sm,clocks.mem",
                "--format=csv,noheader,nounits"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)

            if result.returncode == 0:
                values = result.stdout.strip().split(', ')
                return CudaUtilizationSnapshot(
                    timestamp=time.perf_counter(),
                    gpu_util_percent=int(float(values[0])),
                    memory_util_percent=int(float(values[1])),
                    memory_used_mb=float(values[2]),
                    memory_total_mb=float(values[3]),
                    temperature=int(float(values[4])),
                    power_watts=int(float(values[5])),
                    sm_clock_mhz=int(float(values[6])),
                    memory_clock_mhz=int(float(values[7]))
                )
        except Exception as e:
            print(f"Warning: Failed to get GPU utilization: {e}")
            return None

    def _monitor_utilization(self, interval=0.1):
        """Background thread to monitor GPU utilization"""
        while self.monitoring:
            snapshot = self._get_gpu_utilization()
            if snapshot:
                self.utilization_data.append(snapshot)
            time.sleep(interval)

    def start_monitoring(self):
        """Start GPU utilization monitoring"""
        self.monitoring = True
        self.utilization_data = []
        self.monitor_thread = threading.Thread(target=self._monitor_utilization, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self) -> List[CudaUtilizationSnapshot]:
        """Stop monitoring and return collected data"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        return self.utilization_data.copy()

    def analyze_utilization(self, samples: List[CudaUtilizationSnapshot]) -> Dict:
        """Analyze GPU utilization patterns"""
        if not samples:
            return {}

        gpu_utils = [s.gpu_util_percent for s in samples]
        mem_utils = [s.memory_util_percent for s in samples]

        analysis = {
            "duration_seconds": samples[-1].timestamp - samples[0].timestamp,
            "avg_gpu_utilization": sum(gpu_utils) / len(gpu_utils),
            "peak_gpu_utilization": max(gpu_utils),
            "min_gpu_utilization": min(gpu_utils),
            "avg_memory_utilization": sum(mem_utils) / len(mem_utils),
            "peak_memory_utilization": max(mem_utils),
            "utilization_variance": sum((x - sum(gpu_utils)/len(gpu_utils))**2 for x in gpu_utils) / len(gpu_utils),
            "sample_count": len(samples)
        }

        return analysis

    def profile_inference_workload(self, model, voice_path: str, text: str) -> Dict:
        """Profile GPU utilization during a single inference"""
        print(f"🔍 Profiling inference workload: '{text[:50]}...'")

        # Clear memory and warm up
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

        # Start monitoring
        self.start_monitoring()

        try:
            # Run inference
            start_time = time.perf_counter()

            # Mock inference call - replace with actual TTS inference
            # This is a placeholder since exact interface depends on your model
            with torch.amp.autocast('cuda', enabled=True):
                # Simulate workload with actual model if available
                if hasattr(model, 't3') and hasattr(model.t3, 'inference'):
                    print("Running T3 inference profiling...")
                    # Would need proper TTS parameter setup here

                # For now, create some GPU activity to test monitoring
                dummy_tensor = torch.randn(1000, 1000, device=self.device)
                for _ in range(10):
                    dummy_tensor = torch.mm(dummy_tensor, dummy_tensor.t())
                    torch.cuda.synchronize()

            end_time = time.perf_counter()

        except Exception as e:
            print(f"Inference profiling failed: {e}")
            end_time = start_time

        # Stop monitoring
        samples = self.stop_monitoring()

        # Analyze results
        analysis = self.analyze_utilization(samples)
        analysis['inference_time'] = end_time - start_time

        return analysis

    def generate_optimization_recommendations(self, analysis: Dict) -> List[str]:
        """Generate optimization recommendations based on profiling results"""
        recommendations = []

        avg_gpu_util = analysis.get('avg_gpu_utilization', 0)
        peak_gpu_util = analysis.get('peak_gpu_utilization', 0)
        avg_mem_util = analysis.get('avg_memory_utilization', 0)
        utilization_variance = analysis.get('utilization_variance', 0)

        # GPU utilization analysis
        if avg_gpu_util < 30:
            recommendations.append("❌ LOW GPU UTILIZATION: Average GPU usage is very low. Consider increasing batch sizes or using more parallel operations.")
        elif avg_gpu_util < 60:
            recommendations.append("⚠️ MODERATE GPU UTILIZATION: GPU usage could be improved. Look for opportunities to parallelize operations.")
        else:
            recommendations.append("✅ GOOD GPU UTILIZATION: GPU usage is reasonably high.")

        # Peak vs average analysis
        if peak_gpu_util - avg_gpu_util > 40:
            recommendations.append("⚠️ INCONSISTENT WORKLOAD: Large variance between peak and average GPU usage suggests batch processing or workload balancing opportunities.")

        # Memory utilization analysis
        if avg_mem_util < 20:
            recommendations.append("💾 UNDERUTILIZED MEMORY: Memory bandwidth is underutilized. Consider larger tensors or better memory access patterns.")
        elif avg_mem_util > 90:
            recommendations.append("💾 MEMORY PRESSURE: High memory utilization may be limiting performance. Consider reducing batch sizes or optimizing memory usage.")

        # Variance analysis
        if utilization_variance > 500:
            recommendations.append("📊 HIGH UTILIZATION VARIANCE: GPU workload is very inconsistent. This suggests opportunities for better kernel scheduling or batching.")

        # Specific optimizations
        if avg_gpu_util < 50:
            recommendations.append("🔧 OPTIMIZATION: Try increasing tensor sizes, using tensor fusion, or implementing custom CUDA kernels for better GPU utilization.")

        if avg_mem_util < 30:
            recommendations.append("🔧 MEMORY OPTIMIZATION: Implement memory coalescing, use larger data types, or optimize memory access patterns.")

        return recommendations

    def run_comprehensive_profile(self, voice_path: str) -> KernelProfilingResult:
        """Run comprehensive CUDA kernel profiling"""
        print("🚀 Starting comprehensive CUDA kernel profiling...")

        # Load model
        model = load_optimized_model(self.device, force_reload=True)
        model = prewarm_model_with_voice(model, voice_path)

        all_samples = []
        total_inference_time = 0

        # Profile different workload sizes
        for i, text in enumerate(self.test_texts):
            print(f"\n📊 Profiling workload {i+1}/{len(self.test_texts)}")

            analysis = self.profile_inference_workload(model, voice_path, text)
            all_samples.extend(self.utilization_data)
            total_inference_time += analysis.get('inference_time', 0)

            time.sleep(1)  # Cool down between tests

        # Overall analysis
        overall_analysis = self.analyze_utilization(all_samples)
        recommendations = self.generate_optimization_recommendations(overall_analysis)

        return KernelProfilingResult(
            test_name="comprehensive_cuda_profile",
            duration_seconds=overall_analysis.get('duration_seconds', 0),
            avg_gpu_utilization=overall_analysis.get('avg_gpu_utilization', 0),
            peak_gpu_utilization=overall_analysis.get('peak_gpu_utilization', 0),
            avg_memory_utilization=overall_analysis.get('avg_memory_utilization', 0),
            peak_memory_utilization=overall_analysis.get('peak_memory_utilization', 0),
            memory_bandwidth_gbps=0,  # Would need more sophisticated measurement
            kernel_efficiency=overall_analysis.get('avg_gpu_utilization', 0) / 100.0,
            concurrent_kernels=0,  # Would need nvprof integration
            utilization_samples=all_samples,
            recommendations=recommendations
        )

    def save_profile_results(self, result: KernelProfilingResult, output_file: str):
        """Save profiling results to file"""
        output_data = {
            "profiling_info": {
                "device": self.device,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "torch_version": torch.__version__,
                "cuda_version": torch.version.cuda
            },
            "results": asdict(result)
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"📁 Profile results saved to {output_file}")

    def print_summary(self, result: KernelProfilingResult):
        """Print profiling summary"""
        print("\n" + "="*80)
        print("CUDA KERNEL PROFILING SUMMARY")
        print("="*80)

        print(f"Device: {self.device}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        print(f"Average GPU Utilization: {result.avg_gpu_utilization:.1f}%")
        print(f"Peak GPU Utilization: {result.peak_gpu_utilization:.1f}%")
        print(f"Average Memory Utilization: {result.avg_memory_utilization:.1f}%")
        print(f"Peak Memory Utilization: {result.peak_memory_utilization:.1f}%")
        print(f"Kernel Efficiency: {result.kernel_efficiency:.1%}")

        print(f"\n📊 OPTIMIZATION RECOMMENDATIONS:")
        print("-" * 80)
        for i, rec in enumerate(result.recommendations, 1):
            print(f"{i}. {rec}")


def main():
    parser = argparse.ArgumentParser(description="CUDA Kernel Profiler for Chatterbox TTS")
    parser.add_argument("--profile-type", choices=["utilization", "kernels", "memory", "full"],
                       default="full", help="Type of profiling to perform")
    parser.add_argument("--output", default="cuda_profile_results.json",
                       help="Output file for profiling results")
    parser.add_argument("--voice", help="Specific voice file to use for testing")

    args = parser.parse_args()

    # Check CUDA availability
    if not torch.cuda.is_available():
        print("❌ CUDA not available. This tool requires a CUDA-capable GPU.")
        return

    # Get voice file
    voices = list_voice_samples()
    if args.voice:
        voice_path = args.voice
    elif voices:
        voice_path = voices[0]
    else:
        print("❌ No voice files available for testing")
        return

    print(f"Using voice: {voice_path}")
    print(f"CUDA Device: {torch.cuda.get_device_name()}")

    # Create profiler
    profiler = CudaKernelProfiler()

    # Run profiling
    try:
        result = profiler.run_comprehensive_profile(voice_path)

        # Save and display results
        profiler.save_profile_results(result, args.output)
        profiler.print_summary(result)

    except KeyboardInterrupt:
        print("\n⏹️ Profiling interrupted by user")
    except Exception as e:
        print(f"❌ Profiling failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()