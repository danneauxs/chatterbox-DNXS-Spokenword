"""
GPU Utilization Optimizer
Smooths out GPU usage spikes and reduces dwell time through optimized processing
"""

import torch
import logging
import time
import threading
from queue import Queue, Empty
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from collections import deque

class AsyncTTSProcessor:
    """Asynchronous TTS processor with GPU utilization smoothing"""
    
    def __init__(self, model, max_queue_size=10, prefetch_count=3, batch_size=4):
        self.model = model
        self.max_queue_size = max_queue_size
        self.prefetch_count = prefetch_count
        self.batch_size = batch_size
        self.logger = logging.getLogger(__name__)
        
        # Processing queues
        self.input_queue = Queue(maxsize=max_queue_size)
        self.processing_queue = Queue(maxsize=batch_size * 2)
        self.result_queue = Queue()
        
        # Worker threads
        self.preprocessor_thread = None
        self.gpu_worker_thread = None
        self.running = False
        
        # Performance tracking
        self.stats = {
            'total_processed': 0,
            'avg_gpu_utilization': 0.0,
            'queue_efficiency': 0.0,
            'processing_time_saved': 0.0
        }
        
        # Prefetch buffer for smooth processing
        self.prefetch_buffer = deque(maxlen=prefetch_count)
        
    def start(self):
        """Start async processing threads"""
        if self.running:
            return
        
        self.running = True
        
        # Start preprocessing thread
        self.preprocessor_thread = threading.Thread(target=self._preprocessor_worker)
        self.preprocessor_thread.daemon = True
        self.preprocessor_thread.start()
        
        # Start GPU processing thread  
        self.gpu_worker_thread = threading.Thread(target=self._gpu_worker)
        self.gpu_worker_thread.daemon = True
        self.gpu_worker_thread.start()
        
        self.logger.info("🚀 Async TTS processor started")
    
    def stop(self):
        """Stop async processing"""
        self.running = False
        if self.preprocessor_thread:
            self.preprocessor_thread.join(timeout=2)
        if self.gpu_worker_thread:
            self.gpu_worker_thread.join(timeout=2)
        self.logger.info("⏹️ Async TTS processor stopped")
    
    def _preprocessor_worker(self):
        """Background text preprocessing worker"""
        while self.running:
            try:
                # Get text from input queue
                item = self.input_queue.get(timeout=0.1)
                if item is None:  # Shutdown signal
                    break
                
                text, task_id, params = item
                
                # Preprocessing operations (tokenization, text normalization, etc.)
                preprocessed = self._preprocess_text(text, params)
                
                # Add to processing queue
                self.processing_queue.put((preprocessed, task_id, params))
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Preprocessing error: {e}")
    
    def _gpu_worker(self):
        """Background GPU processing worker with batch optimization"""
        batch_buffer = []
        last_batch_time = time.time()
        batch_timeout = 0.05  # 50ms timeout for batching
        
        while self.running:
            try:
                # Try to get items for batch processing
                try:
                    item = self.processing_queue.get(timeout=0.01)
                    batch_buffer.append(item)
                except Empty:
                    pass
                
                # Process batch if conditions are met
                current_time = time.time()
                should_process = (
                    len(batch_buffer) >= self.batch_size or  # Batch is full
                    (len(batch_buffer) > 0 and current_time - last_batch_time > batch_timeout) or  # Timeout
                    not self.running  # Shutdown
                )
                
                if should_process and batch_buffer:
                    self._process_gpu_batch(batch_buffer)
                    batch_buffer.clear()
                    last_batch_time = current_time
                
                if not batch_buffer:
                    time.sleep(0.001)  # Brief sleep when no work
                    
            except Exception as e:
                self.logger.error(f"GPU worker error: {e}")
                batch_buffer.clear()
    
    def _preprocess_text(self, text: str, params: Dict) -> str:
        """Text preprocessing operations"""
        # Basic text normalization
        text = text.strip()
        
        # Could add more preprocessing here:
        # - Text tokenization
        # - Phoneme conversion
        # - Prosody analysis
        
        return text
    
    def _process_gpu_batch(self, batch_items: List[Tuple]):
        """Process a batch of items on GPU"""
        if not batch_items:
            return
        
        try:
            # Group by similar parameters for better batching
            param_groups = self._group_by_parameters(batch_items)
            
            for param_signature, items in param_groups.items():
                # Extract texts and metadata
                texts = [item[0] for item in items]  # preprocessed text
                task_ids = [item[1] for item in items]
                params = items[0][2]  # Use first item's params (they should be similar)
                
                # Single GPU call for the group
                with torch.inference_mode():
                    if len(texts) == 1:
                        # Single generation
                        audio = self.model.generate(texts[0], **params)
                        audios = [audio]
                    else:
                        # Try batch generation if available
                        try:
                            if hasattr(self.model, 'generate_batch'):
                                audios = self.model.generate_batch(texts, **params)
                            else:
                                # Fallback to sequential with GPU persistence
                                audios = []
                                for text in texts:
                                    audio = self.model.generate(text, **params)
                                    audios.append(audio)
                        except Exception:
                            # Final fallback
                            audios = []
                            for text in texts:
                                try:
                                    audio = self.model.generate(text, **params)
                                    audios.append(audio)
                                except Exception as e:
                                    self.logger.error(f"Individual generation failed: {e}")
                                    audios.append(None)
                
                # Store results
                for task_id, audio in zip(task_ids, audios):
                    self.result_queue.put((task_id, audio))
                    
                self.stats['total_processed'] += len(items)
        
        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")
            # Add None results for failed items
            for item in batch_items:
                task_id = item[1]
                self.result_queue.put((task_id, None))
    
    def _group_by_parameters(self, items: List[Tuple]) -> Dict[str, List[Tuple]]:
        """Group items by similar TTS parameters"""
        groups = {}
        
        for item in items:
            _, task_id, params = item
            
            # Create parameter signature for grouping
            sig_items = sorted(params.items()) if params else []
            param_signature = str(sig_items)
            
            if param_signature not in groups:
                groups[param_signature] = []
            groups[param_signature].append(item)
        
        return groups
    
    def generate_async(self, text: str, task_id: Optional[str] = None, **params) -> str:
        """Add text to async processing queue"""
        if task_id is None:
            task_id = f"task_{int(time.time() * 1000000)}"
        
        try:
            self.input_queue.put((text, task_id, params), timeout=1.0)
            return task_id
        except:
            raise Exception("Processing queue full")
    
    def get_result(self, timeout: float = 5.0) -> Optional[Tuple[str, torch.Tensor]]:
        """Get next completed result"""
        try:
            return self.result_queue.get(timeout=timeout)
        except Empty:
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.stats.copy()

class PipelinedTTSProcessor:
    """Pipelined TTS processor for smoother GPU utilization"""
    
    def __init__(self, model, pipeline_depth=3):
        self.model = model
        self.pipeline_depth = pipeline_depth
        self.logger = logging.getLogger(__name__)
        
        # Pipeline stages
        self.stages = ['preprocess', 'generate', 'postprocess']
        self.stage_queues = {stage: Queue(maxsize=pipeline_depth) for stage in self.stages}
        self.result_queue = Queue()
        
        # Worker threads
        self.workers = {}
        self.running = False
        
        # Performance tracking
        self.pipeline_stats = {
            'throughput': 0.0,
            'gpu_efficiency': 0.0,
            'stage_utilization': {stage: 0.0 for stage in self.stages}
        }
    
    def start(self):
        """Start pipelined processing"""
        if self.running:
            return
        
        self.running = True
        
        # Start workers for each stage
        self.workers['preprocess'] = threading.Thread(target=self._preprocess_worker)
        self.workers['generate'] = threading.Thread(target=self._generate_worker)
        self.workers['postprocess'] = threading.Thread(target=self._postprocess_worker)
        
        for worker in self.workers.values():
            worker.daemon = True
            worker.start()
        
        self.logger.info("🔄 Pipelined TTS processor started")
    
    def stop(self):
        """Stop pipelined processing"""
        self.running = False
        for worker in self.workers.values():
            if worker.is_alive():
                worker.join(timeout=1)
        self.logger.info("⏸️ Pipelined TTS processor stopped")
    
    def _preprocess_worker(self):
        """Preprocessing pipeline stage"""
        while self.running:
            try:
                item = self.stage_queues['preprocess'].get(timeout=0.1)
                if item is None:
                    break
                
                text, task_id, params = item
                
                # Text preprocessing
                processed_text = text.strip()  # Basic processing
                
                # Pass to next stage
                self.stage_queues['generate'].put((processed_text, task_id, params))
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Preprocess stage error: {e}")
    
    def _generate_worker(self):
        """GPU generation pipeline stage (critical path)"""
        while self.running:
            try:
                item = self.stage_queues['generate'].get(timeout=0.1)
                if item is None:
                    break
                
                text, task_id, params = item
                
                # GPU TTS generation
                start_time = time.time()
                with torch.inference_mode():
                    audio = self.model.generate(text, **params)
                generation_time = time.time() - start_time
                
                # Pass to next stage
                self.stage_queues['postprocess'].put((audio, task_id, generation_time))
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Generate stage error: {e}")
                # Pass error result
                self.stage_queues['postprocess'].put((None, item[1] if 'item' in locals() else 'unknown', 0))
    
    def _postprocess_worker(self):
        """Post-processing pipeline stage"""
        while self.running:
            try:
                item = self.stage_queues['postprocess'].get(timeout=0.1)
                if item is None:
                    break
                
                audio, task_id, generation_time = item
                
                # Post-processing (normalization, format conversion, etc.)
                # For now, just pass through
                processed_audio = audio
                
                # Store final result
                self.result_queue.put((task_id, processed_audio, generation_time))
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Postprocess stage error: {e}")
    
    def generate_pipelined(self, text: str, task_id: Optional[str] = None, **params) -> str:
        """Add text to pipelined processing"""
        if task_id is None:
            task_id = f"pipeline_{int(time.time() * 1000000)}"
        
        try:
            self.stage_queues['preprocess'].put((text, task_id, params), timeout=1.0)
            return task_id
        except:
            raise Exception("Pipeline queue full")
    
    def get_result(self, timeout: float = 10.0) -> Optional[Tuple[str, torch.Tensor, float]]:
        """Get next completed result from pipeline"""
        try:
            return self.result_queue.get(timeout=timeout)
        except Empty:
            return None

class SmoothGPUOptimizer:
    """Main GPU utilization optimizer combining multiple strategies"""
    
    def __init__(self, model, strategy='async'):
        self.model = model
        self.strategy = strategy
        self.logger = logging.getLogger(__name__)
        
        # Initialize chosen strategy
        if strategy == 'async':
            self.processor = AsyncTTSProcessor(model, max_queue_size=15, batch_size=3)
        elif strategy == 'pipeline':
            self.processor = PipelinedTTSProcessor(model, pipeline_depth=4)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        # Start processing
        self.processor.start()
        
        # Performance tracking
        self.optimization_stats = {
            'strategy': strategy,
            'utilization_improvement': 0.0,
            'throughput_improvement': 0.0,
            'dwell_time_reduction': 0.0
        }
    
    def generate_optimized(self, texts: List[str], **params) -> List[torch.Tensor]:
        """Generate audio with optimized GPU utilization"""
        if not texts:
            return []
        
        results = []
        task_ids = []
        
        # Submit all texts for processing
        for i, text in enumerate(texts):
            if self.strategy == 'async':
                task_id = self.processor.generate_async(text, f"batch_{i}", **params)
            else:  # pipeline
                task_id = self.processor.generate_pipelined(text, f"batch_{i}", **params)
            task_ids.append(task_id)
        
        # Collect results
        completed = {}
        while len(completed) < len(task_ids):
            result = self.processor.get_result(timeout=15.0)
            if result is None:
                self.logger.warning("Timeout waiting for results")
                break
            
            if self.strategy == 'async':
                task_id, audio = result
            else:  # pipeline
                task_id, audio, gen_time = result
            
            completed[task_id] = audio
        
        # Order results to match input order
        for task_id in task_ids:
            results.append(completed.get(task_id))
        
        return results
    
    def cleanup(self):
        """Clean up processor resources"""
        if hasattr(self.processor, 'stop'):
            self.processor.stop()
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        stats = self.optimization_stats.copy()
        if hasattr(self.processor, 'get_stats'):
            processor_stats = self.processor.get_stats()
            stats.update({f'processor_{k}': v for k, v in processor_stats.items()})
        return stats

def create_gpu_optimizer(model, strategy='async'):
    """Create GPU utilization optimizer"""
    return SmoothGPUOptimizer(model, strategy=strategy)