#!/usr/bin/env python3
"""
ChatterboxTTS Launcher
Activates virtual environment and starts main_launcher.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Define paths
    venv_dir = script_dir / "venv"
    main_launcher = script_dir / "main_launcher.py"
    
    # Check if virtual environment exists
    if not venv_dir.exists():
        print("❌ Virtual environment not found!")
        print(f"Expected location: {venv_dir}")
        print("Please run setup first or check if venv directory is correct.")
        return 1
    
    # Check if main_launcher.py exists
    if not main_launcher.exists():
        print("❌ main_launcher.py not found!")
        print(f"Expected location: {main_launcher}")
        return 1
    
    # Determine the correct Python executable in venv
    if os.name == 'nt':  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:  # Linux/macOS
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print(f"❌ Python executable not found in virtual environment!")
        print(f"Expected location: {python_exe}")
        return 1
    
    print("🚀 ChatterboxTTS Launcher")
    print("=" * 40)
    print(f"📁 Working directory: {script_dir}")
    print(f"🐍 Virtual env: {venv_dir}")
    print(f"▶️  Starting main_launcher.py...")
    print()
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run main_launcher.py with the virtual environment's Python
        result = subprocess.run([str(python_exe), str(main_launcher)], 
                              cwd=script_dir,
                              check=False)
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⏹️ Launcher interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error running launcher: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())