#!/bin/bash
# Launcher script for ChatterboxTTS GUI

echo "🎙️ Launching ChatterboxTTS GUI"
echo "=============================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for PyQt5 availability before activating venv
echo "Checking for PyQt5..."
PYQT5_SYSTEM_AVAILABLE=0
PYQT5_VENV_AVAILABLE=0

# Check system-wide PyQt5
if python3 -c "import PyQt5" 2>/dev/null; then
    echo "✅ PyQt5 found in system Python"
    PYQT5_SYSTEM_AVAILABLE=1
fi

# Check if we should use venv or system Python
USE_VENV=0

# Try to activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Found virtual environment, checking PyQt5 in venv..."
    source venv/bin/activate
    if python3 -c "import PyQt5" 2>/dev/null; then
        echo "✅ PyQt5 found in virtual environment"
        PYQT5_VENV_AVAILABLE=1
        USE_VENV=1
    else
        echo "⚠️ PyQt5 not found in virtual environment"
        if [ $PYQT5_SYSTEM_AVAILABLE -eq 1 ]; then
            echo "🔄 Deactivating venv to use system PyQt5"
            deactivate
            USE_VENV=0
        fi
    fi
elif [ -d "../venv" ]; then
    echo "🔧 Found virtual environment in parent directory, checking PyQt5..."
    source ../venv/bin/activate
    if python3 -c "import PyQt5" 2>/dev/null; then
        echo "✅ PyQt5 found in virtual environment"
        PYQT5_VENV_AVAILABLE=1
        USE_VENV=1
    else
        echo "⚠️ PyQt5 not found in virtual environment"
        if [ $PYQT5_SYSTEM_AVAILABLE -eq 1 ]; then
            echo "🔄 Deactivating venv to use system PyQt5"
            deactivate
            USE_VENV=0
        fi
    fi
fi

# Final check
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo "❌ PyQt5 not found in any Python environment!"
    echo ""
    if [ $USE_VENV -eq 1 ]; then
        echo "To install in virtual environment:"
        echo "  source venv/bin/activate"
        echo "  pip install PyQt5"
    else
        echo "To install system-wide:"
        echo "  pip install PyQt5"
        echo "  # or"
        echo "  sudo apt install python3-pyqt5"
    fi
    exit 1
fi

if [ $USE_VENV -eq 1 ]; then
    echo "✅ Using virtual environment"
else
    echo "✅ Using system Python"
fi

echo "✅ PyQt5 found"

# Check for optional dependencies
if ! python3 -c "import vaderSentiment" 2>/dev/null; then
    echo "⚠️ Warning: vaderSentiment not found (sentiment analysis will be disabled)"
fi

# Check if main GUI file exists
if [ ! -f "main_launcher_gui.py" ]; then
    echo "❌ main_launcher_gui.py not found!"
    echo "Make sure you're in the correct directory."
    exit 1
fi

echo "🚀 Starting GUI..."
echo ""

# Launch the GUI
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python3 main_launcher_gui.py

exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "❌ Application exited with error code: $exit_code"
fi

exit $exit_code