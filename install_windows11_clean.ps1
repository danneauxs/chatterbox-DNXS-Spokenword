# ChatterboxTTS Windows 11 Installation Script - Clean Version
# Run as Administrator: Right-click PowerShell -> "Run as Administrator"

param(
    [switch]$SkipCUDA,
    [switch]$SkipGPU,
    [string]$InstallPath = "C:\ChatterboxTTS"
)

Write-Host "ChatterboxTTS Windows 11 Installation Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select Run as Administrator" -ForegroundColor Yellow
    exit 1
}

# Function to add to PATH
function Add-ToPath {
    param([string]$path)
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$path*") {
        Write-Host "Adding $path to system PATH..." -ForegroundColor Green
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$path", "Machine")
        $env:Path += ";$path"
    }
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([8-9]|1[0-9])") {
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Python 3.8+ required but found: $pythonVersion" -ForegroundColor Red
        Write-Host "Please install Python 3.8+ from python.org" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Python not found" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from python.org" -ForegroundColor Yellow
    exit 1
}

# Check Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Git not found - manual download required" -ForegroundColor Yellow
}

# Create installation directory
Write-Host "Creating installation directory: $InstallPath" -ForegroundColor Yellow
if (Test-Path $InstallPath) {
    Remove-Item $InstallPath -Recurse -Force
}
New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null

# Clone or copy repository
Set-Location $InstallPath
Write-Host "Downloading ChatterboxTTS..." -ForegroundColor Yellow

try {
    git clone https://github.com/USER/REPO.git . 2>&1 | Out-Null
    Write-Host "Repository cloned successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Git clone failed - using manual copy" -ForegroundColor Yellow
    # Copy files from current directory if git fails
    $sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Copy-Item "$sourceDir\*" $InstallPath -Recurse -Force
}

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
if (-not (Test-Path "venv\Scripts\activate.bat")) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\activate.bat"

# Install requirements
Write-Host "Installing Python packages..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "WARNING: requirements.txt not found - installing basic packages" -ForegroundColor Yellow
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip install gradio numpy soundfile librosa
}

# Test installation
Write-Host "Testing installation..." -ForegroundColor Yellow
try {
    python -c "import torch; print('PyTorch:', torch.__version__)" 2>&1 | Out-Null
    Write-Host "PyTorch installation verified" -ForegroundColor Green
} catch {
    Write-Host "WARNING: PyTorch test failed" -ForegroundColor Yellow
}

# Create desktop shortcut
Write-Host "Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\ChatterboxTTS GUI.lnk")
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = "chatterbox_gui.py"
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.Save()

Write-Host ""
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Cyan
Write-Host "Installation location: $InstallPath" -ForegroundColor White
Write-Host "Launch GUI: Double-click ChatterboxTTS GUI on desktop" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Place .txt books in Text_Input folder" -ForegroundColor White
Write-Host "2. Place .wav voice samples in Voice_Samples folder" -ForegroundColor White
Write-Host "3. Launch the GUI and start converting!" -ForegroundColor White
Write-Host ""
Write-Host "WARNING: Please restart your computer to ensure all PATH changes take effect." -ForegroundColor Red
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")