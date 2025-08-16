#!/usr/bin/env python3
"""
ChatterboxTTS Gradio Web Interface - Main Entry Point
====================================================

OVERVIEW:
This is the main web interface for ChatterboxTTS, providing a user-friendly
Gradio-based GUI for audiobook generation. It serves as the primary entry point
for users who prefer web interfaces over command-line tools.

ARCHITECTURE:
- MODULAR TAB SYSTEM: Each major function is a separate tab module
- GRACEFUL DEGRADATION: Missing tab modules show placeholder pages
- RESPONSIVE DESIGN: Works on desktop and mobile browsers
- IMPORT SAFETY: Handles missing dependencies gracefully

AVAILABLE TABS:
1. Convert Book (Tab 1) - FUNCTIONAL: Main TTS conversion interface
2. Quick Convert (Tab 2) - PLACEHOLDER: Fast conversion for small texts
3. Voice Analysis (Tab 3) - PLACEHOLDER: Voice sample analysis tools  
4. Batch Processing (Tab 4) - PLACEHOLDER: Multi-book processing
5. Audio Tools (Tab 5) - PLACEHOLDER: Audio editing and enhancement
6. Settings (Tab 6) - FUNCTIONAL: Configuration management
7. Chunk Tools (Tab 7) - PLACEHOLDER: Chunk editing and repair
8. Voice Training (Tab 8) - PLACEHOLDER: Voice cloning tools
9. System Monitor (Tab 9) - PLACEHOLDER: Performance monitoring

DEPLOYMENT MODES:
- LOCAL: python3 gradio_main_interface.py (development)
- HUGGINGFACE SPACES: Called by app.py launcher (production)
- COLAB/RUNPOD: Automatic sharing and port configuration

TECHNICAL FEATURES:
- Auto-detects HuggingFace Spaces environment
- Configurable sharing and port settings
- Error handling for missing tab modules
- Clean, professional interface design
"""

import gradio as gr
import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
# This ensures tab modules can be imported regardless of working directory
sys.path.append(str(Path(__file__).parent))

def detect_device_status():
    """Detect and return device status information"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
            return f"🚀 **GPU Active**: {gpu_name} ({gpu_memory:.1f}GB)", True
        else:
            return "💻 **CPU Mode**: GPU not available", False
    except Exception as e:
        return f"❌ **Device Detection Failed**: {e}", False

# Import tab modules
try:
    from gradio_tabs.tab1_convert_book import create_convert_book_tab
    TAB1_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 1 not available: {e}")
    TAB1_AVAILABLE = False

try:
    from gradio_tabs.tab2_configuration import create_configuration_tab
    TAB2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 2 (Configuration) not available: {e}")
    TAB2_AVAILABLE = False

try:
    from gradio_tabs.tab4_combine_audio import create_combine_audio_tab
    TAB4_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 4 (Combine Audio) not available: {e}")
    TAB4_AVAILABLE = False

try:
    from gradio_tabs.tab5_prepare_text import create_prepare_text_tab
    TAB5_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 5 (Prepare Text) not available: {e}")
    TAB5_AVAILABLE = False

try:
    from gradio_tabs.tab6_settings import create_settings_tab_interface
    TAB6_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 6 (Settings) not available: {e}")
    TAB6_AVAILABLE = False

try:
    from gradio_tabs.tab7_chunk_tools import create_chunk_tools_tab
    TAB7_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 7 (Chunk Tools) not available: {e}")
    TAB7_AVAILABLE = False

try:
    from gradio_tabs.tab8_json_generate import create_json_generate_tab
    TAB8_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 8 (JSON Generate) not available: {e}")
    TAB8_AVAILABLE = False

def create_placeholder_tab(tab_name, tab_number):
    """Create a placeholder tab for future implementation"""
    with gr.Column():
        gr.Markdown(f"# 🚧 {tab_name}")
        gr.Markdown(f"*Tab {tab_number} - Coming Soon*")
        gr.Markdown("This tab will be implemented in a future update.")

        gr.Button("Placeholder Button", interactive=False)

def create_main_interface():
    """Create the main ChatterboxTTS Gradio interface with all tabs"""

    with gr.Blocks(
        title="ChatterboxTTS - Complete Interface",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:

        # Header
        gr.Markdown("""
        # 🎤 ChatterboxTTS - Complete Web Interface
        *Modular audiobook generation system with advanced TTS capabilities*
        """)
        
        # Device Status
        device_text, is_gpu = detect_device_status()
        gr.Markdown(f"**Device Status**: {device_text}")

        # Tab interface
        with gr.Tabs():
            # Tab 1: Convert Book (Working)
            if TAB1_AVAILABLE:
                with gr.Tab("1. Convert Book"):
                    create_convert_book_tab()
            else:
                with gr.Tab("1. Convert Book"):
                    create_placeholder_tab("Convert Book", 1)

            # Tab 2: Configuration Settings (Working)
            if TAB2_AVAILABLE:
                with gr.Tab("2. Configuration"):
                    create_configuration_tab()
            else:
                with gr.Tab("2. Configuration"):
                    create_placeholder_tab("Configuration Settings", 2)

            with gr.Tab("3. Voice Analysis"):
                create_placeholder_tab("Voice Analysis", 3)

            # Tab 4: Combine Audio (Working)
            if TAB4_AVAILABLE:
                with gr.Tab("4. Combine Audio"):
                    create_combine_audio_tab()
            else:
                with gr.Tab("4. Combine Audio"):
                    create_placeholder_tab("Combine Audio", 4)

            # Tab 5: Prepare Text (Working)
            if TAB5_AVAILABLE:
                with gr.Tab("5. Prepare Text"):
                    create_prepare_text_tab()
            else:
                with gr.Tab("5. Prepare Text"):
                    create_placeholder_tab("Prepare Text", 5)

            # Tab 6: Settings (Working)
            if TAB6_AVAILABLE:
                with gr.Tab("6. Settings"):
                    create_settings_tab_interface()
            else:
                with gr.Tab("6. Settings"):
                    create_placeholder_tab("Settings", 6)

            # Tab 7: Chunk Tools (Working)
            if TAB7_AVAILABLE:
                with gr.Tab("7. Chunk Tools"):
                    create_chunk_tools_tab()
            else:
                with gr.Tab("7. Chunk Tools"):
                    create_placeholder_tab("Chunk Tools", 7)

            # Tab 8: JSON Generate (Working)
            if TAB8_AVAILABLE:
                with gr.Tab("8. JSON Generate"):
                    create_json_generate_tab()
            else:
                with gr.Tab("8. JSON Generate"):
                    create_placeholder_tab("JSON Generate", 8)

            with gr.Tab("9. System Monitor"):
                create_placeholder_tab("System Monitor", 9)

            with gr.Tab("10. About"):
                create_placeholder_tab("About", 10)

        # Footer
        gr.Markdown("""
        ---
        *ChatterboxTTS Gradio Interface - Modular Design*
        Each tab is a separate module for easy maintenance and development.
        """)

    return demo

def launch_interface():
    """Launch the main interface"""
    print("🚀 ChatterboxTTS - Starting Main Interface")
    print("📊 Tab Status:")
    print(f"   Tab 1 (Convert Book): {'✅ Available' if TAB1_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 2 (Configuration): {'✅ Available' if TAB2_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 4 (Combine Audio): {'✅ Available' if TAB4_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 5 (Prepare Text): {'✅ Available' if TAB5_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 6 (Settings): {'✅ Available' if TAB6_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 7 (Chunk Tools): {'✅ Available' if TAB7_AVAILABLE else '❌ Not Available'}")
    print(f"   Tab 8 (JSON Generate): {'✅ Available' if TAB8_AVAILABLE else '❌ Not Available'}")
    print("   Other Tabs: 🚧 Placeholder (Coming Soon)")
    print("-" * 50)

    demo = create_main_interface()

    # Launch configuration
    launch_kwargs = {
        'server_name': '0.0.0.0',
        'server_port': 7860,
        'show_error': True,
        'quiet': False
    }

    # Detect cloud environments
    if os.getenv("RUNPOD_POD_ID"):
        print("☁️  RunPod deployment detected")
        launch_kwargs['share'] = True
    elif os.getenv("COLAB_GPU"):
        print("☁️  Google Colab detected")
        launch_kwargs['share'] = True
    else:
        print("💻 Local deployment")
        launch_kwargs['share'] = False

    print(f"🌐 Interface will be available at: http://localhost:{launch_kwargs['server_port']}")

    try:
        demo.launch(**launch_kwargs)
    except Exception as e:
        print(f"❌ Error launching interface: {e}")
        raise

if __name__ == "__main__":
    launch_interface()
