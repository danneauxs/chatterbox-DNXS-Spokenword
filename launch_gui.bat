@echo off
REM Launcher script for ChatterboxTTS GUI on Windows

echo 🎙️ Launching ChatterboxTTS GUI
echo ==============================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check for virtual environment
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found - using system Python
)

REM Check PyTorch CUDA compatibility
echo 🔍 Checking PyTorch CUDA compatibility...

python -c "
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
        nvcc_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, shell=True)
        if nvcc_result.returncode == 0:
            import re
            match = re.search(r'release (\d+\.\d+)', nvcc_result.stdout)
            if match:
                system_cuda = match.group(1)
                
                # CUDA compatibility check with family-based matching
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
" > cuda_check_result.tmp 2>nul

set /p PYTORCH_CUDA_CHECK=<cuda_check_result.tmp
del cuda_check_result.tmp 2>nul

if "%PYTORCH_CUDA_CHECK%"=="COMPATIBLE" (
    echo ✅ PyTorch CUDA compatibility verified
) else if "%PYTORCH_CUDA_CHECK%"=="CPU_ONLY" (
    echo ℹ️ PyTorch CPU-only version detected
) else if "%PYTORCH_CUDA_CHECK%"=="NO_NVCC" (
    echo ℹ️ CUDA toolkit not found - using PyTorch as-is
) else if "%PYTORCH_CUDA_CHECK%"=="UNKNOWN" (
    echo ⚠️ Could not determine CUDA compatibility
) else if "%PYTORCH_CUDA_CHECK:~0,8%"=="MISMATCH" (
    echo ❌ PyTorch CUDA mismatch detected!
    for /f "tokens=2,3 delims=:" %%a in ("%PYTORCH_CUDA_CHECK%") do (
        echo    PyTorch CUDA: %%a
        echo    System CUDA:  %%b
    )
    echo.
    echo 🔧 This may cause GPU detection failures.
    echo    To fix: re-run the installation script
    echo.
    set /p continue_choice="Continue anyway? [y/N]: "
    if /i not "%continue_choice%"=="y" (
        echo Exiting...
        exit /b 1
    )
) else (
    echo ⚠️ Error checking PyTorch CUDA compatibility
)

REM Check if main GUI file exists
if not exist "chatterbox_gui.py" (
    echo ❌ chatterbox_gui.py not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

echo 🚀 Starting GUI...
echo.

REM Launch the GUI
python chatterbox_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Application exited with error code: %errorlevel%
    pause
)