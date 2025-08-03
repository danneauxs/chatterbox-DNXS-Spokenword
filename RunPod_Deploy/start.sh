#!/bin/bash
# DNXS-Spokenword [Chatterbox-xTTS] Startup Script
# Main launcher with interface selection

set -e

# Colors for branding
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Brand header
echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                                                          ║${NC}"
echo -e "${MAGENTA}║        ${CYAN}🎙️  DNXS-Spokenword [Chatterbox-xTTS]${MAGENTA}           ║${NC}"
echo -e "${MAGENTA}║                                                          ║${NC}"
echo -e "${MAGENTA}║            ${YELLOW}Advanced TTS Audiobook Generation${MAGENTA}             ║${NC}"
echo -e "${MAGENTA}║                                                          ║${NC}"
echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Environment setup
echo -e "${BLUE}🔧 Setting up environment...${NC}"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Activating virtual environment${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  No virtual environment found, using system Python${NC}"
fi

# Set environment variables
export CHATTERBOX_DATA_ROOT=${CHATTERBOX_DATA_ROOT:-/workspace/data}
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}

# Check if we're in the right directory
if [ ! -f "gradio_main_interface.py" ] && [ ! -f "main_launcher.py" ]; then
    echo -e "${RED}❌ Error: ChatterboxTTS files not found${NC}"
    echo -e "${YELLOW}💡 Expected files in current directory${NC}"
    echo -e "${YELLOW}💡 Please run the installation script first or navigate to /workspace${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environment ready${NC}"
echo ""

# Interface selection menu
echo -e "${CYAN}📋 Select Interface:${NC}"
echo ""
echo -e "${GREEN}1)${NC} 🌐 ${BLUE}Gradio Web Interface${NC} ${YELLOW}(Recommended)${NC}"
echo -e "   • Modern web-based interface"
echo -e "   • Accessible via browser"
echo -e "   • Real-time progress monitoring"
echo ""
echo -e "${GREEN}2)${NC} 💻 ${BLUE}CLI Menu Interface${NC}"
echo -e "   • Command-line interface"
echo -e "   • Full feature access"
echo -e "   • Advanced options available"
echo ""
echo -e "${GREEN}3)${NC} ❌ ${BLUE}Exit${NC}"
echo ""

# Get user choice
while true; do
    read -p $'\033[1;36mSelect interface [1-3]: \033[0m' choice
    
    case $choice in
        1)
            echo ""
            echo -e "${MAGENTA}🚀 Starting DNXS-Spokenword [Chatterbox-xTTS] Web Interface${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}🌐 Launching Gradio interface...${NC}"
            echo -e "${YELLOW}📱 Interface will be available on port 7860${NC}"
            
            if [ -n "$RUNPOD_POD_ID" ]; then
                echo -e "${CYAN}☁️  RunPod detected - public link will be generated${NC}"
            fi
            
            echo ""
            # Use venv if available, otherwise system python
            if [ -d "venv" ] && [ "$VIRTUAL_ENV" != "" ]; then
                python3 gradio_main_interface.py
            elif [ -d "venv" ]; then
                echo -e "${BLUE}🔄 Activating virtual environment for Gradio...${NC}"
                source venv/bin/activate
                python3 gradio_main_interface.py
            else
                python3 gradio_main_interface.py
            fi
            break
            ;;
        2)
            echo ""
            echo -e "${MAGENTA}🚀 Starting DNXS-Spokenword [Chatterbox-xTTS] CLI Interface${NC}"
            echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}💻 Launching command-line interface...${NC}"
            echo ""
            python3 main_launcher.py
            break
            ;;
        3)
            echo ""
            echo -e "${YELLOW}👋 Thank you for using DNXS-Spokenword [Chatterbox-xTTS]${NC}"
            echo -e "${BLUE}Visit us at: ${CYAN}https://dnxs.ai${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid selection. Please choose 1, 2, or 3.${NC}"
            ;;
    esac
done