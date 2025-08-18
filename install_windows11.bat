@echo off
REM ChatterboxTTS Windows 11 Installation Launcher
REM This batch file launches the PowerShell installer script
REM Double-click to run - no special permissions needed for this .bat file

echo.
echo =====================================================
echo    ChatterboxTTS Windows 11 Installation Launcher
echo =====================================================
echo.
echo This will launch the PowerShell installation script...
echo.

REM Check if PowerShell script exists
if not exist "%~dp0install_windows11.ps1" (
    echo ❌ Error: install_windows11.ps1 not found!
    echo Please ensure install_windows11.ps1 is in the same folder as this batch file.
    pause
    exit /b 1
)

echo 🔍 Checking PowerShell execution policy...

REM Try to run PowerShell script with bypass policy
echo.
echo 🚀 Launching ChatterboxTTS installer...
echo.
echo ⚠️  If you see a security warning, choose [Y] Yes to allow the script to run.
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0install_windows11.ps1"

REM Check if PowerShell script succeeded
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Installation completed successfully!
) else (
    echo.
    echo ❌ Installation failed with error code: %ERRORLEVEL%
    echo.
    echo 🔧 Troubleshooting tips:
    echo    1. Right-click this file and "Run as Administrator"
    echo    2. Check antivirus software isn't blocking the installation
    echo    3. Ensure you have internet connection for downloads
)

echo.
echo Press any key to exit...
pause >nul