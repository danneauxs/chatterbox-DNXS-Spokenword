@echo off
REM ChatterboxTTS Launcher Script for Windows
REM Activates virtual environment and starts main_launcher.py

echo 🚀 ChatterboxTTS Launcher
echo ========================================

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Define paths
set "VENV_DIR=%SCRIPT_DIR%\venv"
set "MAIN_LAUNCHER=%SCRIPT_DIR%\main_launcher.py"

echo 📁 Working directory: %SCRIPT_DIR%
echo 🐍 Virtual env: %VENV_DIR%

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo ❌ Virtual environment not found!
    echo Expected location: %VENV_DIR%
    echo Please run setup first or check if venv directory is correct.
    pause
    exit /b 1
)

REM Check if main_launcher.py exists
if not exist "%MAIN_LAUNCHER%" (
    echo ❌ main_launcher.py not found!
    echo Expected location: %MAIN_LAUNCHER%
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo ▶️  Starting main_launcher.py...
echo.

REM Run main_launcher.py
python main_launcher.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% equ 0 (
    echo ✅ main_launcher.py completed successfully
) else (
    echo ❌ main_launcher.py exited with code: %EXIT_CODE%
)

REM Deactivate virtual environment
call deactivate

echo.
echo Press any key to exit...
pause >nul
exit /b %EXIT_CODE%