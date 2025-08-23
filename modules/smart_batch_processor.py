"""
Smart Batch Processing Module
Optimizes TTS generation by intelligently batching chunks with similar parameters
"""

import json
import time
import logging
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Tuple, Any
import torch

class SmartBatchProcessor:
    """Intelligent batch processing for JSON-based TTS chunks with varying parameters"""
    
    def __init__(self, model, tolerance=0.05, min_batch_size=2, max_batch_size=8):
        """
        Initialize smart batch processor
        
        Args:
            model: ChatterboxTTS model instance
            tolerance: Parameter tolerance for grouping (0.05 = 5% variation allowed)
            min_batch_size: Minimum chunks to form a batch
            max_batch_size: Maximum chunks per batch (memory/performance limit)
        """
        self.model = model
        self.tolerance = tolerance
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.logger = logging.getLogger(__name__)
        
        # Performance tracking
        self.stats = {
            'total_chunks': 0,
            'batched_chunks': 0,
            'individual_chunks': 0,
            'batch_groups': 0,
            'total_time': 0,
            'batch_time': 0,
            'individual_time': 0
        }
    
    def analyze_chunk_distribution(self, chunks: List[Dict]) -> Dict:
        """
        Analyze parameter distribution and batching potential
        
        Args:
            chunks: List of chunk dictionaries with tts_params
            
        Returns:
            Dictionary with analysis results
        """
        if not chunks:
            return {'error': 'No chunks provided'}
        
        # Extract parameters
        param_combos = []
        for chunk in chunks:
            if 'tts_params' not in chunk:
                continue
                
            params = chunk['tts_params']
            combo = (
                round(params.get('exaggeration', 0.5), 3),
                round(params.get('cfg_weight', 0.5), 3),
                round(params.get('temperature', 0.8), 3),
                round(params.get('min_p', 0.05), 3),
                round(params.get('repetition_penalty', 1.2), 3)
            )
            param_combos.append(combo)
        
        # Count combinations
        combo_counts = Counter(param_combos)
        unique_combos = len(combo_counts)
        
        # Calculate batching potential
        exact_batchable = sum(count for count in combo_counts.values() if count >= self.min_batch_size)
        
        # Estimate tolerant batching potential
        tolerant_groups = self._estimate_tolerant_groups(param_combos)
        tolerant_batchable = sum(len(group) for group in tolerant_groups if len(group) >= self.min_batch_size)
        
        analysis = {
            'total_chunks': len(chunks),
            'unique_combinations': unique_combos,
            'exact_batchable': exact_batchable,
            'exact_batch_percentage': (exact_batchable / len(chunks)) * 100,
            'tolerant_batchable': tolerant_batchable,
            'tolerant_batch_percentage': (tolerant_batchable / len(chunks)) * 100,
            'most_common_combos': combo_counts.most_common(5),
            'estimated_speedup': self._estimate_speedup(len(chunks), exact_batchable, tolerant_batchable)
        }
        
        return analysis
    
    def _estimate_tolerant_groups(self, param_combos: List[Tuple]) -> List[List[int]]:
        """Estimate grouping with tolerance"""
        groups = []
        used = set()
        
        for i, combo1 in enumerate(param_combos):
            if i in used:
                continue
                
            group = [i]
            used.add(i)
            
            for j, combo2 in enumerate(param_combos[i+1:], i+1):
                if j in used:
                    continue
                    
                if self._params_within_tolerance(combo1, combo2):
                    group.append(j)
                    used.add(j)
            
            groups.append(group)
        
        return groups
    
    def _params_within_tolerance(self, params1: Tuple, params2: Tuple) -> bool:
        """Check if two parameter sets are within tolerance"""
        for p1, p2 in zip(params1, params2):
            if abs(p1 - p2) > self.tolerance:
                return False
        return True
    
    def _estimate_speedup(self, total_chunks: int, exact_batchable: int, tolerant_batchable: int) -> Dict:
        """Estimate performance improvements"""
        # Assume batch processing is 3x faster per chunk
        batch_factor = 3.0
        
        # Exact batching
        exact_individual = total_chunks - exact_batchable
        exact_time = (exact_batchable / batch_factor) + exact_individual
        exact_speedup = total_chunks / exact_time
        
        # Tolerant batching  
        tolerant_individual = total_chunks - tolerant_batchable
        tolerant_time = (tolerant_batchable / batch_factor) + tolerant_individual
        tolerant_speedup = total_chunks / tolerant_time
        
        return {
            'exact_speedup': exact_speedup,
            'tolerant_speedup': tolerant_speedup,
            'potential_time_savings': {
                'exact': ((total_chunks - exact_time) / total_chunks) * 100,
                'tolerant': ((total_chunks - tolerant_time) / total_chunks) * 100
            }
        }
    
    def group_chunks_for_batching(self, chunks: List[Dict], use_tolerance: bool = True) -> Dict:
        """
        Group chunks for optimal batching
        
        Args:
            chunks: List of chunk dictionaries
            use_tolerance: Whether to use parameter tolerance for grouping
            
        Returns:
            Dictionary with batch groups and individual chunks
        """
        if not chunks:
            return {'batch_groups': [], 'individual_chunks': []}
        
        # Create parameter signatures for grouping
        param_groups = defaultdict(list)
        
        for i, chunk in enumerate(chunks):
            if 'tts_params' not in chunk:
                # Skip chunks without TTS parameters
                continue
            
            params = chunk['tts_params']
            
            if use_tolerance:
                # Round to tolerance level for grouping
                signature = (
                    round(params.get('exaggeration', 0.5) / self.tolerance) * self.tolerance,
                    round(params.get('cfg_weight', 0.5) / self.tolerance) * self.tolerance,
                    round(params.get('temperature', 0.8) / self.tolerance) * self.tolerance,
                    round(params.get('min_p', 0.05) / self.tolerance) * self.tolerance,
                    round(params.get('repetition_penalty', 1.2) / self.tolerance) * self.tolerance
                )
            else:
                # Exact parameter matching
                signature = (
                    params.get('exaggeration', 0.5),
                    params.get('cfg_weight', 0.5),
                    params.get('temperature', 0.8),
                    params.get('min_p', 0.05),
                    params.get('repetition_penalty', 1.2)
                )
            
            param_groups[signature].append((i, chunk))
        
        # Separate into batch groups and individual chunks
        batch_groups = []
        individual_chunks = []
        
        for signature, group_chunks in param_groups.items():
            if len(group_chunks) >= self.min_batch_size:
                # Split large groups into smaller batches
                for i in range(0, len(group_chunks), self.max_batch_size):
                    batch = group_chunks[i:i + self.max_batch_size]
                    if len(batch) >= self.min_batch_size:
                        batch_groups.append({
                            'signature': signature,
                            'chunks': batch,
                            'params': self._calculate_average_params([chunk for _, chunk in batch])
                        })
                    else:
                        individual_chunks.extend(batch)
            else:
                individual_chunks.extend(group_chunks)
        
        self.logger.info(f"📊 Batching analysis: {len(batch_groups)} batch groups, {len(individual_chunks)} individual chunks")
        
        return {
            'batch_groups': batch_groups,
            'individual_chunks': individual_chunks
        }
    
    def _calculate_average_params(self, chunks: List[Dict]) -> Dict:
        """Calculate average TTS parameters for a group"""
        if not chunks:
            return {}
        
        param_sums = defaultdict(float)
        param_counts = defaultdict(int)
        
        for chunk in chunks:
            params = chunk.get('tts_params', {})
            for key, value in params.items():
                if isinstance(value, (int, float)):
                    param_sums[key] += value
                    param_counts[key] += 1
        
        # Calculate averages
        avg_params = {}
        for key in param_sums:
            if param_counts[key] > 0:
                avg_params[key] = param_sums[key] / param_counts[key]
        
        return avg_params
    
    def process_chunks_with_smart_batching(self, chunks: List[Dict], use_tolerance: bool = True) -> List[torch.Tensor]:
        """
        Process chunks using smart batching for optimal performance
        
        Args:
            chunks: List of chunk dictionaries from JSON
            use_tolerance: Whether to use parameter tolerance
            
        Returns:
            List of audio tensors in original chunk order
        """
        if not chunks:
            return []
        
        start_time = time.time()
        self.stats['total_chunks'] = len(chunks)
        
        # Group chunks for batching
        grouping = self.group_chunks_for_batching(chunks, use_tolerance)
        batch_groups = grouping['batch_groups']
        individual_chunks = grouping['individual_chunks']
        
        # Initialize results array
        results = [None] * len(chunks)
        
        # Process batch groups
        batch_start = time.time()
        for group in batch_groups:
            self.logger.info(f"🔥 Processing batch of {len(group['chunks'])} chunks")
            
            # Extract texts and parameters
            texts = [chunk['text'] for _, chunk in group['chunks']]
            indices = [idx for idx, _ in group['chunks']]
            params = group['params']
            
            try:
                # Batch generate
                batch_start_time = time.time()
                audio_batch = self.model.generate_batch(
                    texts,
                    exaggeration=params.get('exaggeration', 0.5),
                    cfg_weight=params.get('cfg_weight', 0.5),
                    temperature=params.get('temperature', 0.8),
                    min_p=params.get('min_p', 0.05),
                    top_p=params.get('top_p', 1.0),
                    repetition_penalty=params.get('repetition_penalty', 1.2)
                )
                batch_time = time.time() - batch_start_time
                
                # Store results in correct positions
                for idx, audio in zip(indices, audio_batch):
                    results[idx] = audio
                
                self.stats['batched_chunks'] += len(group['chunks'])
                self.logger.info(f"   ✅ Batch completed in {batch_time:.2f}s ({len(texts)} chunks)")
                
            except Exception as e:
                self.logger.error(f"❌ Batch processing failed: {e}")
                # Fallback to individual processing
                for idx, chunk in group['chunks']:
                    individual_chunks.append((idx, chunk))
        
        self.stats['batch_time'] = time.time() - batch_start
        
        # Process individual chunks
        individual_start = time.time()
        for idx, chunk in individual_chunks:
            self.logger.info(f"🔧 Processing individual chunk {idx}")
            
            try:
                params = chunk.get('tts_params', {})
                audio = self.model.generate(
                    chunk['text'],
                    exaggeration=params.get('exaggeration', 0.5),
                    cfg_weight=params.get('cfg_weight', 0.5),
                    temperature=params.get('temperature', 0.8),
                    min_p=params.get('min_p', 0.05),
                    top_p=params.get('top_p', 1.0),
                    repetition_penalty=params.get('repetition_penalty', 1.2)
                )
                results[idx] = audio
                self.stats['individual_chunks'] += 1
                
            except Exception as e:
                self.logger.error(f"❌ Individual chunk {idx} failed: {e}")
                # Create silent audio as fallback
                results[idx] = torch.zeros(1, 24000)  # 1 second of silence
        
        self.stats['individual_time'] = time.time() - individual_start
        self.stats['batch_groups'] = len(batch_groups)
        self.stats['total_time'] = time.time() - start_time
        
        # Log performance summary
        self._log_performance_summary()
        
        return results
    
    def _log_performance_summary(self):
        """Log performance statistics"""
        stats = self.stats
        
        self.logger.info("📊 SMART BATCH PROCESSING SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Total chunks processed: {stats['total_chunks']}")
        self.logger.info(f"Batched chunks: {stats['batched_chunks']} ({stats['batched_chunks']/stats['total_chunks']*100:.1f}%)")
        self.logger.info(f"Individual chunks: {stats['individual_chunks']} ({stats['individual_chunks']/stats['total_chunks']*100:.1f}%)")
        self.logger.info(f"Batch groups: {stats['batch_groups']}")
        self.logger.info(f"Total time: {stats['total_time']:.2f}s")
        self.logger.info(f"Batch processing time: {stats['batch_time']:.2f}s")
        self.logger.info(f"Individual processing time: {stats['individual_time']:.2f}s")
        
        # Calculate estimated speedup
        if stats['total_chunks'] > 0:
            # Estimate what individual processing would have taken
            avg_individual_time = stats['individual_time'] / max(stats['individual_chunks'], 1)
            estimated_individual_total = avg_individual_time * stats['total_chunks']
            actual_speedup = estimated_individual_total / stats['total_time'] if stats['total_time'] > 0 else 1.0
            
            self.logger.info(f"Estimated speedup: {actual_speedup:.2f}x")
            self.logger.info(f"Time saved: {estimated_individual_total - stats['total_time']:.1f}s")

def load_chunks_from_json(json_path: str) -> List[Dict]:
    """
    Load chunks from JSON file
    
    Args:
        json_path: Path to chunks JSON file
        
    Returns:
        List of chunk dictionaries
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter out metadata entries
        chunks = [item for item in data if isinstance(item, dict) and 'text' in item]
        return chunks
        
    except Exception as e:
        logging.error(f"Failed to load JSON file {json_path}: {e}")
        return []

def demo_smart_batching(json_path: str, model):
    """
    Demonstrate smart batching with a JSON file
    
    Args:
        json_path: Path to chunks JSON file
        model: ChatterboxTTS model instance
    """
    # Load chunks
    chunks = load_chunks_from_json(json_path)
    if not chunks:
        print("❌ No chunks loaded from JSON file")
        return
    
    # Create processor
    processor = SmartBatchProcessor(model, tolerance=0.05, min_batch_size=2, max_batch_size=6)
    
    # Analyze batching potential
    analysis = processor.analyze_chunk_distribution(chunks)
    
    print("🔍 SMART BATCHING ANALYSIS")
    print("=" * 40)
    print(f"Total chunks: {analysis['total_chunks']}")
    print(f"Unique parameter combinations: {analysis['unique_combinations']}")
    print(f"Exact batchable: {analysis['exact_batchable']} ({analysis['exact_batch_percentage']:.1f}%)")
    print(f"Tolerant batchable: {analysis['tolerant_batchable']} ({analysis['tolerant_batch_percentage']:.1f}%)")
    print(f"Estimated speedup: {analysis['estimated_speedup']['tolerant_speedup']:.2f}x")
    print()
    
    # Process first few chunks as demo
    demo_chunks = chunks[:10]  # Process first 10 chunks for demo
    print(f"🚀 Processing {len(demo_chunks)} demo chunks...")
    
    # Process with smart batching
    results = processor.process_chunks_with_smart_batching(demo_chunks, use_tolerance=True)
    
    print(f"✅ Smart batching completed!")
    print(f"Generated {len([r for r in results if r is not None])} audio files")
    
    return results