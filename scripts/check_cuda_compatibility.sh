#!/bin/bash
# Shared CUDA compatibility checking function for all launchers

check_pytorch_cuda_compatibility() {
    echo "🔍 Checking PyTorch CUDA compatibility..."
    
    PYTORCH_CUDA_CHECK=$(python3 -c "
import torch
import sys
import subprocess

try:
    # Check if PyTorch has CUDA support
    if not hasattr(torch.version, 'cuda') or torch.version.cuda is None:
        print('CPU_ONLY')
        sys.exit(0)
    
    pytorch_cuda = torch.version.cuda
    
    # Try to detect system CUDA
    try:
        nvcc_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if nvcc_result.returncode == 0:
            import re
            match = re.search(r'release (\d+\.\d+)', nvcc_result.stdout)
            if match:
                system_cuda = match.group(1)
                
                # CUDA compatibility check with special handling for CUDA 12.0
                pytorch_version = float(pytorch_cuda)
                system_version = float(system_cuda)
                
                # CUDA 12.x family compatibility (12.0, 12.1, 12.2, etc.)
                if (system_version >= 12.0 and pytorch_version >= 12.0 and 
                    int(system_version) == 12 and int(pytorch_version) == 12):
                    print('COMPATIBLE')
                # CUDA 11.x family compatibility  
                elif (system_version >= 11.0 and pytorch_version >= 11.0 and 
                      int(system_version) == 11 and int(pytorch_version) == 11):
                    print('COMPATIBLE')
                # General rule: PyTorch CUDA should be <= System CUDA + tolerance
                elif pytorch_version <= system_version + 0.5:
                    print('COMPATIBLE')
                else:
                    print(f'MISMATCH:{pytorch_cuda}:{system_cuda}')
            else:
                print('UNKNOWN')
        else:
            print('NO_NVCC')
    except:
        print('NO_NVCC')
except Exception as e:
    print(f'ERROR:{str(e)}')
" 2>/dev/null)

    case "$PYTORCH_CUDA_CHECK" in
        "COMPATIBLE")
            echo "✅ PyTorch CUDA compatibility verified"
            return 0
            ;;
        "CPU_ONLY")
            echo "ℹ️ PyTorch CPU-only version detected"
            return 0
            ;;
        "NO_NVCC")
            echo "ℹ️ CUDA toolkit not found - using PyTorch as-is"
            return 0
            ;;
        "UNKNOWN")
            echo "⚠️ Could not determine CUDA compatibility"
            return 0
            ;;
        MISMATCH:*)
            IFS=':' read -r _ pytorch_cuda system_cuda <<< "$PYTORCH_CUDA_CHECK"
            echo "❌ PyTorch CUDA mismatch detected!"
            echo "   PyTorch CUDA: $pytorch_cuda"
            echo "   System CUDA:  $system_cuda"
            echo ""
            echo "🔧 This may cause GPU detection failures."
            echo ""
            echo "Options:"
            echo "  1) Auto-fix PyTorch installation now"
            echo "  2) Continue anyway (GPU may not work)"
            echo "  3) Exit"
            echo ""
            read -p "Choose [1/2/3]: " fix_choice
            case "$fix_choice" in
                1)
                    echo "🔧 Updating PyTorch for CUDA $system_cuda..."
                    pip install torch torchvision torchaudio --index-url "https://download.pytorch.org/whl/cu${system_cuda//./}" --upgrade
                    if [ $? -eq 0 ]; then
                        echo "✅ PyTorch updated successfully"
                        return 0
                    else
                        echo "❌ PyTorch update failed"
                        read -p "Continue with old PyTorch? [y/N]: " continue_anyway
                        if [[ "$continue_anyway" =~ ^[Yy]$ ]]; then
                            return 0
                        else
                            return 1
                        fi
                    fi
                    ;;
                2)
                    echo "⚠️ Continuing with mismatched PyTorch (GPU may not work)"
                    return 0
                    ;;
                *)
                    echo "Exiting..."
                    return 1
                    ;;
            esac
            ;;
        ERROR:*)
            echo "⚠️ Error checking PyTorch CUDA compatibility"
            return 0
            ;;
    esac
}