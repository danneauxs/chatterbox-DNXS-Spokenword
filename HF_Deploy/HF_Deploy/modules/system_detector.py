"""
System Resource Detection Module
Detects VRAM, RAM, CPU cores and recommends appropriate ASR models
"""

import psutil
import torch
import os
import sys
from pathlib import Path

# Add project root to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import ASR_MODEL_VRAM_MB, ASR_MODEL_RAM_MB

def get_gpu_memory():
    """Get total and available GPU memory in MB"""
    try:
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            if gpu_count > 0:
                # Use first GPU
                total_vram = torch.cuda.get_device_properties(0).total_memory
                allocated_vram = torch.cuda.memory_allocated(0)
                available_vram = total_vram - allocated_vram
                
                return {
                    'total_mb': total_vram // 1024 // 1024,
                    'available_mb': available_vram // 1024 // 1024,
                    'allocated_mb': allocated_vram // 1024 // 1024
                }
    except:
        pass
    
    return {'total_mb': 0, 'available_mb': 0, 'allocated_mb': 0}

def get_system_memory():
    """Get total and available system RAM in MB"""
    try:
        memory = psutil.virtual_memory()
        return {
            'total_mb': memory.total // 1024 // 1024,
            'available_mb': memory.available // 1024 // 1024,
            'used_mb': memory.used // 1024 // 1024
        }
    except:
        return {'total_mb': 0, 'available_mb': 0, 'used_mb': 0}

def get_cpu_cores():
    """Get number of CPU cores"""
    try:
        return psutil.cpu_count(logical=False) or psutil.cpu_count()
    except:
        return 1

def estimate_tts_vram_usage():
    """Estimate VRAM usage by ChatterboxTTS (updated based on real usage)"""
    return 5500  # 5.5GB in MB (was 7GB, adjusted based on actual 3.5GB usage + buffer)

def get_system_profile():
    """Get complete system resource profile"""
    gpu_info = get_gpu_memory()
    ram_info = get_system_memory()
    cpu_cores = get_cpu_cores()
    
    # Estimate available resources after TTS loading
    tts_vram_estimate = estimate_tts_vram_usage()
    available_vram_after_tts = max(0, gpu_info['available_mb'] - tts_vram_estimate)
    
    return {
        'gpu': gpu_info,
        'ram': ram_info,
        'cpu_cores': cpu_cores,
        'available_vram_after_tts': available_vram_after_tts,
        'has_gpu': gpu_info['total_mb'] > 0
    }

def categorize_system(profile):
    """Categorize system capabilities"""
    gpu_total = profile['gpu']['total_mb']
    ram_total = profile['ram']['total_mb']
    cpu_cores = profile['cpu_cores']
    
    # VRAM categories
    if gpu_total < 4000:
        vram_category = "low"
    elif gpu_total <= 12000:
        vram_category = "medium"
    else:
        vram_category = "high"
    
    # RAM categories  
    if ram_total < 16000:
        ram_category = "low"
    elif ram_total <= 64000:
        ram_category = "medium"
    else:
        ram_category = "high"
    
    # CPU categories
    if cpu_cores < 6:
        cpu_category = "low"
    elif cpu_cores <= 16:
        cpu_category = "medium"
    else:
        cpu_category = "high"
    
    return {
        'vram': vram_category,
        'ram': ram_category,
        'cpu': cpu_category
    }

def get_safe_asr_models(profile):
    """Get ASR models that can safely run on GPU with available VRAM"""
    available_vram = profile['available_vram_after_tts']
    safe_models = []
    
    for model, vram_req in ASR_MODEL_VRAM_MB.items():
        if vram_req <= available_vram:
            safe_models.append(model)
    
    return safe_models

def get_safe_cpu_models(profile):
    """Get ASR models that can safely run on CPU with available RAM"""
    available_ram = profile['ram']['available_mb']
    safe_models = []
    
    for model, ram_req in ASR_MODEL_RAM_MB.items():
        if ram_req <= available_ram:
            safe_models.append(model)
    
    return safe_models

def recommend_asr_models(profile):
    """Recommend Safe/Moderate/Insane ASR model configurations"""
    categories = categorize_system(profile)
    safe_gpu_models = get_safe_asr_models(profile)
    safe_cpu_models = get_safe_cpu_models(profile)
    
    recommendations = {}
    
    # Model priority order (best to worst)
    model_priority = ["large-v3", "large", "large-v2", "medium", "small", "base", "tiny"]
    
    # Safe: Conservative choice
    safe_gpu = None
    safe_cpu = None
    
    for model in reversed(model_priority):  # Start from smallest
        if model in safe_gpu_models and not safe_gpu:
            safe_gpu = model
        if model in safe_cpu_models and not safe_cpu:
            safe_cpu = model
        if safe_gpu and safe_cpu:
            break
    
    # Moderate: Balanced choice  
    moderate_gpu = None
    moderate_cpu = None
    
    # Try to get a model 1-2 steps up from safe
    safe_idx = model_priority.index(safe_gpu) if safe_gpu else len(model_priority)
    moderate_idx = max(0, safe_idx - 2)
    
    for i in range(moderate_idx, len(model_priority)):
        model = model_priority[i]
        if model in safe_gpu_models and not moderate_gpu:
            moderate_gpu = model
        if model in safe_cpu_models and not moderate_cpu:
            moderate_cpu = model
        if moderate_gpu and moderate_cpu:
            break
    
    # Insane: Push the limits (best available models)
    insane_gpu = None
    insane_cpu = None
    
    # Get the best (largest) models that are safe
    for model in model_priority:  # Start from best
        if model in safe_gpu_models and not insane_gpu:
            insane_gpu = model
        if model in safe_cpu_models and not insane_cpu:
            insane_cpu = model
        if insane_gpu and insane_cpu:
            break
    
    # Build recommendations
    recommendations['safe'] = {
        'primary': {'model': safe_gpu or safe_cpu, 'device': 'gpu' if safe_gpu else 'cpu'},
        'fallback': {'model': safe_cpu, 'device': 'cpu'}
    }
    
    recommendations['moderate'] = {
        'primary': {'model': moderate_gpu or moderate_cpu, 'device': 'gpu' if moderate_gpu else 'cpu'},
        'fallback': {'model': moderate_cpu, 'device': 'cpu'}
    }
    
    recommendations['insane'] = {
        'primary': {'model': insane_gpu or insane_cpu, 'device': 'gpu' if insane_gpu else 'cpu'},
        'fallback': {'model': insane_cpu, 'device': 'cpu'}
    }
    
    return recommendations

def print_system_summary(profile):
    """Print a human-readable system summary"""
    categories = categorize_system(profile)
    
    print(f"🖥️ System Profile:")
    print(f"   VRAM: {profile['gpu']['total_mb']:,}MB total, {profile['available_vram_after_tts']:,}MB available after TTS ({categories['vram']} class)")
    print(f"   RAM:  {profile['ram']['total_mb']:,}MB total, {profile['ram']['available_mb']:,}MB available ({categories['ram']} class)")
    print(f"   CPU:  {profile['cpu_cores']} cores ({categories['cpu']} class)")
    
    if not profile['has_gpu']:
        print(f"   ⚠️ No CUDA GPU detected - ASR will run on CPU only")

if __name__ == "__main__":
    # Test the detection
    profile = get_system_profile()
    print_system_summary(profile)
    
    recommendations = recommend_asr_models(profile)
    print(f"\nASR Model Recommendations:")
    for level, config in recommendations.items():
        primary = config['primary']
        fallback = config['fallback']
        print(f"🟢 {level.upper()}: {primary['model']} ({primary['device']}) + {fallback['model']} (cpu fallback)")