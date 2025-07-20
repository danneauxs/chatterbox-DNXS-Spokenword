#!/bin/bash
# Automated HuggingFace Spaces Deployment

# Configuration
HF_USERNAME="bobsackett"  # Change this to your HF username
SPACE_NAME="DNXS-Spokenword"
HF_SPACE_URL="https://huggingface.co/spaces/bobsackett/DNXS-Spokenword"

echo "🚀 Deploying ChatterboxTTS to HuggingFace Spaces"
echo "Space URL will be: $HF_SPACE_URL"
echo ""

# Step 1: Create deployment package
echo "📦 Creating deployment package..."
python3 deploy_hf.py

# Step 2: Clone HF Space (create it first on HF website)
echo "📥 Cloning HuggingFace Space..."
if [ -d "hf_space_repo" ]; then
    rm -rf hf_space_repo
fi

git clone https://huggingface.co/spaces/bobsackett/DNXS-Spokenword
cd hf_space_repo

# Step 3: Copy deployment files
echo "📋 Copying files to HF Space..."
cp -r ../hf_spaces_deploy/* .

# Step 4: Git operations
echo "📤 Pushing to HuggingFace..."
git add .
git commit -m "Deploy ChatterboxTTS Audiobook Generator

- Gradio web interface for audiobook generation
- Voice cloning with ChatterboxTTS
- Smart text processing with sentiment analysis
- Optimized for HuggingFace Spaces GPU limits"

git push

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your space will be available at: $HF_SPACE_URL"
echo "⏱️  Allow 2-3 minutes for the space to build and start"
