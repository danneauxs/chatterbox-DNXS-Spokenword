#!/bin/bash
# ChatterboxTTS Launcher Script
# Activates virtual environment and starts main_launcher.py

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths
VENV_DIR="$SCRIPT_DIR/venv"
MAIN_LAUNCHER="$SCRIPT_DIR/main_launcher.py"

echo "🚀 ChatterboxTTS Launcher"
echo "========================================"
echo "📁 Working directory: $SCRIPT_DIR"
echo "🐍 Virtual env: $VENV_DIR"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found!"
    echo "Expected location: $VENV_DIR"
    echo "Please run setup first or check if venv directory is correct."
    exit 1
fi

# Check if main_launcher.py exists
if [ ! -f "$MAIN_LAUNCHER" ]; then
    echo "❌ main_launcher.py not found!"
    echo "Expected location: $MAIN_LAUNCHER"
    exit 1
fi

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo "▶️  Starting main_launcher.py..."
echo ""

# Run main_launcher.py
python3 main_launcher.py

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ main_launcher.py completed successfully"
else
    echo "❌ main_launcher.py exited with code: $EXIT_CODE"
fi

# Deactivate virtual environment
deactivate

exit $EXIT_CODE