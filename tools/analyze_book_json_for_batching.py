#!/usr/bin/env python3
"""
Book JSON Batching Analyzer
===========================

Analyzes book JSON files to identify optimal batching groups based on TTS parameters.
Creates batching strategy for Flash Attention optimization.

Usage:
    cd /home/danno/MyApps/chatterbox (copy)
    venv/bin/python tools/analyze_book_json_for_batching.py <json_file_path>
"""

import sys
import json
import time
from pathlib import Path
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch


@dataclass
class ChunkInfo:
    """Information about a single text chunk"""
    chunk_id: str
    text: str
    tts_params: Dict[str, Any]
    word_count: int
    token_estimate: int
    is_paragraph_end: bool = False
    vader_sentiment: Dict[str, float] = None


@dataclass
class BatchGroup:
    """Group of chunks with identical TTS parameters"""
    tts_params: Dict[str, Any]
    chunks: List[ChunkInfo]
    total_tokens: int
    avg_tokens_per_chunk: int
    batch_benefit_score: float


def parse_book_json(json_file_path: Path) -> List[ChunkInfo]:
    """Parse book JSON file and extract chunk information"""
    print(f"📖 Parsing book JSON: {json_file_path}")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return []

    chunks = []

    # Handle different JSON structures
    if isinstance(book_data, list):
        # Direct list of chunks
        chunk_list = book_data
    elif isinstance(book_data, dict):
        # Look for common chunk container keys
        if 'chunks' in book_data:
            chunk_list = book_data['chunks']
        elif 'enriched_chunks' in book_data:
            chunk_list = book_data['enriched_chunks']
        elif 'data' in book_data:
            chunk_list = book_data['data']
        else:
            # Try to find the main data array
            for key, value in book_data.items():
                if isinstance(value, list) and value:
                    chunk_list = value
                    break
            else:
                print(f"❌ Could not find chunk data in JSON structure")
                return []
    else:
        print(f"❌ Unexpected JSON structure type: {type(book_data)}")
        return []

    print(f"📊 Found {len(chunk_list)} chunks in JSON")

    for i, chunk_data in enumerate(chunk_list):
        try:
            # Extract text content
            if isinstance(chunk_data, str):
                # Simple string chunks
                text = chunk_data
                chunk_id = f"chunk_{i:05d}"
                tts_params = {}  # Default params
                vader_sentiment = None
            elif isinstance(chunk_data, dict):
                # Structured chunk data
                # Try different text field names
                text = (chunk_data.get('text') or
                       chunk_data.get('content') or
                       chunk_data.get('chunk_text') or
                       chunk_data.get('sentence', ''))

                chunk_id = (chunk_data.get('chunk_id') or
                           chunk_data.get('id') or
                           f"chunk_{i:05d}")

                # Extract TTS parameters
                tts_params = {}
                for param in ['temperature', 'cfg_weight', 'repetition_penalty',
                             'top_p', 'min_p', 'length_penalty', 'max_new_tokens']:
                    if param in chunk_data:
                        tts_params[param] = chunk_data[param]
                    elif 'tts_params' in chunk_data and param in chunk_data['tts_params']:
                        tts_params[param] = chunk_data['tts_params'][param]

                # Extract VADER sentiment if available
                vader_sentiment = chunk_data.get('vader_sentiment') or chunk_data.get('sentiment')

                # Look for paragraph end markers
                is_paragraph_end = chunk_data.get('is_paragraph_end', False)
            else:
                print(f"⚠️ Skipping unexpected chunk type at index {i}: {type(chunk_data)}")
                continue

            if not text.strip():
                continue

            # Calculate word count and token estimate
            word_count = len(text.split())
            token_estimate = int(word_count * 1.3)  # Rough token estimate

            chunk_info = ChunkInfo(
                chunk_id=str(chunk_id),
                text=text.strip(),
                tts_params=tts_params,
                word_count=word_count,
                token_estimate=token_estimate,
                is_paragraph_end=is_paragraph_end,
                vader_sentiment=vader_sentiment
            )

            chunks.append(chunk_info)

        except Exception as e:
            print(f"⚠️ Error processing chunk {i}: {e}")
            continue

    print(f"✅ Successfully parsed {len(chunks)} chunks")
    return chunks


def group_chunks_by_tts_params(chunks: List[ChunkInfo]) -> Dict[str, BatchGroup]:
    """Group chunks by identical TTS parameters"""
    print(f"\n🔧 Grouping chunks by TTS parameters...")

    # Group chunks by TTS parameter signature
    param_groups = defaultdict(list)

    for chunk in chunks:
        # Create a hashable signature of TTS parameters
        param_signature = tuple(sorted(chunk.tts_params.items()))
        param_groups[param_signature].append(chunk)

    # Convert to BatchGroup objects
    batch_groups = {}
    for param_signature, chunk_list in param_groups.items():
        tts_params = dict(param_signature)
        total_tokens = sum(chunk.token_estimate for chunk in chunk_list)
        avg_tokens = total_tokens // len(chunk_list) if chunk_list else 0

        # Calculate batch benefit score
        batch_benefit_score = calculate_batch_benefit(chunk_list, total_tokens)

        group_key = f"group_{len(batch_groups):03d}"
        batch_groups[group_key] = BatchGroup(
            tts_params=tts_params,
            chunks=chunk_list,
            total_tokens=total_tokens,
            avg_tokens_per_chunk=avg_tokens,
            batch_benefit_score=batch_benefit_score
        )

    print(f"📊 Created {len(batch_groups)} parameter groups")
    return batch_groups


def calculate_batch_benefit(chunks: List[ChunkInfo], total_tokens: int) -> float:
    """Calculate potential benefit score for batching this group"""
    chunk_count = len(chunks)
    avg_tokens = total_tokens / chunk_count if chunk_count > 0 else 0

    # Benefit factors:
    # 1. Number of chunks (more chunks = more kernel launch savings)
    # 2. Total sequence length (longer = better Flash Attention benefit)
    # 3. Batch efficiency (fewer very short chunks)

    chunk_factor = min(chunk_count / 10.0, 1.0)  # Normalize to 0-1, cap at 10 chunks
    length_factor = min(total_tokens / 500.0, 1.0)  # Normalize to 0-1, cap at 500 tokens
    efficiency_factor = min(avg_tokens / 30.0, 1.0)  # Normalize to 0-1, cap at 30 tokens/chunk

    # Weighted combination
    benefit_score = (chunk_factor * 0.4 + length_factor * 0.4 + efficiency_factor * 0.2)

    return benefit_score


def analyze_batching_potential(batch_groups: Dict[str, BatchGroup]) -> Dict[str, Any]:
    """Analyze the overall batching potential"""
    print(f"\n📈 Analyzing batching potential...")

    total_chunks = sum(len(group.chunks) for group in batch_groups.values())
    total_groups = len(batch_groups)

    # Sort groups by benefit score
    sorted_groups = sorted(batch_groups.values(), key=lambda g: g.batch_benefit_score, reverse=True)

    # Categorize groups
    high_benefit_groups = [g for g in sorted_groups if g.batch_benefit_score >= 0.7]
    medium_benefit_groups = [g for g in sorted_groups if 0.3 <= g.batch_benefit_score < 0.7]
    low_benefit_groups = [g for g in sorted_groups if g.batch_benefit_score < 0.3]

    # Calculate statistics
    batchable_chunks = sum(len(g.chunks) for g in high_benefit_groups + medium_benefit_groups)
    sequential_chunks = sum(len(g.chunks) for g in low_benefit_groups)

    # Group size distribution
    group_sizes = [len(group.chunks) for group in batch_groups.values()]
    size_distribution = Counter(group_sizes)

    analysis = {
        'total_chunks': total_chunks,
        'total_groups': total_groups,
        'high_benefit_groups': len(high_benefit_groups),
        'medium_benefit_groups': len(medium_benefit_groups),
        'low_benefit_groups': len(low_benefit_groups),
        'batchable_chunks': batchable_chunks,
        'sequential_chunks': sequential_chunks,
        'batch_efficiency': batchable_chunks / total_chunks if total_chunks > 0 else 0,
        'avg_group_size': sum(group_sizes) / len(group_sizes) if group_sizes else 0,
        'max_group_size': max(group_sizes) if group_sizes else 0,
        'size_distribution': dict(size_distribution),
        'top_groups': sorted_groups[:10]  # Top 10 groups by benefit
    }

    return analysis


def print_analysis_report(analysis: Dict[str, Any], batch_groups: Dict[str, BatchGroup]):
    """Print detailed analysis report"""
    print(f"\n" + "="*70)
    print(f"BATCHING ANALYSIS REPORT")
    print(f"="*70)

    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total chunks: {analysis['total_chunks']}")
    print(f"   Parameter groups: {analysis['total_groups']}")
    print(f"   Average group size: {analysis['avg_group_size']:.1f} chunks")
    print(f"   Largest group: {analysis['max_group_size']} chunks")

    print(f"\n🎯 BATCHING POTENTIAL:")
    print(f"   High benefit groups: {analysis['high_benefit_groups']} ({analysis['high_benefit_groups']/analysis['total_groups']*100:.1f}%)")
    print(f"   Medium benefit groups: {analysis['medium_benefit_groups']} ({analysis['medium_benefit_groups']/analysis['total_groups']*100:.1f}%)")
    print(f"   Low benefit groups: {analysis['low_benefit_groups']} ({analysis['low_benefit_groups']/analysis['total_groups']*100:.1f}%)")

    print(f"\n⚡ OPTIMIZATION IMPACT:")
    print(f"   Batchable chunks: {analysis['batchable_chunks']} ({analysis['batch_efficiency']*100:.1f}%)")
    print(f"   Sequential chunks: {analysis['sequential_chunks']} ({(1-analysis['batch_efficiency'])*100:.1f}%)")

    if analysis['batch_efficiency'] >= 0.7:
        print(f"   🚀 EXCELLENT batching potential - major speedup expected!")
    elif analysis['batch_efficiency'] >= 0.4:
        print(f"   ⚡ GOOD batching potential - significant speedup expected")
    else:
        print(f"   📈 MODERATE batching potential - some speedup expected")

    print(f"\n🔍 GROUP SIZE DISTRIBUTION:")
    for size, count in sorted(analysis['size_distribution'].items()):
        percentage = count / analysis['total_groups'] * 100
        print(f"   {size} chunks/group: {count} groups ({percentage:.1f}%)")

    print(f"\n🏆 TOP 5 BATCHING CANDIDATES:")
    for i, group in enumerate(analysis['top_groups'][:5], 1):
        tokens_per_chunk = group.total_tokens / len(group.chunks)
        print(f"   {i}. {len(group.chunks)} chunks, {group.total_tokens} tokens ({tokens_per_chunk:.1f} tok/chunk)")
        print(f"      Benefit score: {group.batch_benefit_score:.2f}")
        print(f"      TTS params: {group.tts_params}")
        print()


def create_batching_plan(batch_groups: Dict[str, BatchGroup], analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Create concrete batching implementation plan"""
    print(f"\n🔧 CREATING BATCHING IMPLEMENTATION PLAN:")

    # Define batching thresholds
    MIN_BATCH_SIZE = 2  # Minimum chunks to justify batching
    MAX_BATCH_SIZE = 16  # Maximum chunks per batch (memory constraint)
    MIN_BATCH_TOKENS = 60  # Minimum tokens to benefit from Flash Attention

    batching_plan = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'thresholds': {
            'min_batch_size': MIN_BATCH_SIZE,
            'max_batch_size': MAX_BATCH_SIZE,
            'min_batch_tokens': MIN_BATCH_TOKENS
        },
        'batch_groups': [],
        'sequential_groups': [],
        'expected_benefits': {}
    }

    total_batched_chunks = 0
    total_sequential_chunks = 0
    total_kernel_launch_savings = 0

    for group_id, group in batch_groups.items():
        group_size = len(group.chunks)

        # Determine if group should be batched
        should_batch = (
            group_size >= MIN_BATCH_SIZE and
            group.total_tokens >= MIN_BATCH_TOKENS and
            group.batch_benefit_score >= 0.3
        )

        if should_batch:
            # Split large groups into multiple batches
            batches = []
            chunks_remaining = group.chunks.copy()

            while chunks_remaining:
                batch_size = min(MAX_BATCH_SIZE, len(chunks_remaining))
                batch_chunks = chunks_remaining[:batch_size]
                chunks_remaining = chunks_remaining[batch_size:]

                batch_tokens = sum(chunk.token_estimate for chunk in batch_chunks)

                batches.append({
                    'batch_id': f"{group_id}_batch_{len(batches)}",
                    'chunks': [chunk.chunk_id for chunk in batch_chunks],
                    'chunk_count': len(batch_chunks),
                    'total_tokens': batch_tokens,
                    'tts_params': group.tts_params,
                    'expected_flash_benefit': batch_tokens >= 128
                })

                total_batched_chunks += len(batch_chunks)
                total_kernel_launch_savings += len(batch_chunks) - 1  # N chunks -> 1 call = N-1 savings

            batching_plan['batch_groups'].append({
                'group_id': group_id,
                'batches': batches,
                'original_chunk_count': group_size,
                'batch_count': len(batches)
            })
        else:
            # Process sequentially
            batching_plan['sequential_groups'].append({
                'group_id': group_id,
                'chunks': [chunk.chunk_id for chunk in group.chunks],
                'chunk_count': group_size,
                'reason': 'too_small' if group_size < MIN_BATCH_SIZE else 'low_benefit'
            })
            total_sequential_chunks += group_size

    # Calculate expected benefits
    total_chunks = total_batched_chunks + total_sequential_chunks
    batch_efficiency = total_batched_chunks / total_chunks if total_chunks > 0 else 0

    batching_plan['expected_benefits'] = {
        'total_chunks': total_chunks,
        'batched_chunks': total_batched_chunks,
        'sequential_chunks': total_sequential_chunks,
        'batch_efficiency': batch_efficiency,
        'kernel_launch_savings': total_kernel_launch_savings,
        'estimated_speedup_percent': min(batch_efficiency * 30, 25)  # Conservative estimate
    }

    print(f"   📊 Batching Plan Created:")
    print(f"      Batched chunks: {total_batched_chunks} ({batch_efficiency*100:.1f}%)")
    print(f"      Sequential chunks: {total_sequential_chunks}")
    print(f"      Kernel launch savings: {total_kernel_launch_savings}")
    print(f"      Estimated speedup: {batching_plan['expected_benefits']['estimated_speedup_percent']:.1f}%")

    return batching_plan


def save_analysis_results(analysis: Dict, batching_plan: Dict, json_file_path: Path):
    """Save analysis results to file"""
    output_file = json_file_path.parent / f"{json_file_path.stem}_batching_analysis.json"

    results = {
        'source_file': str(json_file_path),
        'analysis': analysis,
        'batching_plan': batching_plan
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n📁 Analysis saved to: {output_file}")
    return output_file


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_book_json_for_batching.py <json_file_path>")
        sys.exit(1)

    json_file_path = Path(sys.argv[1])

    if not json_file_path.exists():
        print(f"❌ JSON file not found: {json_file_path}")
        sys.exit(1)

    print("="*70)
    print("BOOK JSON BATCHING ANALYZER")
    print("="*70)

    # Parse book JSON
    chunks = parse_book_json(json_file_path)
    if not chunks:
        print("❌ No chunks found in JSON file")
        sys.exit(1)

    # Group by TTS parameters
    batch_groups = group_chunks_by_tts_params(chunks)

    # Analyze batching potential
    analysis = analyze_batching_potential(batch_groups)

    # Print report
    print_analysis_report(analysis, batch_groups)

    # Create implementation plan
    batching_plan = create_batching_plan(batch_groups, analysis)

    # Save results
    save_analysis_results(analysis, batching_plan, json_file_path)

    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Review batching plan in output file")
    print(f"   2. Implement batched T3 inference")
    print(f"   3. Test with Flash Attention enabled")
    print(f"   4. Benchmark performance improvements")


if __name__ == "__main__":
    main()