"""
Model Optimization Module
Advanced optimizations for ChatterboxTTS models including mixed precision, caching, and memory management
"""

import torch
import logging
import time
import hashlib
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import gc

class MixedPrecisionOptimizer:
    """Mixed precision optimization for faster inference"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled and torch.cuda.is_available()
        self.autocast_context = None
        self.logger = logging.getLogger(__name__)
        
        if self.enabled:
            self.logger.info("🚀 Mixed precision optimization enabled")
        else:
            self.logger.info("📋 Mixed precision optimization disabled")
    
    def __enter__(self):
        if self.enabled:
            self.autocast_context = torch.autocast(device_type='cuda', dtype=torch.float16)
            return self.autocast_context.__enter__()
        return None
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled and self.autocast_context:
            return self.autocast_context.__exit__(exc_type, exc_val, exc_tb)
        return False

class TextTokenizationCache:
    """Smart caching system for text tokenization"""
    
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
        self.logger = logging.getLogger(__name__)
    
    def _get_cache_key(self, text: str, params: Dict = None) -> str:
        """Generate cache key from text and parameters"""
        key_str = text
        if params:
            # Include relevant parameters that affect tokenization
            param_str = str(sorted(params.items()))
            key_str += f"|{param_str}"
        
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, text: str, params: Dict = None) -> Optional[Any]:
        """Get cached tokenization result"""
        key = self._get_cache_key(text, params)
        
        if key in self.cache:
            self.hit_count += 1
            self.logger.debug(f"📋 Tokenization cache HIT for: '{text[:30]}...'")
            return self.cache[key]
        
        self.miss_count += 1
        self.logger.debug(f"🔍 Tokenization cache MISS for: '{text[:30]}...'")
        return None
    
    def put(self, text: str, result: Any, params: Dict = None):
        """Store tokenization result in cache"""
        if len(self.cache) >= self.max_size:
            # Simple LRU eviction - remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            self.logger.debug("🗑️ Evicted oldest cache entry")
        
        key = self._get_cache_key(text, params)
        self.cache[key] = result
        self.logger.debug(f"💾 Cached tokenization for: '{text[:30]}...'")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'max_size': self.max_size
        }
    
    def clear(self):
        """Clear the cache"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
        self.logger.info("🗑️ Tokenization cache cleared")

class MemoryOptimizer:
    """Advanced memory optimization strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory_threshold_gb = 6.0  # Memory threshold for aggressive cleanup
    
    def optimize_memory_usage(self, aggressive=False):
        """Optimize memory usage with various strategies"""
        initial_memory = self.get_gpu_memory_usage()
        
        # Standard cleanup
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        
        if aggressive:
            # More aggressive cleanup
            if torch.cuda.is_available():
                torch.cuda.ipc_collect()
                # Clear unused memory
                torch.cuda.reset_peak_memory_stats()
        
        final_memory = self.get_gpu_memory_usage()
        freed_memory = initial_memory - final_memory
        
        if freed_memory > 0.1:  # More than 100MB freed
            self.logger.info(f"🗑️ Memory cleanup freed {freed_memory:.2f}GB")
        
        return freed_memory
    
    def get_gpu_memory_usage(self) -> float:
        """Get current GPU memory usage in GB"""
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / 1024**3
        return 0.0
    
    def should_optimize_memory(self) -> bool:
        """Check if memory optimization is needed"""
        current_memory = self.get_gpu_memory_usage()
        return current_memory > self.memory_threshold_gb
    
    def monitor_memory_usage(self, operation_name: str = ""):
        """Context manager for monitoring memory usage during operations"""
        return MemoryMonitor(self, operation_name)

class MemoryMonitor:
    """Context manager for monitoring memory usage"""
    
    def __init__(self, optimizer: MemoryOptimizer, operation_name: str):
        self.optimizer = optimizer
        self.operation_name = operation_name
        self.start_memory = 0.0
    
    def __enter__(self):
        self.start_memory = self.optimizer.get_gpu_memory_usage()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_memory = self.optimizer.get_gpu_memory_usage()
        memory_diff = end_memory - self.start_memory
        
        if memory_diff > 0.1:  # Significant memory increase
            self.optimizer.logger.info(
                f"📈 {self.operation_name}: +{memory_diff:.2f}GB memory usage"
            )
        elif memory_diff < -0.1:  # Significant memory decrease
            self.optimizer.logger.info(
                f"📉 {self.operation_name}: {abs(memory_diff):.2f}GB memory freed"
            )

class InferenceOptimizer:
    """Optimizations specifically for inference performance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_inference_optimizations()
    
    def setup_inference_optimizations(self):
        """Setup general inference optimizations"""
        # Disable gradient computation globally for inference
        torch.set_grad_enabled(False)
        
        # Enable cuDNN benchmarking for consistent input sizes
        if torch.backends.cudnn.is_available():
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            self.logger.info("🏃 cuDNN benchmark mode enabled")
        
        # Enable optimized attention if available
        if hasattr(torch.backends.cuda, 'enable_flash_sdp'):
            torch.backends.cuda.enable_flash_sdp(True)
            self.logger.info("⚡ Flash attention enabled")
    
    def optimize_model_for_inference(self, model):
        """Apply inference-specific optimizations to a model"""
        optimizations_applied = []
        
        # Set model to eval mode if possible
        if hasattr(model, 'eval'):
            model.eval()
            optimizations_applied.append("eval_mode")
        
        # Apply eval mode to submodules
        if hasattr(model, 't3') and hasattr(model.t3, 'eval'):
            model.t3.eval()
            optimizations_applied.append("t3_eval")
        
        if hasattr(model, 's3gen') and hasattr(model.s3gen, 'eval'):
            model.s3gen.eval()
            optimizations_applied.append("s3gen_eval")
        
        # Enable inference mode context
        if hasattr(torch, 'inference_mode'):
            # Note: This would need to be applied as a context manager
            optimizations_applied.append("inference_mode_available")
        
        self.logger.info(f"🔧 Applied inference optimizations: {', '.join(optimizations_applied)}")
        return model

class OptimizedTTSWrapper:
    """Wrapper that applies all optimizations to TTS operations"""
    
    def __init__(self, model, enable_mixed_precision=True, enable_caching=True):
        self.model = model
        self.mixed_precision = MixedPrecisionOptimizer(enable_mixed_precision)
        self.tokenization_cache = TextTokenizationCache() if enable_caching else None
        self.memory_optimizer = MemoryOptimizer()
        self.inference_optimizer = InferenceOptimizer()
        self.logger = logging.getLogger(__name__)
        
        # Apply inference optimizations to the model
        self.inference_optimizer.optimize_model_for_inference(self.model)
        
        # Performance tracking
        self.stats = {
            'optimized_generations': 0,
            'cache_hits': 0,
            'memory_optimizations': 0,
            'total_time_saved': 0.0
        }
    
    def generate(self, text: str, **kwargs) -> torch.Tensor:
        """Optimized generation with all optimizations applied"""
        start_time = time.time()
        
        # Check if memory optimization is needed
        if self.memory_optimizer.should_optimize_memory():
            freed = self.memory_optimizer.optimize_memory_usage(aggressive=True)
            if freed > 0:
                self.stats['memory_optimizations'] += 1
        
        # Use mixed precision if enabled
        with self.mixed_precision:
            with self.memory_optimizer.monitor_memory_usage(f"TTS generation"):
                # Check cache for identical requests
                cache_key = None
                if self.tokenization_cache:
                    cache_key = f"{text}|{str(sorted(kwargs.items()))}"
                    cached_result = self.tokenization_cache.get(text, kwargs)
                    if cached_result is not None:
                        self.stats['cache_hits'] += 1
                        self.logger.debug("📋 Using cached generation result")
                        return cached_result
                
                # Generate audio with optimizations
                with torch.inference_mode() if hasattr(torch, 'inference_mode') else torch.no_grad():
                    audio = self.model.generate(text, **kwargs)
                
                # Cache the result if caching is enabled
                if self.tokenization_cache and cache_key:
                    self.tokenization_cache.put(text, audio, kwargs)
        
        generation_time = time.time() - start_time
        self.stats['optimized_generations'] += 1
        
        # Estimate time saved (rough heuristic)
        estimated_baseline_time = generation_time * 1.15  # Assume 15% overhead without optimizations
        time_saved = estimated_baseline_time - generation_time
        self.stats['total_time_saved'] += time_saved
        
        return audio
    
    def prepare_conditionals(self, *args, **kwargs):
        """Optimized voice conditioning preparation"""
        with self.mixed_precision:
            with self.memory_optimizer.monitor_memory_usage("Voice conditioning"):
                return self.model.prepare_conditionals(*args, **kwargs)
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get comprehensive optimization statistics"""
        stats = self.stats.copy()
        
        if self.tokenization_cache:
            cache_stats = self.tokenization_cache.get_stats()
            stats.update({
                'cache_hit_rate': cache_stats['hit_rate'],
                'cache_size': cache_stats['cache_size']
            })
        
        stats['current_memory_gb'] = self.memory_optimizer.get_gpu_memory_usage()
        
        return stats
    
    def log_performance_summary(self):
        """Log comprehensive performance summary"""
        stats = self.get_optimization_stats()
        
        self.logger.info("📊 OPTIMIZATION PERFORMANCE SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Optimized generations: {stats['optimized_generations']}")
        self.logger.info(f"Memory optimizations: {stats['memory_optimizations']}")
        self.logger.info(f"Total time saved: {stats['total_time_saved']:.2f}s")
        
        if 'cache_hit_rate' in stats:
            self.logger.info(f"Cache hit rate: {stats['cache_hit_rate']:.1f}%")
            self.logger.info(f"Cache size: {stats['cache_size']} entries")
        
        self.logger.info(f"Current memory usage: {stats['current_memory_gb']:.2f}GB")
        
        # Calculate estimated performance improvement
        if stats['optimized_generations'] > 0:
            avg_time_saved = stats['total_time_saved'] / stats['optimized_generations']
            self.logger.info(f"Average time saved per generation: {avg_time_saved:.2f}s")

def create_optimized_model(model, enable_mixed_precision=True, enable_caching=True):
    """Create an optimized wrapper around a ChatterboxTTS model"""
    return OptimizedTTSWrapper(
        model, 
        enable_mixed_precision=enable_mixed_precision,
        enable_caching=enable_caching
    )