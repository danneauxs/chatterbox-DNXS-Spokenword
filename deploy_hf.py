#!/usr/bin/env python3
"""
HuggingFace Spaces Deployment Helper
Creates a clean deployment package for HF Spaces
"""

import os
import shutil
import tempfile
from pathlib import Path

def create_hf_deployment():
    """Create a clean HuggingFace Spaces deployment"""
    
    # Files needed for HF Spaces
    essential_files = [
        "gradio_app.py",
        "requirements_hf.txt", 
        "README_HF.md",
        "src/",
        "modules/",
        "config/",
        ".gitignore"
    ]
    
    # Create deployment directory
    deploy_dir = Path("hf_spaces_deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    print("🚀 Creating HuggingFace Spaces deployment...")
    
    # Copy essential files
    for item in essential_files:
        src_path = Path(item)
        if src_path.exists():
            dst_path = deploy_dir / item
            
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
                print(f"📁 Copied directory: {item}")
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"📄 Copied file: {item}")
        else:
            print(f"⚠️  Missing: {item}")
    
    # Rename files for HF Spaces
    (deploy_dir / "requirements_hf.txt").rename(deploy_dir / "requirements.txt")
    (deploy_dir / "README_HF.md").rename(deploy_dir / "README.md")
    
    # Create app.py (HF Spaces expects this name)
    shutil.copy2(deploy_dir / "gradio_app.py", deploy_dir / "app.py")
    
    print(f"✅ Deployment package created in: {deploy_dir}")
    print("\n📋 Next steps:")
    print("1. Create new HuggingFace Space at: https://huggingface.co/new-space")
    print("2. Choose 'Gradio' as SDK")
    print("3. Upload all files from hf_spaces_deploy/ directory")
    print("4. Set hardware to 't4-medium' or higher for GPU acceleration")
    print("5. Your space will be available at: https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME")

if __name__ == "__main__":
    create_hf_deployment()