#!/bin/bash
# Script to push fixed files to HuggingFace Space

echo "🚀 Preparing HuggingFace Space deployment with fixes..."

# Files that need to be uploaded to HF Space:
echo "📋 Files to upload:"
echo "1. app.py (fixed to use local ChatterboxTTS)"
echo "2. requirements.txt (removed chatterbox-tts dependency)" 
echo "3. src/chatterbox/models/s3tokenizer/utils.py (new file)"
echo "4. src/chatterbox/models/s3tokenizer/model_v2.py (new file)"

echo ""
echo "🔧 You can upload these files in two ways:"
echo ""

echo "METHOD 1: Git Push (if you have HF token)"
echo "=================================="
echo "# Get your HF token from: https://huggingface.co/settings/tokens"
echo "# Then run:"
echo "git clone https://YOUR_HF_TOKEN@huggingface.co/spaces/bobsackett/DNXS-Spokenword hf_temp"
echo "cd hf_temp"
echo "cp ../hf_spaces_deploy/app.py ."
echo "cp ../hf_spaces_deploy/requirements.txt ."
echo "cp -r ../hf_spaces_deploy/src ."
echo "cp -r ../hf_spaces_deploy/modules ."
echo "cp -r ../hf_spaces_deploy/config ."
echo "git add ."
echo "git commit -m 'Fix ChatterboxTTS dependencies and add missing files'"
echo "git push"
echo ""

echo "METHOD 2: Manual Upload (easier)"
echo "==============================="
echo "1. Go to: https://huggingface.co/spaces/bobsackett/DNXS-Spokenword/tree/main"
echo "2. Upload these files one by one:"
echo "   - hf_spaces_deploy/app.py"
echo "   - hf_spaces_deploy/requirements.txt"
echo "   - hf_spaces_deploy/src/chatterbox/models/s3tokenizer/utils.py"
echo "   - hf_spaces_deploy/src/chatterbox/models/s3tokenizer/model_v2.py"
echo ""

echo "🎯 Key fixes made:"
echo "✅ Created missing utils.py with padding functions"
echo "✅ Created missing model_v2.py with S3TokenizerV2 class"
echo "✅ Fixed app.py to use local ChatterboxTTS source"
echo "✅ Removed external chatterbox-tts dependency"
echo "✅ Added fallback text processing if modules fail"
echo ""

echo "🏃 After upload, your space should:"
echo "- Build successfully without import errors"
echo "- Keep all your advanced audiobook features"
echo "- Have proper error handling and fallbacks"