#!/usr/bin/env python3
"""
Comprehensive Gradio Launcher for ChatterboxTTS
Automatically handles all requirements, installation, and setup
"""

import sys
import os
import subprocess
import importlib
import pkg_resources
from pathlib import Path
import time

class GradioLauncher:
    def __init__(self):
        self.required_packages = {
            # Core packages with fallbacks
            'gradio': {'min_version': '4.0.0', 'install_name': 'gradio>=4.0.0'},
            'torch': {'min_version': '2.0.0', 'install_name': 'torch>=2.0.0'},
            'torchaudio': {'min_version': '2.0.0', 'install_name': 'torchaudio>=2.0.0'},
            'transformers': {'min_version': '4.20.0', 'install_name': 'transformers>=4.20.0'},
            'huggingface_hub': {'min_version': '0.15.0', 'install_name': 'huggingface_hub>=0.15.0'},
            'safetensors': {'min_version': '0.3.0', 'install_name': 'safetensors>=0.3.0'},

            # Audio processing
            'soundfile': {'min_version': '0.12.0', 'install_name': 'soundfile>=0.12.0'},
            'librosa': {'min_version': '0.10.0', 'install_name': 'librosa>=0.10.0'},
            'pydub': {'min_version': '0.25.0', 'install_name': 'pydub>=0.25.0'},

            # Voice Analysis (optional but recommended)
            'parselmouth': {'min_version': '0.4.3', 'install_name': 'praat-parselmouth>=0.4.3', 'optional': True},
            'matplotlib': {'min_version': '3.5.0', 'install_name': 'matplotlib>=3.5.0'},
            'scipy': {'min_version': '1.8.0', 'install_name': 'scipy>=1.8.0'},
            'numpy': {'min_version': '1.21.0', 'install_name': 'numpy>=1.21.0'},

            # System utilities
            'psutil': {'min_version': '5.8.0', 'install_name': 'psutil>=5.8.0'},
            'vaderSentiment': {'min_version': '3.3.0', 'install_name': 'vaderSentiment>=3.3.0'},
        }

        self.chatterbox_git_url = 'git+https://github.com/resemble-ai/chatterbox-tts.git'
        self.optional_packages = ['parselmouth', 'pynvml']

    def print_header(self):
        """Print launcher header"""
        print("=" * 70)
        print("🚀 ChatterboxTTS Gradio Launcher")
        print("=" * 70)
        print("🔧 Comprehensive setup and dependency manager")
        print("📦 Automatically installs missing requirements")
        print("🌐 Launches web interface when ready")
        print("-" * 70)

    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")

        version_info = sys.version_info
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
            print("❌ Error: Python 3.8+ required")
            print(f"   Current version: {version_info.major}.{version_info.minor}.{version_info.micro}")
            print("   Please upgrade Python and try again")
            sys.exit(1)

        print(f"✅ Python {version_info.major}.{version_info.minor}.{version_info.micro} - Compatible")

    def check_working_directory(self):
        """Verify we're in the correct directory"""
        print("📁 Checking working directory...")


        if missing_files:
            print(f"❌ Error: Missing required files/directories: {', '.join(missing_files)}")
            print("   Please run this script from the ChatterboxTTS root directory")
            print("   Expected structure:")
            print("   ├── gradio_main_interface.py")
            print("   ├── gradio_tabs/")
            print("   ├── config/")
            print("   ├── src/")
            print("   └── ...")
            return False

        print("✅ Working directory structure verified")
        return True

    def create_directories(self):
        """Create required directories if they don't exist"""
        print("📂 Creating required directories...")

        directories = ['Voice_Samples', 'Text_Input', 'Audiobook', 'Output', 'voice_analyzer']
        created = []

        for dir_name in directories:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                created.append(dir_name)

        if created:
            print(f"✅ Created directories: {', '.join(created)}")
        else:
            print("✅ All required directories exist")

    def check_package_installed(self, package_name):
        """Check if a package is installed and get its version"""
        # If we have a virtual environment, check there first
        if hasattr(self, 'venv_python') and Path(self.venv_python).exists():
            try:
                cmd = [self.venv_python, '-c', f'''
try:
    import {package_name}
    print("INSTALLED", getattr({package_name}, "__version__", "0.0.0"))
except ImportError:
    print("NOT_INSTALLED")
''']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    output = result.stdout.strip()
                    if output.startswith("INSTALLED"):
                        version = output.split(" ", 1)[1] if " " in output else "0.0.0"
                        return True, version
                    else:
                        return False, None
            except Exception:
                pass  # Fall back to local check

        # Fallback to local Python environment check
        try:
            if package_name == 'parselmouth':
                # Special case for praat-parselmouth
                import parselmouth
                return True, getattr(parselmouth, '__version__', '0.0.0')
            else:
                module = importlib.import_module(package_name)
                version = getattr(module, '__version__', '0.0.0')
                return True, version
        except ImportError:
            try:
                # Try with pkg_resources as fallback
                pkg = pkg_resources.get_distribution(package_name)
                return True, pkg.version
            except (pkg_resources.DistributionNotFound, ImportError):
                return False, None

    def compare_versions(self, current, required):
        """Compare version strings"""
        try:
            current_parts = [int(x) for x in current.split('.')]
            required_parts = [int(x) for x in required.split('.')]

            # Pad shorter version with zeros
            max_len = max(len(current_parts), len(required_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            required_parts.extend([0] * (max_len - len(required_parts)))

            return current_parts >= required_parts
        except (ValueError, AttributeError):
            # If we can't parse versions, assume it's okay
            return True

    def setup_virtual_environment(self):
        """Set up virtual environment if in externally managed environment"""
        venv_path = Path("venv")

        if not venv_path.exists():
            print("🔧 Creating virtual environment (externally managed Python detected)...")
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'venv', 'venv'],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    print(f"   ❌ Failed to create virtual environment: {result.stderr}")
                    return False
                print("   ✅ Virtual environment created")
            except Exception as e:
                print(f"   ❌ Error creating virtual environment: {e}")
                return False
        else:
            print("🔧 Using existing virtual environment...")

        # Update sys.executable to use venv python
        if os.name == 'nt':  # Windows
            self.venv_python = str(venv_path / "Scripts" / "python.exe")
            self.venv_pip = str(venv_path / "Scripts" / "pip.exe")
        else:  # Unix/Linux/Mac
            self.venv_python = str(venv_path / "bin" / "python")
            self.venv_pip = str(venv_path / "bin" / "pip")

        # Verify venv python works
        try:
            result = subprocess.run([self.venv_python, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Virtual environment Python: {result.stdout.strip()}")
                return True
            else:
                print("   ❌ Virtual environment Python not working")
                return False
        except Exception as e:
            print(f"   ❌ Error testing virtual environment: {e}")
            return False

    def install_package(self, package_spec):
        """Install a package using pip (with virtual environment support)"""
        try:
            print(f"   Installing {package_spec}...")

            # Use venv pip if available, otherwise system pip
            pip_executable = getattr(self, 'venv_pip', None)
            if pip_executable and Path(pip_executable).exists():
                cmd = [pip_executable, 'install', package_spec]
            else:
                cmd = [sys.executable, '-m', 'pip', 'install', package_spec]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                print(f"   ✅ Successfully installed {package_spec}")
                return True
            else:
                print(f"   ❌ Failed to install {package_spec}")
                print(f"   Error: {result.stderr}")

                # If we get externally-managed error, try setting up venv
                if "externally-managed-environment" in result.stderr and not hasattr(self, 'venv_python'):
                    print("   🔄 Detected externally managed environment, setting up virtual environment...")
                    if self.setup_virtual_environment():
                        # Retry installation with venv
                        return self.install_package(package_spec)

                return False

        except subprocess.TimeoutExpired:
            print(f"   ⏰ Installation of {package_spec} timed out")
            return False
        except Exception as e:
            print(f"   ❌ Error installing {package_spec}: {str(e)}")
            return False

    def check_and_install_requirements(self):
        """Check and install all required packages"""
        print("📦 Checking package requirements...")

        missing_packages = []
        outdated_packages = []
        optional_missing = []

        # Check each required package
        for package_name, info in self.required_packages.items():
            is_installed, current_version = self.check_package_installed(package_name)
            min_version = info['min_version']
            is_optional = info.get('optional', False)

            if not is_installed:
                if is_optional:
                    optional_missing.append((package_name, info))
                    print(f"   ⚠️  Optional package missing: {package_name}")
                else:
                    missing_packages.append((package_name, info))
                    print(f"   ❌ Missing required package: {package_name}")
            elif current_version and not self.compare_versions(current_version, min_version):
                if is_optional:
                    print(f"   ⚠️  Optional package outdated: {package_name} {current_version} < {min_version}")
                else:
                    outdated_packages.append((package_name, info))
                    print(f"   ❌ Outdated package: {package_name} {current_version} < {min_version}")
            else:
                status = "✅" if not is_optional else "🔧"
                print(f"   {status} {package_name}: {current_version}")

        # Install missing/outdated packages
        if missing_packages or outdated_packages:
            print(f"\n🔧 Installing {len(missing_packages + outdated_packages)} required packages...")

            for package_name, info in missing_packages + outdated_packages:
                install_spec = info['install_name']
                if not self.install_package(install_spec):
                    print(f"❌ Critical error: Failed to install {package_name}")
                    return False

        # Install ChatterboxTTS if not available
        print("🎤 Checking ChatterboxTTS installation...")
        try:
            import chatterbox
            print("   ✅ ChatterboxTTS already installed")
        except ImportError:
            print("   📥 Installing ChatterboxTTS from GitHub...")
            if not self.install_package(self.chatterbox_git_url):
                print("   ⚠️  ChatterboxTTS installation failed - some features may not work")

        # Try to install optional packages
        if optional_missing:
            print(f"\n🎯 Installing {len(optional_missing)} optional packages...")
            for package_name, info in optional_missing:
                install_spec = info['install_name']
                if self.install_package(install_spec):
                    print(f"   ✅ Optional package {package_name} installed successfully")
                else:
                    print(f"   ⚠️  Optional package {package_name} failed - voice analysis may be limited")

        return True

    def check_gpu_availability(self):
        """Check for GPU availability"""
        print("🖥️  Checking GPU availability...")

        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0)
                print(f"   ✅ CUDA GPU available: {gpu_name} ({gpu_count} device{'s' if gpu_count > 1 else ''})")
                return True
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("   ✅ Apple Metal Performance Shaders (MPS) available")
                return True
            else:
                print("   ⚠️  No GPU acceleration available - using CPU")
                print("   💡 For better performance, consider using a GPU-enabled environment")
                return False
        except Exception as e:
            print(f"   ❌ Error checking GPU: {str(e)}")
            return False

    def verify_installation(self):
        """Verify that all components can be imported"""
        print("🔍 Verifying installation...")

        critical_imports = [
            ('gradio', 'Gradio web interface'),
            ('torch', 'PyTorch machine learning'),
            ('transformers', 'Hugging Face transformers'),
            ('librosa', 'Audio processing'),
            ('soundfile', 'Audio file I/O'),
            ('numpy', 'Numerical computing'),
            ('matplotlib', 'Plotting and visualization')
        ]

        optional_imports = [
            ('parselmouth', 'Praat voice analysis'),
            ('scipy', 'Scientific computing'),
            ('psutil', 'System monitoring')
        ]

        failed_critical = []
        failed_optional = []

        # Check critical imports
        for module_name, description in critical_imports:
            try:
                importlib.import_module(module_name)
                print(f"   ✅ {description}")
            except ImportError as e:
                print(f"   ❌ {description}: {str(e)}")
                failed_critical.append(module_name)

        # Check optional imports
        for module_name, description in optional_imports:
            try:
                importlib.import_module(module_name)
                print(f"   🔧 {description}")
            except ImportError:
                print(f"   ⚠️  {description}: Not available")
                failed_optional.append(module_name)

        if failed_critical:
            print(f"\n❌ Critical imports failed: {', '.join(failed_critical)}")
            print("   The interface may not work properly")
            return False

        if failed_optional:
            print(f"\n⚠️  Optional features unavailable: {', '.join(failed_optional)}")
            print("   Voice analysis features may be limited")

        print("✅ Installation verification complete")
        return True

    def launch_interface(self):
        """Launch the Gradio interface"""
        print("\n🚀 Launching ChatterboxTTS Gradio Interface...")
        print("-" * 50)

        # If we're using a virtual environment, launch with venv python
        if hasattr(self, 'venv_python') and Path(self.venv_python).exists():
            print("🔧 Using virtual environment Python...")
            try:
                print("🌐 Starting web server...")
                print("📱 Interface will be available in your browser")
                print("🔗 Default URL: http://localhost:7860")

                if os.getenv("RUNPOD_POD_ID"):
                    print("☁️  RunPod deployment detected")
                elif os.getenv("COLAB_GPU"):
                    print("☁️  Google Colab detected - sharing link will be generated")

                print("\n" + "=" * 50)
                print("🎉 LAUNCHING CHATTERBOX TTS!")
                print("=" * 50)

                # Launch using virtual environment python
                subprocess.run([self.venv_python, "gradio_main_interface.py"])

            except KeyboardInterrupt:
                print("\n\n👋 Shutdown requested by user")
                print("   Thanks for using ChatterboxTTS!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error launching with virtual environment: {str(e)}")
                print("   Falling back to direct import...")
                self._launch_direct()
        else:
            self._launch_direct()

    def _launch_direct(self):
        """Launch interface by direct import"""
        try:
            # Import and launch
            from gradio_main_interface import launch_interface

            print("🌐 Starting web server...")
            print("📱 Interface will be available in your browser")
            print("🔗 Default URL: http://localhost:7860")

            if os.getenv("RUNPOD_POD_ID"):
                print("☁️  RunPod deployment detected")
            elif os.getenv("COLAB_GPU"):
                print("☁️  Google Colab detected - sharing link will be generated")

            print("\n" + "=" * 50)
            print("🎉 LAUNCHING CHATTERBOX TTS!")
            print("=" * 50)

            # Small delay for user to read messages
            time.sleep(2)

            # Launch the interface
            launch_interface()

        except KeyboardInterrupt:
            print("\n\n👋 Shutdown requested by user")
            print("   Thanks for using ChatterboxTTS!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error launching interface: {str(e)}")
            print("\nTroubleshooting tips:")
            print("1. Check that all dependencies are installed")
            print("2. Verify you're in the correct directory")
            if hasattr(self, 'venv_python'):
                print(f"3. Try running: {self.venv_python} gradio_main_interface.py")
            else:
                print("3. Try running: python3 gradio_main_interface.py")
            sys.exit(1)

    def run(self):
        """Run the complete launcher process"""
        self.print_header()

        # Step 1: Check Python version
        self.check_python_version()

        # Step 2: Check working directory
        if not self.check_working_directory():
            sys.exit(1)

        # Step 3: Create required directories
        self.create_directories()

        # Step 4: Check and install requirements
        if not self.check_and_install_requirements():
            print("\n❌ Failed to install required packages")
            sys.exit(1)

        # Step 5: Check GPU availability
        self.check_gpu_availability()

        # Step 6: Verify installation
        if not self.verify_installation():
            print("\n⚠️  Installation verification failed")
            print("   Proceeding anyway - some features may not work")

        # Step 7: Launch interface
        self.launch_interface()

def main():
    """Main entry point"""
    launcher = GradioLauncher()
    launcher.run()

if __name__ == "__main__":
      # Add current directory to Python path for HF Spaces
      import sys
      import os
      sys.path.append(os.path.dirname(os.path.abspath(__file__)))
      
      # Fix OpenMP environment variable for HuggingFace Spaces
      os.environ["OMP_NUM_THREADS"] = "1"

      # Skip launcher logic for HF Spaces, run interface directly
      try:
          # Import the actual Gradio interface
          import gradio_main_interface

          # Create and launch the interface
          demo = gradio_main_interface.create_main_interface()
          demo.launch(
              server_name="0.0.0.0",
              server_port=7860,
              share=False,
              show_error=True
          )
      except ImportError as e:
          print(f"❌ Failed to import gradio_main_interface: {e}")
          # Fallback to launcher if needed
          launcher = GradioLauncher()
          launcher.launch_interface()
