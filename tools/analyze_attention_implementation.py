#!/usr/bin/env python3
"""
Attention Implementation Analyzer
================================

Analyzes the current attention implementation in T3 and tests
Flash Attention optimization for Phase 1 of forward pass optimization.

Current State: T3 uses LlamaModel with "eager" attention
Optimization Target: Enable Flash Attention 2 for 30-50% attention speedup

Usage:
    cd /home/danno/MyApps/chatterbox (copy)
    venv/bin/python tools/analyze_attention_implementation.py
"""

import sys
import time
import os
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import gc

# Import required modules
from modules.tts_engine import load_optimized_model, prewarm_model_with_voice


def check_flash_attention_availability():
    """Check if Flash Attention is available"""
    print("🔍 CHECKING FLASH ATTENTION AVAILABILITY:")
    print("=" * 50)

    try:
        import flash_attn
        flash_version = flash_attn.__version__
        print(f"✅ Flash Attention installed: v{flash_version}")
        has_flash_attn = True
    except ImportError:
        print("❌ Flash Attention not installed")
        has_flash_attn = False

    # Check transformers version
    try:
        import transformers
        transformers_version = transformers.__version__
        print(f"✅ Transformers version: {transformers_version}")

        # Check if transformers supports flash_attention_2
        major, minor = transformers_version.split('.')[:2]
        if int(major) >= 4 and int(minor) >= 30:
            print("✅ Transformers supports flash_attention_2")
            transformers_supports = True
        else:
            print("⚠️ Transformers version may not support flash_attention_2")
            transformers_supports = False
    except Exception as e:
        print(f"❌ Error checking transformers: {e}")
        transformers_supports = False

    # Check PyTorch version
    torch_version = torch.__version__
    print(f"✅ PyTorch version: {torch_version}")

    return {
        'has_flash_attn': has_flash_attn,
        'transformers_supports': transformers_supports,
        'flash_version': flash_version if has_flash_attn else None,
        'transformers_version': transformers_version,
        'torch_version': torch_version
    }


def analyze_current_attention_config(model):
    """Analyze the current attention configuration in T3"""
    print("\n🔍 CURRENT T3 ATTENTION CONFIGURATION:")
    print("=" * 50)

    t3_model = model.t3
    config = t3_model.cfg

    print(f"Model type: {type(t3_model.tfmr)}")
    print(f"Config type: {type(config)}")

    # Check attention implementation
    if hasattr(config, 'attn_implementation'):
        current_attn = config.attn_implementation
        print(f"Current attention implementation: {current_attn}")
    else:
        print("Attention implementation not specified")
        current_attn = "default"

    # Check model architecture details
    print(f"Hidden size: {config.hidden_size}")
    print(f"Number of attention heads: {config.num_attention_heads}")
    print(f"Number of layers: {config.num_hidden_layers}")

    if hasattr(config, 'num_key_value_heads'):
        print(f"Number of KV heads: {config.num_key_value_heads}")

    # Check if model is using grouped query attention
    if hasattr(config, 'num_key_value_heads') and config.num_key_value_heads < config.num_attention_heads:
        print("✅ Using Grouped Query Attention (GQA)")
        gqa_ratio = config.num_attention_heads / config.num_key_value_heads
        print(f"   GQA ratio: {gqa_ratio:.1f}:1")
    else:
        print("❌ Not using Grouped Query Attention")

    return {
        'current_implementation': current_attn,
        'hidden_size': config.hidden_size,
        'num_attention_heads': config.num_attention_heads,
        'num_layers': config.num_hidden_layers,
        'num_kv_heads': getattr(config, 'num_key_value_heads', config.num_attention_heads),
        'using_gqa': hasattr(config, 'num_key_value_heads') and config.num_key_value_heads < config.num_attention_heads
    }


def benchmark_attention_implementations(model, voice_path, test_text="This is a test sentence for attention benchmarking."):
    """Benchmark different attention implementations"""
    print(f"\n⚡ ATTENTION IMPLEMENTATION BENCHMARK:")
    print("=" * 50)

    # Prepare inputs
    model.prepare_conditionals(voice_path)
    norm_text = test_text.strip()
    text_tokens = model.tokenizer.text_to_tokens(norm_text)

    # Add start/stop tokens
    sot = model.t3.hp.start_text_token
    eot = model.t3.hp.stop_text_token
    text_tokens = torch.cat([
        torch.tensor([[sot]], device=text_tokens.device),
        text_tokens,
        torch.tensor([[eot]], device=text_tokens.device)
    ], dim=1)

    results = {}

    # Test current implementation
    print("Testing current implementation (eager)...")
    start_time = time.time()

    try:
        with torch.inference_mode():
            speech_tokens = model.t3.inference(
                t3_cond=model.conds.t3,
                text_tokens=text_tokens,
                max_new_tokens=50,  # Shorter for benchmark
                temperature=0.8,
                cfg_weight=0.5
            )

        current_time = time.time() - start_time
        results['eager'] = {
            'time': current_time,
            'tokens_generated': speech_tokens.shape[-1] if hasattr(speech_tokens, 'shape') else 0,
            'success': True
        }
        print(f"✅ Eager attention: {current_time:.2f}s")

    except Exception as e:
        print(f"❌ Eager attention failed: {e}")
        results['eager'] = {'success': False, 'error': str(e)}

    # Test Flash Attention 2 if available
    flash_available = False
    try:
        import flash_attn
        flash_available = True
    except ImportError:
        pass

    if flash_available:
        print("Testing Flash Attention 2...")

        # Temporarily modify config
        original_attn = model.t3.cfg.attn_implementation
        try:
            model.t3.cfg.attn_implementation = "flash_attention_2"

            # Need to reload the model for attention change to take effect
            print("⚠️ Flash Attention test requires model reload (skipping for now)")
            results['flash_attention_2'] = {'success': False, 'reason': 'requires_model_reload'}

        except Exception as e:
            print(f"❌ Flash Attention 2 failed: {e}")
            results['flash_attention_2'] = {'success': False, 'error': str(e)}
        finally:
            # Restore original
            model.t3.cfg.attn_implementation = original_attn
    else:
        print("⚠️ Flash Attention not available for testing")
        results['flash_attention_2'] = {'success': False, 'reason': 'not_installed'}

    return results


def create_attention_optimization_plan(availability, config_analysis, benchmark_results):
    """Create optimization plan based on analysis"""
    print(f"\n🎯 ATTENTION OPTIMIZATION PLAN:")
    print("=" * 50)

    plan = []

    # Flash Attention upgrade
    if availability['has_flash_attn'] and availability['transformers_supports']:
        plan.append({
            'optimization': 'Enable Flash Attention 2',
            'expected_speedup': '30-50%',
            'implementation': 'Change attn_implementation from "eager" to "flash_attention_2"',
            'priority': 'HIGH',
            'risk': 'LOW'
        })
        print("🚀 PRIMARY: Enable Flash Attention 2")
        print("   Expected speedup: 30-50%")
        print("   Risk: Low (well-tested)")
    else:
        plan.append({
            'optimization': 'Install Flash Attention',
            'expected_speedup': '30-50%',
            'implementation': 'pip install flash-attn',
            'priority': 'HIGH',
            'risk': 'MEDIUM'
        })
        print("📦 PREREQUISITE: Install Flash Attention")

    # Grouped Query Attention
    if not config_analysis['using_gqa']:
        plan.append({
            'optimization': 'Enable Grouped Query Attention',
            'expected_speedup': '10-20%',
            'implementation': 'Modify config.num_key_value_heads',
            'priority': 'MEDIUM',
            'risk': 'MEDIUM'
        })
        print("🔧 SECONDARY: Enable Grouped Query Attention")
        print("   Expected speedup: 10-20%")
        print("   Risk: Medium (may affect quality)")

    # SDPA optimization
    plan.append({
        'optimization': 'Scaled Dot Product Attention (SDPA)',
        'expected_speedup': '10-30%',
        'implementation': 'Change attn_implementation to "sdpa"',
        'priority': 'MEDIUM',
        'risk': 'LOW'
    })
    print("⚡ ALTERNATIVE: Use PyTorch SDPA")
    print("   Expected speedup: 10-30%")
    print("   Risk: Low (PyTorch built-in)")

    return plan


def main():
    print("=" * 70)
    print("ATTENTION IMPLEMENTATION ANALYZER")
    print("=" * 70)

    # Check CUDA
    if not torch.cuda.is_available():
        print("❌ CUDA not available")
        return

    device_name = torch.cuda.get_device_name()
    print(f"🔍 CUDA Device: {device_name}")

    # Test configuration
    voice_file = "Voice_Samples/Aubrey Parsons 339.wav"
    test_text = "This is a test sentence for attention analysis."

    if not Path(voice_file).exists():
        print(f"❌ Voice file not found: {voice_file}")
        return

    try:
        # Check Flash Attention availability
        availability = check_flash_attention_availability()

        # Load model
        print(f"\n🔥 Loading model...")
        model = load_optimized_model("cuda", force_reload=True)
        model = prewarm_model_with_voice(model, voice_file)
        print("✅ Model loaded and prewarmed")

        # Analyze current configuration
        config_analysis = analyze_current_attention_config(model)

        # Benchmark implementations
        benchmark_results = benchmark_attention_implementations(model, voice_file, test_text)

        # Create optimization plan
        optimization_plan = create_attention_optimization_plan(availability, config_analysis, benchmark_results)

        # Save results
        results = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'device': device_name,
            'voice_file': voice_file,
            'availability': availability,
            'current_config': config_analysis,
            'benchmark_results': benchmark_results,
            'optimization_plan': optimization_plan
        }

        output_file = "attention_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n📁 Analysis saved to {output_file}")

        # Immediate next steps
        print(f"\n🚀 IMMEDIATE NEXT STEPS:")
        print("=" * 50)

        if availability['has_flash_attn']:
            print("1. Test Flash Attention 2 implementation")
            print("2. Benchmark performance improvement")
            print("3. Validate output quality")
        else:
            print("1. Install Flash Attention: pip install flash-attn")
            print("2. Test Flash Attention 2 implementation")
            print("3. Benchmark performance improvement")

        print("4. Consider SDPA as alternative")
        print("5. Evaluate Grouped Query Attention")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()