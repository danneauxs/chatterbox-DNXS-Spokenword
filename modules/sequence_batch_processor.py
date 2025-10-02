#!/usr/bin/env python3
"""
True Sequence-Level Batch Processor
==================================

This module implements proper sequence-level batching using the existing
generate_batch() method in ChatterboxTTS to maintain 87% GPU utilization
and achieve the target 20% speed increase.

The key insight from CUDA profiling: GPU utilization spikes to 87% during
inference but drops to 0-1% between chunks. True batching maintains that
87% utilization by processing multiple texts simultaneously.
"""

import time
import logging
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import torch

logger = logging.getLogger(__name__)


class SequenceBatchProcessor:
    """
    True sequence-level batch processor that uses ChatterboxTTS.generate_batch()
    to maintain consistent GPU utilization and achieve 20% speed increase.
    """

    def __init__(self, model, batch_size: int = 4, parameter_tolerance: float = 0.05):
        """
        Initialize sequence batch processor

        Args:
            model: ChatterboxTTS model instance
            batch_size: Number of texts to process simultaneously
            parameter_tolerance: Tolerance for parameter grouping (0.05 = 5%)
        """
        self.model = model
        self.batch_size = batch_size
        self.parameter_tolerance = parameter_tolerance
        self.logger = logging.getLogger(__name__)

        # Performance tracking
        self.stats = {
            'total_chunks': 0,
            'batched_chunks': 0,
            'individual_chunks': 0,
            'batch_groups': 0,
            'total_time': 0,
            'avg_gpu_utilization': 0,
            'parameter_groups': 0
        }

    def analyze_batching_potential(self, chunks: List[Dict]) -> Dict:
        """
        Analyze the batching potential of a chunk list

        Args:
            chunks: List of chunk dictionaries with text and tts_params

        Returns:
            Analysis results with batching recommendations
        """
        if not chunks:
            return {'error': 'No chunks provided'}

        # Group by similar parameters
        param_groups = self._group_by_parameters(chunks)

        total_chunks = len(chunks)
        batchable_chunks = sum(len(group) for group in param_groups if len(group) >= 2)
        max_batch_efficiency = sum(
            (len(group) // self.batch_size) * self.batch_size
            for group in param_groups
            if len(group) >= self.batch_size
        )

        # Calculate expected speedup
        # Assume: individual = 100 it/s, batch = 87% GPU util sustained = ~150 it/s equivalent
        individual_time = total_chunks  # Normalized time units
        batch_time = (
            max_batch_efficiency / self.batch_size +  # Full batches
            (total_chunks - max_batch_efficiency)     # Remaining individual
        )
        expected_speedup = individual_time / batch_time if batch_time > 0 else 1.0

        analysis = {
            'total_chunks': total_chunks,
            'parameter_groups': len(param_groups),
            'batchable_chunks': batchable_chunks,
            'batch_efficiency': (batchable_chunks / total_chunks) * 100,
            'max_batch_utilization': max_batch_efficiency,
            'expected_speedup': expected_speedup,
            'target_achieved': expected_speedup >= 1.2,  # 20% increase
            'recommendations': self._generate_recommendations(param_groups, total_chunks)
        }

        return analysis

    def _group_by_parameters(self, chunks: List[Dict]) -> List[List[Tuple[int, Dict]]]:
        """Group chunks by similar TTS parameters for batching"""
        param_groups = defaultdict(list)

        for i, chunk in enumerate(chunks):
            # Extract parameters with tolerance rounding
            params = chunk.get('tts_params', {})
            signature = self._create_parameter_signature(params)
            param_groups[signature].append((i, chunk))

        # Convert to list and sort by group size (largest first)
        groups = list(param_groups.values())
        groups.sort(key=len, reverse=True)

        return groups

    def _create_parameter_signature(self, params: Dict) -> Tuple:
        """Create a parameter signature for grouping with tolerance"""
        tolerance = self.parameter_tolerance

        return (
            round(params.get('exaggeration', 0.5) / tolerance) * tolerance,
            round(params.get('cfg_weight', 0.5) / tolerance) * tolerance,
            round(params.get('temperature', 0.8) / tolerance) * tolerance,
            round(params.get('min_p', 0.05) / tolerance) * tolerance,
            round(params.get('repetition_penalty', 1.2) / tolerance) * tolerance
        )

    def _generate_recommendations(self, param_groups: List, total_chunks: int) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        large_groups = [g for g in param_groups if len(g) >= self.batch_size]
        if large_groups:
            total_batchable = sum(len(g) for g in large_groups)
            recommendations.append(
                f"✅ EXCELLENT BATCHING: {len(large_groups)} groups with {total_batchable} chunks "
                f"can use full batch processing"
            )
        else:
            recommendations.append(
                "⚠️ LIMITED BATCHING: No parameter groups large enough for optimal batch sizes"
            )

        medium_groups = [g for g in param_groups if 2 <= len(g) < self.batch_size]
        if medium_groups:
            recommendations.append(
                f"🔧 PARTIAL BATCHING: {len(medium_groups)} groups can use smaller batch sizes"
            )

        singleton_groups = [g for g in param_groups if len(g) == 1]
        if len(singleton_groups) > total_chunks * 0.5:
            recommendations.append(
                "❌ HIGH PARAMETER VARIANCE: Consider parameter consolidation or "
                "increasing tolerance for better batching"
            )

        return recommendations

    def process_chunks_with_sequence_batching(self, chunks: List[Dict]) -> List[torch.Tensor]:
        """
        Process chunks using true sequence-level batching

        Args:
            chunks: List of chunk dictionaries

        Returns:
            List of audio tensors in original order
        """
        if not chunks:
            return []

        start_time = time.time()
        self.stats['total_chunks'] = len(chunks)

        # Group chunks by parameters
        param_groups = self._group_by_parameters(chunks)
        self.stats['parameter_groups'] = len(param_groups)

        # Initialize results array
        results = [None] * len(chunks)

        # Process each parameter group
        for group_idx, group in enumerate(param_groups):
            self.logger.info(f"🔥 Processing parameter group {group_idx + 1}/{len(param_groups)} "
                           f"with {len(group)} chunks")

            # Extract parameters from first chunk in group
            _, first_chunk = group[0]
            group_params = first_chunk.get('tts_params', {})

            # Process this group in batches
            self._process_parameter_group(group, group_params, results)

        self.stats['total_time'] = time.time() - start_time
        self._log_performance_summary()

        return results

    def _process_parameter_group(self, group: List[Tuple[int, Dict]],
                                params: Dict, results: List) -> None:
        """Process a single parameter group using optimal batching"""

        group_size = len(group)
        batches_processed = 0

        # Process in batches of batch_size
        for i in range(0, group_size, self.batch_size):
            batch = group[i:i + self.batch_size]

            if len(batch) == 1:
                # Process single chunk individually
                self._process_individual_chunk(batch[0], params, results)
                self.stats['individual_chunks'] += 1
            else:
                # Process as true batch
                self._process_chunk_batch(batch, params, results)
                self.stats['batched_chunks'] += len(batch)
                batches_processed += 1

        self.stats['batch_groups'] += batches_processed

    def _process_chunk_batch(self, batch: List[Tuple[int, Dict]],
                           params: Dict, results: List) -> None:
        """Process a batch of chunks using generate_batch()"""
        try:
            # Extract texts and indices
            texts = [chunk['text'] for _, chunk in batch]
            indices = [idx for idx, _ in batch]

            self.logger.info(f"   🚀 Batch processing {len(texts)} texts simultaneously")

            # Use the actual generate_batch method - THIS IS THE KEY!
            batch_start = time.time()
            audio_batch = self.model.generate_batch(
                texts=texts,
                exaggeration=params.get('exaggeration', 0.5),
                cfg_weight=params.get('cfg_weight', 0.5),
                temperature=params.get('temperature', 0.8),
                min_p=params.get('min_p', 0.05),
                top_p=params.get('top_p', 1.0),
                repetition_penalty=params.get('repetition_penalty', 1.2)
            )
            batch_time = time.time() - batch_start

            # Store results in correct positions
            for idx, audio in zip(indices, audio_batch):
                results[idx] = audio

            it_per_sec = len(texts) / batch_time if batch_time > 0 else 0
            self.logger.info(f"   ✅ Batch completed: {len(texts)} chunks in {batch_time:.2f}s "
                           f"({it_per_sec:.1f} it/s)")

        except Exception as e:
            self.logger.error(f"❌ Batch processing failed: {e}")
            # Fallback to individual processing
            for idx_chunk in batch:
                self._process_individual_chunk(idx_chunk, params, results)

    def _process_individual_chunk(self, idx_chunk: Tuple[int, Dict],
                                params: Dict, results: List) -> None:
        """Process a single chunk individually"""
        idx, chunk = idx_chunk

        try:
            self.logger.info(f"   🔧 Individual processing chunk {idx}")

            chunk_start = time.time()
            audio = self.model.generate(
                chunk['text'],
                exaggeration=params.get('exaggeration', 0.5),
                cfg_weight=params.get('cfg_weight', 0.5),
                temperature=params.get('temperature', 0.8),
                min_p=params.get('min_p', 0.05),
                top_p=params.get('top_p', 1.0),
                repetition_penalty=params.get('repetition_penalty', 1.2)
            )
            chunk_time = time.time() - chunk_start

            results[idx] = audio
            self.logger.info(f"   ✅ Individual chunk completed in {chunk_time:.2f}s")

        except Exception as e:
            self.logger.error(f"❌ Individual chunk {idx} failed: {e}")
            # Create silent audio as fallback
            results[idx] = torch.zeros(1, 24000)

    def _log_performance_summary(self) -> None:
        """Log comprehensive performance summary"""
        stats = self.stats

        self.logger.info("📊 SEQUENCE BATCH PROCESSING SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Total chunks processed: {stats['total_chunks']}")
        self.logger.info(f"Parameter groups: {stats['parameter_groups']}")
        self.logger.info(f"Batched chunks: {stats['batched_chunks']} "
                        f"({stats['batched_chunks']/stats['total_chunks']*100:.1f}%)")
        self.logger.info(f"Individual chunks: {stats['individual_chunks']} "
                        f"({stats['individual_chunks']/stats['total_chunks']*100:.1f}%)")
        self.logger.info(f"Batch groups processed: {stats['batch_groups']}")
        self.logger.info(f"Total processing time: {stats['total_time']:.2f}s")

        # Calculate performance metrics
        if stats['total_chunks'] > 0 and stats['total_time'] > 0:
            chunks_per_second = stats['total_chunks'] / stats['total_time']
            estimated_baseline = 102  # it/s from CUDA profiling baseline
            speedup = chunks_per_second / estimated_baseline

            self.logger.info(f"Processing rate: {chunks_per_second:.1f} chunks/s")
            self.logger.info(f"Estimated speedup: {speedup:.2f}x")

            if speedup >= 1.2:
                self.logger.info("🎯 TARGET ACHIEVED: 20%+ speed increase!")
            else:
                self.logger.info(f"📈 Progress: {(speedup - 1.0) * 100:.1f}% improvement")

        self.logger.info("=" * 60)


def create_sequence_batch_processor(model, batch_size: int = 4) -> SequenceBatchProcessor:
    """
    Factory function to create optimized sequence batch processor

    Args:
        model: ChatterboxTTS model instance
        batch_size: Optimal batch size based on GPU memory and target workload

    Returns:
        Configured SequenceBatchProcessor
    """
    processor = SequenceBatchProcessor(model, batch_size=batch_size)

    logger.info(f"🚀 Sequence Batch Processor created:")
    logger.info(f"   Batch size: {batch_size}")
    logger.info(f"   Target: 20% speed increase (100-105 → 120-126 it/s)")
    logger.info(f"   Strategy: Maintain 87% GPU utilization through true batching")

    return processor