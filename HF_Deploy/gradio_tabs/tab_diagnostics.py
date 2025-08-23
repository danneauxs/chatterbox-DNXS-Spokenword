#!/usr/bin/env python3
"""
Gradio Diagnostics Tab
Run parallel processing diagnostics through web interface
"""

import gradio as gr
import time
import threading
import multiprocessing
import concurrent.futures
import os
import sys
import torch
from pathlib import Path
import io
from contextlib import redirect_stdout

# Try to import psutil, fallback if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class DiagnosticRunner:
    def __init__(self):
        self.running = False
    
    def test_basic_multiprocessing(self):
        """Test 1: Basic multiprocessing capability"""
        output = []
        output.append("=== TEST 1: Basic Multiprocessing ===")
        
        def simple_task(n):
            return n * n
        
        try:
            # Sequential
            start = time.time()
            results_seq = [simple_task(i) for i in range(100)]
            seq_time = time.time() - start
            output.append(f"Sequential: {seq_time:.3f}s")
            
            # Parallel
            start = time.time()
            with multiprocessing.Pool(processes=4) as pool:
                results_par = pool.map(simple_task, range(100))
            par_time = time.time() - start
            output.append(f"Parallel (4 workers): {par_time:.3f}s")
            output.append(f"Speedup: {seq_time/par_time:.2f}x")
            
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_thread_vs_process(self):
        """Test 2: Threading vs Processing"""
        output = []
        output.append("=== TEST 2: Threading vs Processing ===")
        
        def cpu_task(n):
            total = 0
            for i in range(n * 1000):
                total += i * i
            return total
        
        try:
            tasks = [1000] * 8
            
            # Sequential
            start = time.time()
            seq_results = [cpu_task(t) for t in tasks]
            seq_time = time.time() - start
            output.append(f"Sequential: {seq_time:.3f}s")
            
            # Threading
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                thread_results = list(executor.map(cpu_task, tasks))
            thread_time = time.time() - start
            output.append(f"ThreadPool: {thread_time:.3f}s, speedup: {seq_time/thread_time:.2f}x")
            
            # Processing
            start = time.time()
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                process_results = list(executor.map(cpu_task, tasks))
            process_time = time.time() - start
            output.append(f"ProcessPool: {process_time:.3f}s, speedup: {seq_time/process_time:.2f}x")
            
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_gpu_access(self):
        """Test 3: GPU sharing capability"""
        output = []
        output.append("=== TEST 3: GPU Access ===")
        
        if not torch.cuda.is_available():
            output.append("No CUDA available - skipping GPU test")
            output.append("")
            return "\n".join(output)
        
        def gpu_task(worker_id):
            try:
                device = torch.device("cuda")
                x = torch.randn(1000, 1000, device=device)
                y = torch.randn(1000, 1000, device=device)
                start = time.time()
                for _ in range(10):
                    z = torch.mm(x, y)
                duration = time.time() - start
                return f"Worker {worker_id}: {duration:.3f}s"
            except Exception as e:
                return f"Worker {worker_id}: ERROR - {e}"
        
        try:
            # Sequential GPU access
            start = time.time()
            seq_results = [gpu_task(i) for i in range(4)]
            seq_time = time.time() - start
            output.append("Sequential GPU:")
            for result in seq_results:
                output.append(f"  {result}")
            output.append(f"Total sequential time: {seq_time:.3f}s")
            
            # Parallel GPU access
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                par_results = list(executor.map(gpu_task, range(4)))
            par_time = time.time() - start
            output.append("Parallel GPU:")
            for result in par_results:
                output.append(f"  {result}")
            output.append(f"Total parallel time: {par_time:.3f}s")
            
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_model_loading(self):
        """Test 4: Model loading overhead"""
        output = []
        output.append("=== TEST 4: Model Loading Simulation ===")
        
        def load_model():
            time.sleep(0.5)  # 500ms loading time
            return {"model": "loaded", "size": "large"}
        
        def task_with_model_loading(worker_id):
            start = time.time()
            model = load_model()
            processing_time = 0.1
            time.sleep(processing_time)
            total_time = time.time() - start
            return f"Worker {worker_id}: {total_time:.3f}s"
        
        try:
            output.append("Each worker loads model:")
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(task_with_model_loading, range(4)))
            total_time = time.time() - start
            
            for result in results:
                output.append(f"  {result}")
            output.append(f"Total time with per-worker loading: {total_time:.3f}s")
            
            shared_load_time = 0.5
            processing_time = 0.1 * 4
            simulated_shared_time = shared_load_time + processing_time
            output.append(f"Simulated shared model time: {simulated_shared_time:.3f}s")
            output.append(f"Overhead from per-worker loading: {total_time - simulated_shared_time:.3f}s")
            
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_environment_info(self):
        """Test 5: Environment information"""
        output = []
        output.append("=== TEST 5: Environment Info ===")
        
        try:
            output.append(f"Python version: {sys.version}")
            output.append(f"Platform: {sys.platform}")
            output.append(f"CPU cores: {multiprocessing.cpu_count()}")
            
            if PSUTIL_AVAILABLE:
                output.append(f"CPU usage: {psutil.cpu_percent()}%")
                output.append(f"Memory: {psutil.virtual_memory().percent}% used")
            else:
                output.append("psutil not available - limited system info")
            
            if torch.cuda.is_available():
                output.append(f"CUDA available: Yes")
                output.append(f"CUDA devices: {torch.cuda.device_count()}")
                output.append(f"Current device: {torch.cuda.current_device()}")
                output.append(f"Device name: {torch.cuda.get_device_name()}")
                if hasattr(torch.cuda, 'memory_summary'):
                    output.append("GPU Memory:")
                    output.append(torch.cuda.memory_summary(abbreviated=True))
            else:
                output.append("CUDA available: No")
            
            mp_vars = [
                'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'
            ]
            output.append("Threading environment variables:")
            for var in mp_vars:
                value = os.environ.get(var, 'Not set')
                output.append(f"  {var}: {value}")
                
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_worker_creation(self):
        """Test 6: Worker creation monitoring"""
        output = []
        output.append("=== TEST 6: Worker Creation ===")
        
        def monitored_task(worker_id):
            pid = os.getpid()
            tid = threading.get_ident()
            return f"Worker {worker_id}: PID={pid}, TID={tid}"
        
        try:
            output.append("Main process:")
            output.append(f"  PID: {os.getpid()}")
            output.append(f"  TID: {threading.get_ident()}")
            
            output.append("ThreadPoolExecutor workers:")
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(monitored_task, range(4)))
            for result in results:
                output.append(f"  {result}")
            
            output.append("ProcessPoolExecutor workers:")
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(monitored_task, range(4)))
            for result in results:
                output.append(f"  {result}")
                
        except Exception as e:
            output.append(f"ERROR: {e}")
        
        output.append("")
        return "\n".join(output)
    
    def test_tts_model_performance(self):
        """Test 7: Real TTS model performance"""
        output = []
        output.append("=== TEST 7: TTS Model Performance ===")
        
        try:
            # Import TTS components
            sys.path.append(str(Path(__file__).parent.parent))
            from modules.tts_engine import load_optimized_model, detect_deployment_environment
            
            # Detect environment
            env = detect_deployment_environment()
            output.append(f"🌐 Environment: {env}")
            
            # Test 1: Model loading time
            output.append("\n--- MODEL LOADING TEST ---")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            output.append(f"🚀 Loading model on {device}...")
            
            start_time = time.time()
            model = load_optimized_model(device)
            load_time = time.time() - start_time
            output.append(f"⏱️ Model load time: {load_time:.2f}s")
            
            # Test 2: Single inference timing
            output.append("\n--- SINGLE INFERENCE TEST ---")
            test_text = "Hello world, this is a test."
            
            # Warmup run
            try:
                with torch.no_grad():
                    _ = model.generate(test_text, exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                output.append("✅ Warmup completed")
            except Exception as e:
                output.append(f"⚠️ Warmup failed: {e}")
            
            # Timed run
            start_time = time.time()
            try:
                with torch.no_grad():
                    audio = model.generate(test_text, exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
                if torch.cuda.is_available():
                    torch.cuda.synchronize()
                inference_time = time.time() - start_time
                
                # Calculate realtime factor
                if hasattr(audio, 'shape'):
                    sample_rate = getattr(model, 'sr', 24000)
                    audio_duration = audio.shape[-1] / sample_rate
                    realtime_factor = audio_duration / inference_time if inference_time > 0 else 0
                    output.append(f"⏱️ Inference time: {inference_time:.3f}s")
                    output.append(f"🎵 Audio duration: {audio_duration:.3f}s")
                    output.append(f"🚀 Realtime factor: {realtime_factor:.2f}x")
                    
                    # Check if this matches your slow performance
                    if realtime_factor < 0.5:
                        output.append("⚠️ WARNING: Very slow realtime factor!")
                        output.append("   This matches your reported slow performance")
                    elif realtime_factor > 1.0:
                        output.append("✅ Good realtime factor - issue may be elsewhere")
                else:
                    output.append(f"⏱️ Inference time: {inference_time:.3f}s")
                    output.append("⚠️ Could not determine audio duration")
                    
            except Exception as e:
                output.append(f"❌ Inference failed: {e}")
            
            # Test 3: Multiple sequential runs (simulating current problem)
            output.append("\n--- SEQUENTIAL PROCESSING TEST ---")
            sequential_times = []
            for i in range(3):
                start_time = time.time()
                try:
                    with torch.no_grad():
                        _ = model.generate(f"Test run number {i+1}.", exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    run_time = time.time() - start_time
                    sequential_times.append(run_time)
                    output.append(f"  Run {i+1}: {run_time:.3f}s")
                except Exception as e:
                    output.append(f"  Run {i+1} failed: {e}")
            
            if sequential_times:
                avg_time = sum(sequential_times) / len(sequential_times)
                output.append(f"📊 Average sequential time: {avg_time:.3f}s")
                
                # Check consistency
                if max(sequential_times) - min(sequential_times) > 0.5:
                    output.append("⚠️ High variance in processing times - possible memory issues")
            
            # Test 4: Threading test with actual model
            output.append("\n--- THREADING WITH TTS MODEL TEST ---")
            try:
                def tts_worker(text_idx):
                    try:
                        start = time.time()
                        with torch.no_grad():
                            _ = model.generate(f"Threading test {text_idx}.", 
                                             exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
                        if torch.cuda.is_available():
                            torch.cuda.synchronize()
                        return time.time() - start
                    except Exception as e:
                        return f"Error: {e}"
                
                # Test with 2 workers (like current setup)
                start_time = time.time()
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    futures = [executor.submit(tts_worker, i) for i in range(4)]
                    thread_results = [f.result() for f in futures]
                
                total_thread_time = time.time() - start_time
                output.append(f"⏱️ Threading (2 workers, 4 tasks): {total_thread_time:.3f}s")
                
                successful_times = [r for r in thread_results if isinstance(r, float)]
                if successful_times:
                    output.append(f"📊 Successful tasks: {len(successful_times)}/4")
                    output.append(f"📊 Average task time: {sum(successful_times)/len(successful_times):.3f}s")
                    
                    # Compare with sequential
                    if sequential_times:
                        expected_sequential = avg_time * 4
                        speedup = expected_sequential / total_thread_time
                        output.append(f"📊 Threading speedup: {speedup:.2f}x")
                        
                        if speedup < 1.2:
                            output.append("⚠️ Threading provides minimal speedup")
                            output.append("   This explains your slow HuggingFace performance!")
                        else:
                            output.append("✅ Threading working well")
                else:
                    output.append("❌ All threading tasks failed")
                    for i, result in enumerate(thread_results):
                        output.append(f"  Task {i+1}: {result}")
                        
            except Exception as e:
                output.append(f"❌ Threading test failed: {e}")
            
            # Test 5: Model reloading overhead
            output.append("\n--- MODEL RELOADING TEST ---")
            try:
                # Simulate what might be happening in your slow processing
                reload_times = []
                for i in range(3):
                    # Delete and reload model
                    del model
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    
                    start_time = time.time()
                    model = load_optimized_model(device)
                    # Single inference after reload
                    with torch.no_grad():
                        _ = model.generate("Reload test.", exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    reload_time = time.time() - start_time
                    reload_times.append(reload_time)
                    output.append(f"  Reload + inference {i+1}: {reload_time:.3f}s")
                
                avg_reload_time = sum(reload_times) / len(reload_times)
                output.append(f"📊 Average reload + inference: {avg_reload_time:.3f}s")
                
                if sequential_times and avg_reload_time > avg_time * 2:
                    output.append("⚠️ Model reloading adds significant overhead")
                    output.append("   Workers may be reloading models per chunk!")
                    
            except Exception as e:
                output.append(f"❌ Model reloading test failed: {e}")
            
            # Cleanup
            try:
                del model
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                output.append("\n✅ Model cleanup completed")
            except:
                pass
                
        except Exception as e:
            output.append(f"❌ TTS performance test failed: {e}")
            import traceback
            output.append(f"Traceback: {traceback.format_exc()}")
            
        output.append("")
        return "\n".join(output)
    
    def run_all_diagnostics(self, progress=gr.Progress()):
        """Run all diagnostic tests"""
        if self.running:
            return "Diagnostics already running..."
        
        self.running = True
        
        try:
            results = []
            results.append("🔍 Parallel Processing Diagnostic Tool")
            results.append("=" * 50)
            results.append("")
            
            # Run each test with progress updates
            progress(0.1, desc="Environment Info...")
            results.append(self.test_environment_info())
            
            progress(0.2, desc="Basic Multiprocessing...")
            results.append(self.test_basic_multiprocessing())
            
            progress(0.4, desc="Thread vs Process...")
            results.append(self.test_thread_vs_process())
            
            progress(0.6, desc="GPU Access...")
            results.append(self.test_gpu_access())
            
            progress(0.8, desc="Model Loading...")
            results.append(self.test_model_loading())
            
            progress(0.85, desc="Worker Creation...")
            results.append(self.test_worker_creation())
            
            progress(0.95, desc="TTS Model Performance...")
            results.append(self.test_tts_model_performance())
            
            progress(1.0, desc="Complete!")
            
            results.append("🏁 Diagnostic complete!")
            results.append("")
            results.append("ANALYSIS:")
            results.append("- If basic multiprocessing is slow: Environment blocks parallelism")
            results.append("- If threading faster than processing: Use ThreadPoolExecutor")
            results.append("- If GPU parallel time >> sequential: GPU contention issue")
            results.append("- If model loading overhead high: Need model sharing strategy")
            results.append("- If same PID for all workers: Using threads, not processes")
            results.append("- If TTS realtime factor < 0.5x: Severe performance bottleneck")
            results.append("- If model reloading overhead high: Workers reloading models per chunk")
            
            return "\n".join(results)
            
        finally:
            self.running = False

# Create global diagnostic runner
diagnostic_runner = DiagnosticRunner()

def create_diagnostics_tab():
    """Create the diagnostics tab interface"""
    
    with gr.Column():
        gr.Markdown("# 🔍 System Diagnostics")
        gr.Markdown("*Test parallel processing capabilities and identify performance bottlenecks*")
        
        with gr.Row():
            run_diagnostics_btn = gr.Button("🚀 Run Full Diagnostics", variant="primary", size="lg")
            tts_diagnostics_btn = gr.Button("🎤 TTS Performance Test", variant="secondary", size="lg")
        
        with gr.Row():
            diagnostic_output = gr.Textbox(
                label="Diagnostic Results",
                lines=30,
                max_lines=50,
                interactive=False,
                show_copy_button=True
            )
        
        # Button click handlers
        run_diagnostics_btn.click(
            diagnostic_runner.run_all_diagnostics,
            outputs=[diagnostic_output]
        )
        
        tts_diagnostics_btn.click(
            diagnostic_runner.test_tts_model_performance,
            outputs=[diagnostic_output]
        )
        
        # Instructions
        with gr.Accordion("📋 How to Interpret Results", open=False):
            gr.Markdown("""
            **Key Metrics to Look For:**
            
            1. **Basic Multiprocessing Speedup**: Should be > 2x with 4 workers
            2. **ThreadPool vs ProcessPool**: Which is faster indicates best approach
            3. **GPU Sequential vs Parallel**: Large difference indicates contention
            4. **Model Loading Overhead**: High overhead means workers reload models
            5. **Worker PIDs**: Same PID = threads, different PID = processes
            
            **Common Issues:**
            - **No speedup**: Environment blocks multiprocessing
            - **GPU parallel slower**: GPU memory contention
            - **High model loading overhead**: Need shared model architecture
            - **Threading faster than processing**: Use ThreadPoolExecutor for TTS
            """)
    
    return {}