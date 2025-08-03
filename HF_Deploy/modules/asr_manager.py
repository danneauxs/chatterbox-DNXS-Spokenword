"""
ASR Manager Module
Centralized ASR model loading with adaptive GPU/CPU fallback and real-time VRAM monitoring
"""

import torch
import logging
from pathlib import Path
from config.config import DEFAULT_ASR_MODEL, ASR_MODEL_VRAM_MB, ASR_MODEL_RAM_MB

def get_real_time_vram_status():
    """Get current GPU memory usage in real-time"""
    try:
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            if gpu_count > 0:
                # Use first GPU
                total_vram = torch.cuda.get_device_properties(0).total_memory
                allocated_vram = torch.cuda.memory_allocated(0)
                reserved_vram = torch.cuda.memory_reserved(0)
                available_vram = total_vram - allocated_vram
                
                return {
                    'total_mb': total_vram // 1024 // 1024,
                    'allocated_mb': allocated_vram // 1024 // 1024,
                    'reserved_mb': reserved_vram // 1024 // 1024,
                    'available_mb': available_vram // 1024 // 1024,
                    'has_gpu': True
                }
    except Exception as e:
        logging.warning(f"Failed to get real-time VRAM status: {e}")
    
    return {
        'total_mb': 0,
        'allocated_mb': 0, 
        'reserved_mb': 0,
        'available_mb': 0,
        'has_gpu': False
    }

def calculate_available_vram_for_asr(safety_buffer_mb=500):
    """Calculate VRAM available for ASR with safety buffer"""
    vram_status = get_real_time_vram_status()
    
    if not vram_status['has_gpu']:
        return 0
    
    # Available VRAM minus safety buffer for stability
    available_with_buffer = max(0, vram_status['available_mb'] - safety_buffer_mb)
    
    return available_with_buffer

def can_model_fit_gpu(model_name, available_vram_mb):
    """Check if a specific ASR model can fit in available VRAM"""
    required_vram = ASR_MODEL_VRAM_MB.get(model_name, 0)
    return available_vram_mb >= required_vram

def try_load_model_with_fallback(model_name, primary_device, fallback_device="cpu"):
    """Try to load model on primary device, fallback to secondary if it fails"""
    import whisper
    
    # Convert device names for whisper compatibility
    def convert_device_name(device):
        if device.lower() == "gpu":
            return "cuda"
        return device.lower()
    
    primary_device_whisper = convert_device_name(primary_device)
    fallback_device_whisper = convert_device_name(fallback_device)
    
    try:
        print(f"🎯 Attempting to load {model_name} on {primary_device.upper()}")
        model = whisper.load_model(model_name, device=primary_device_whisper)
        print(f"✅ Successfully loaded {model_name} on {primary_device.upper()}")
        return model, primary_device
        
    except Exception as e:
        print(f"⚠️ {model_name} failed on {primary_device} ({str(e)[:50]}...)")
        
        if fallback_device_whisper != primary_device_whisper:
            try:
                print(f"🔄 Trying {model_name} on {fallback_device.upper()}")
                model = whisper.load_model(model_name, device=fallback_device_whisper)
                print(f"✅ Successfully loaded {model_name} on {fallback_device.upper()}")
                return model, fallback_device
                
            except Exception as fallback_e:
                print(f"❌ {model_name} also failed on {fallback_device} ({str(fallback_e)[:50]}...)")
        
        # Both failed
        raise Exception(f"Model {model_name} failed on both {primary_device} and {fallback_device}")

def load_asr_model_adaptive(asr_config=None):
    """
    Adaptive ASR model loading with real-time VRAM checking and intelligent fallback
    
    Args:
        asr_config: ASR configuration dict from interfaces (None for GUI fallback)
        
    Returns:
        tuple: (asr_model, actual_device_used) or (None, None) if all loading fails
    """
    print(f"🔍 Starting adaptive ASR model loading...")
    
    # Get current VRAM status
    vram_status = get_real_time_vram_status()
    available_vram = calculate_available_vram_for_asr()
    
    print(f"🖥️ Real-time VRAM status:")
    print(f"   Total: {vram_status['total_mb']:,}MB")
    print(f"   Allocated: {vram_status['allocated_mb']:,}MB") 
    print(f"   Available for ASR: {available_vram:,}MB (with 500MB safety buffer)")
    
    # Determine what models to try based on config
    if asr_config and asr_config.get('enabled') and 'primary_model' in asr_config:
        # Intelligent selection from CLI/Gradio
        primary_model = asr_config['primary_model']
        primary_device = asr_config['primary_device']
        fallback_model = asr_config['fallback_model'] 
        fallback_device = asr_config['fallback_device']
        
        print(f"🧠 Using intelligent ASR config:")
        print(f"   Primary: {primary_model} on {primary_device.upper()}")
        print(f"   Fallback: {fallback_model} on {fallback_device.upper()}")
        
        # Real-time VRAM check for primary model
        if primary_device.lower() == 'gpu':
            if not vram_status['has_gpu']:
                print(f"⚠️ No GPU available, forcing CPU mode")
                primary_device = 'cpu'
            elif not can_model_fit_gpu(primary_model, available_vram):
                required = ASR_MODEL_VRAM_MB.get(primary_model, 0)
                print(f"⚠️ Insufficient VRAM for {primary_model} (need {required}MB, have {available_vram}MB)")
                print(f"🔄 Switching primary to CPU")
                primary_device = 'cpu'
        
        # Try primary model
        try:
            return try_load_model_with_fallback(primary_model, primary_device, primary_device)
        except:
            # Primary failed, try fallback model
            print(f"🔄 Primary model failed, trying fallback configuration...")
            
            # Real-time VRAM check for fallback model  
            if fallback_device.lower() == 'gpu':
                if not vram_status['has_gpu']:
                    print(f"⚠️ No GPU available for fallback, using CPU")
                    fallback_device = 'cpu'
                elif not can_model_fit_gpu(fallback_model, available_vram):
                    required = ASR_MODEL_VRAM_MB.get(fallback_model, 0)
                    print(f"⚠️ Insufficient VRAM for fallback {fallback_model} (need {required}MB, have {available_vram}MB)")
                    fallback_device = 'cpu'
            
            try:
                return try_load_model_with_fallback(fallback_model, fallback_device, 'cpu')
            except:
                print(f"❌ Both configured models failed!")
    
    else:
        # Fallback mode for GUI or missing config
        print(f"🔧 Using fallback mode: {DEFAULT_ASR_MODEL}")
    
    # Last resort: try default model with adaptive device selection
    print(f"🆘 Last resort: trying {DEFAULT_ASR_MODEL} with adaptive device selection")
    
    # Choose device based on real-time VRAM availability
    if vram_status['has_gpu'] and can_model_fit_gpu(DEFAULT_ASR_MODEL, available_vram):
        device = 'cuda'  # Use cuda directly for whisper
        device_display = 'GPU'
        print(f"✅ Using GPU for {DEFAULT_ASR_MODEL}")
    else:
        device = 'cpu'  
        device_display = 'CPU'
        print(f"🔄 Using CPU for {DEFAULT_ASR_MODEL}")
    
    try:
        import whisper
        model = whisper.load_model(DEFAULT_ASR_MODEL, device=device)
        print(f"✅ Successfully loaded {DEFAULT_ASR_MODEL} on {device_display}")
        return model, device_display.lower()
    except Exception as e:
        print(f"❌ Critical failure: Could not load {DEFAULT_ASR_MODEL} on {device}: {e}")
        
        # Ultimate fallback to CPU if GPU failed
        if device == 'cuda':
            try:
                print(f"🆘 Ultimate fallback: {DEFAULT_ASR_MODEL} on CPU")
                model = whisper.load_model(DEFAULT_ASR_MODEL, device='cpu')
                print(f"✅ Successfully loaded {DEFAULT_ASR_MODEL} on CPU")
                return model, 'cpu'
            except Exception as cpu_e:
                print(f"💀 Complete failure: {cpu_e}")
        
        return None, None

def cleanup_asr_model(asr_model):
    """Clean up ASR model to free memory"""
    if asr_model is not None:
        try:
            del asr_model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            print(f"🧹 ASR model cleaned up")
        except Exception as e:
            logging.warning(f"Failed to cleanup ASR model: {e}")

def get_asr_memory_info():
    """Get memory information for ASR debugging"""
    vram_status = get_real_time_vram_status()
    available_vram = calculate_available_vram_for_asr()
    
    info = {
        'vram_total_mb': vram_status['total_mb'],
        'vram_allocated_mb': vram_status['allocated_mb'],
        'vram_available_for_asr_mb': available_vram,
        'has_gpu': vram_status['has_gpu']
    }
    
    return info

if __name__ == "__main__":
    # Test the adaptive loading
    print("Testing ASR Manager...")
    info = get_asr_memory_info()
    print(f"Memory info: {info}")
    
    # Test adaptive loading
    model, device = load_asr_model_adaptive()
    if model:
        print(f"Test successful: Model loaded on {device}")
        cleanup_asr_model(model)
    else:
        print("Test failed: No model loaded")