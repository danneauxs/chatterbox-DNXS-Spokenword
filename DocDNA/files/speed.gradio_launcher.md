# speed.gradio_launcher

> Comprehensive Gradio Launcher for ChatterboxTTS

## Public API

### Classes
- **GradioLauncher**  
  Methods: print_header, check_python_version, check_working_directory, create_directories, check_package_installed, compare_versions, setup_virtual_environment, install_package, check_and_install_requirements, check_gpu_availability, verify_installation, launch_interface, run

### Functions
- **main** — Main entry point
- **print_header** — Print launcher header
- **check_python_version** — Check if Python version is compatible
- **check_working_directory** — Verify we're in the correct directory
- **create_directories** — Create required directories if they don't exist
- **check_package_installed** — Check if a package is installed and get its version
- **compare_versions** — Compare version strings
- **setup_virtual_environment** — Set up virtual environment if in externally managed environment
- **install_package** — Install a package using pip (with virtual environment support)
- **check_and_install_requirements** — Check and install all required packages
- **check_gpu_availability** — Check for GPU availability
- **verify_installation** — Verify that all components can be imported
- **launch_interface** — Launch the Gradio interface
- **run** — Run the complete launcher process

## Imports (local guesses)
- chatterbox, gradio_main_interface, importlib, os, parselmouth, pathlib, pkg_resources, subprocess, sys, time, torch

## Side-effect signals
- subprocess, sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block