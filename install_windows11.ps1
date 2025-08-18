# ChatterboxTTS Windows 11 Installation Script
# Run as Administrator: Right-click PowerShell -> "Run as Administrator"
# Enable execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

param(
    [switch]$SkipCUDA,
    [switch]$SkipGPU,
    [string]$InstallPath = "C:\ChatterboxTTS"
)

Write-Host "🚀 ChatterboxTTS Windows 11 Installation Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Function to check if command exists
function Test-Command($command) {
    try { if(Get-Command $command) { return $true } }
    catch { return $false }
}

# Function to download file
function Download-File($url, $output) {
    Write-Host "📥 Downloading $output..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
}

# Function to add to PATH
function Add-ToPath($path) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$path*") {
        Write-Host "➕ Adding $path to system PATH..." -ForegroundColor Green
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$path", "Machine")
        $env:Path += ";$path"
    }
}

Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check Python
if (-not (Test-Command "python")) {
    Write-Host "📦 Installing Python 3.11..." -ForegroundColor Green
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    Download-File $pythonUrl "python-installer.exe"
    Start-Process -FilePath "python-installer.exe" -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
    Remove-Item "python-installer.exe"
    
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Host "✅ Python already installed" -ForegroundColor Green
}

# Check Git
if (-not (Test-Command "git")) {
    Write-Host "📦 Installing Git..." -ForegroundColor Green
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    Download-File $gitUrl "git-installer.exe"
    Start-Process -FilePath "git-installer.exe" -ArgumentList "/VERYSILENT", "/NORESTART" -Wait
    Remove-Item "git-installer.exe"
    
    # Add Git to PATH
    Add-ToPath "C:\Program Files\Git\bin"
} else {
    Write-Host "✅ Git already installed" -ForegroundColor Green
}

# Install FFmpeg (with user choice)
if (-not (Test-Command "ffmpeg")) {
    Write-Host ""
    Write-Host "🎬 FFmpeg Installation" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    Write-Host "FFmpeg is required for creating M4B audiobook files." -ForegroundColor White
    Write-Host ""
    Write-Host "✅ With FFmpeg you can:" -ForegroundColor Green
    Write-Host "   • Convert audio to M4B audiobook format" -ForegroundColor White
    Write-Host "   • Add cover art and metadata" -ForegroundColor White
    Write-Host "   • Apply audio normalization" -ForegroundColor White
    Write-Host "   • Adjust playback speed" -ForegroundColor White
    Write-Host ""
    Write-Host "❌ Without FFmpeg:" -ForegroundColor Red
    Write-Host "   • You can generate WAV audio chunks" -ForegroundColor White
    Write-Host "   • You CANNOT create final M4B audiobooks" -ForegroundColor White
    Write-Host "   • Limited audio processing features" -ForegroundColor White
    Write-Host ""
    Write-Host "📦 Install FFmpeg now? [Y/n]: " -ForegroundColor Yellow -NoNewline
    $installFFmpeg = Read-Host
    
    if ($installFFmpeg.ToLower() -ne 'n') {
        Write-Host "📦 Installing FFmpeg..." -ForegroundColor Green
        try {
            $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            Download-File $ffmpegUrl "ffmpeg.zip"
            
            Expand-Archive -Path "ffmpeg.zip" -DestinationPath "C:\ffmpeg-temp" -Force
            $extractedFolder = Get-ChildItem "C:\ffmpeg-temp" | Where-Object { $_.PSIsContainer } | Select-Object -First 1
            Move-Item "$($extractedFolder.FullName)" "C:\ffmpeg" -Force
            Remove-Item "ffmpeg.zip"
            Remove-Item "C:\ffmpeg-temp" -Recurse -Force
            
            Add-ToPath "C:\ffmpeg\bin"
            
            # Verify installation
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            if (Test-Command "ffmpeg") {
                Write-Host "✅ FFmpeg installed successfully" -ForegroundColor Green
            } else {
                throw "FFmpeg not found in PATH after installation"
            }
        }
        catch {
            Write-Host "❌ FFmpeg installation failed: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "⚠️  You can install FFmpeg manually later:" -ForegroundColor Yellow
            Write-Host "   1. Download from: https://ffmpeg.org/download.html" -ForegroundColor White
            Write-Host "   2. Extract to C:\ffmpeg\" -ForegroundColor White  
            Write-Host "   3. Add C:\ffmpeg\bin to system PATH" -ForegroundColor White
            Write-Host "   4. Restart ChatterboxTTS" -ForegroundColor White
            Write-Host ""
            Write-Host "⚠️  Continuing installation without FFmpeg..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  Skipping FFmpeg installation" -ForegroundColor Yellow
        Write-Host "   Note: M4B audiobook creation will not be available" -ForegroundColor White
        Write-Host "   You can install FFmpeg later if needed" -ForegroundColor White
    }
} else {
    Write-Host "✅ FFmpeg already installed" -ForegroundColor Green
}

# Install CUDA (optional)
if (-not $SkipCUDA -and -not $SkipGPU) {
    Write-Host "🎮 Installing CUDA Toolkit 11.8..." -ForegroundColor Green
    $cudaUrl = "https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe"
    Download-File $cudaUrl "cuda-installer.exe"
    Start-Process -FilePath "cuda-installer.exe" -ArgumentList "-s" -Wait
    Remove-Item "cuda-installer.exe"
}

# Create installation directory
Write-Host "📁 Creating installation directory: $InstallPath" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
Set-Location $InstallPath

# Clone repository
Write-Host "📂 Cloning ChatterboxTTS repository..." -ForegroundColor Green
git clone https://github.com/your-repo/ChatterboxTTS-DNXS-Spokenwordv1.git .

# Create virtual environment
Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Green
python -m venv venv

# Activate virtual environment and install packages
Write-Host "📦 Installing Python packages..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
python -m pip install --upgrade pip

# Install PyTorch with CUDA support
if (-not $SkipGPU) {
    Write-Host "🔥 Installing PyTorch with CUDA support..." -ForegroundColor Green
    
    # Detect CUDA version for optimal PyTorch installation
    $cudaVersion = ""
    if (Test-Command "nvcc") {
        try {
            $nvccOutput = nvcc --version 2>$null
            if ($nvccOutput -match "release (\d+\.\d+)") {
                $cudaVersion = $matches[1]
                Write-Host "✅ CUDA Runtime detected: $cudaVersion" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️  Could not detect CUDA runtime version" -ForegroundColor Yellow
        }
    }
    
    # Map CUDA version to PyTorch version
    switch ($cudaVersion) {
        { $_ -in @("12.8", "12.9") } {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
            Write-Host "✅ Installed PyTorch with CUDA 12.8 support" -ForegroundColor Green
        }
        { $_ -in @("12.1", "12.2", "12.3") } {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
            Write-Host "✅ Installed PyTorch with CUDA 12.1 support" -ForegroundColor Green
        }
        { $_ -in @("12.0") } {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
            Write-Host "✅ Installed PyTorch with CUDA 12.1 support (compatible with CUDA 12.0)" -ForegroundColor Green
        }
        { $_ -in @("11.8", "11.9") } {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
            Write-Host "✅ Installed PyTorch with CUDA 11.8 support" -ForegroundColor Green
        }
        default {
            Write-Host "⚠️  CUDA version $cudaVersion not specifically supported, using CUDA 12.1" -ForegroundColor Yellow
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        }
    }
} else {
    Write-Host "💻 Installing PyTorch (CPU only)..." -ForegroundColor Green
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
}

# Install main requirements
if (Test-Path "requirements.txt") {
    Write-Host "📋 Installing main requirements..." -ForegroundColor Green
    pip install -r requirements.txt
}

# Install voice analyzer requirements
if (Test-Path "voice_analyzer\requirements.txt") {
    Write-Host "🎤 Installing voice analyzer requirements..." -ForegroundColor Green
    pip install -r voice_analyzer\requirements.txt
}

# Create directories
Write-Host "📁 Creating required directories..." -ForegroundColor Green
$directories = @("Text_Input", "Voice_Samples", "Audiobook", "Output")
foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# Create launch scripts
Write-Host "🚀 Creating launch scripts..." -ForegroundColor Green

# GUI launcher
$guiScript = @"
@echo off
cd /d "$InstallPath"
call venv\Scripts\activate.bat
python chatterbox_gui.py
pause
"@
$guiScript | Out-File -FilePath "Launch_GUI.bat" -Encoding ASCII

# CLI launcher  
$cliScript = @"
@echo off
cd /d "$InstallPath"
call venv\Scripts\activate.bat
python main_launcher.py
pause
"@
$cliScript | Out-File -FilePath "Launch_CLI.bat" -Encoding ASCII

# Create desktop shortcuts
Write-Host "🖥️ Creating desktop shortcuts..." -ForegroundColor Green
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\ChatterboxTTS GUI.lnk")
$Shortcut.TargetPath = "$InstallPath\Launch_GUI.bat"
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.Save()

# Test installation
Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Test FFmpeg functionality
Write-Host "🎬 Testing FFmpeg..." -ForegroundColor Yellow
if (Test-Command "ffmpeg") {
    try {
        $ffmpegTest = ffmpeg -version 2>&1 | Select-String "ffmpeg version" | Select-Object -First 1
        Write-Host "✅ FFmpeg working: $($ffmpegTest.Line.Split(' ')[2])" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  FFmpeg found but may not be working properly" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ FFmpeg not available - audio conversion will not work" -ForegroundColor Red
}

# Test audio system (simplified - skip complex audio testing)
Write-Host "🔊 Testing audio system..." -ForegroundColor Yellow

try {
    $audioTestResult = python -c "import pygame; print('AUDIO_TEST_SUCCESS')" 2>$null
    if ($audioTestResult -match "AUDIO_TEST_SUCCESS") {
        $audioWorking = $true
    } else {
        $audioWorking = $false
    }
} catch {
    $audioWorking = $false
}

if ($audioWorking) {
    Write-Host "✅ Audio system working - voice preview will be available" -ForegroundColor Green
} else {
    Write-Host "Warning: Audio system issue detected:" -ForegroundColor Yellow
    Write-Host "   Voice preview may not work properly" -ForegroundColor Yellow
    Write-Host "   This will not affect TTS generation - only GUI audio preview" -ForegroundColor Yellow
    Write-Host "   Common fixes:" -ForegroundColor White
    Write-Host "   • Update audio drivers" -ForegroundColor White
    Write-Host "   • Check Windows audio settings" -ForegroundColor White
    Write-Host "   • Restart after installation" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "📍 Installation location: $InstallPath" -ForegroundColor White
Write-Host "🚀 Launch GUI: Double-click ChatterboxTTS GUI on desktop" -ForegroundColor White
Write-Host "🚀 Launch CLI: Run Launch_CLI.bat in installation folder" -ForegroundColor White
Write-Host ""
Write-Host "📖 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Place .txt books in Text_Input folder" -ForegroundColor White
Write-Host "2. Place .wav voice samples in Voice_Samples folder" -ForegroundColor White
Write-Host "3. Launch the GUI and start converting!" -ForegroundColor White
Write-Host ""
Write-Host "WARNING: Please restart your computer to ensure all PATH changes take effect." -ForegroundColor Red