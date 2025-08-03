#!/usr/bin/env python3
"""
ChatterboxTTS DNXS-Spokneword Gradio Main Interface
Modular web interface with separate tab modules
"""

import gradio as gr
import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

# Import tab modules
try:
    from gradio_tabs.tab1_convert_book import create_convert_book_tab
    TAB1_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tab 1 not available: {e}")
    TAB1_AVAILABLE = False

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

        # Tab interface
        with gr.Tabs():
            # Tab 1: Convert Book (Working)
            if TAB1_AVAILABLE:
                with gr.Tab("1. Convert Book"):
                    create_convert_book_tab()
            else:
                with gr.Tab("1. Convert Book"):
                    create_placeholder_tab("Convert Book", 1)

            # Tab 2-10: Placeholders for now
            with gr.Tab("2. File Management"):
                create_placeholder_tab("File Management", 2)

            with gr.Tab("3. Voice Analysis"):
                create_placeholder_tab("Voice Analysis", 3)

            with gr.Tab("4. Batch Processing"):
                create_placeholder_tab("Batch Processing", 4)

            with gr.Tab("5. Audio Tools"):
                create_placeholder_tab("Audio Tools", 5)

            with gr.Tab("6. Settings"):
                create_placeholder_tab("Settings", 6)

            with gr.Tab("7. Chunk Tools"):
                create_placeholder_tab("Chunk Tools", 7)

            with gr.Tab("8. Voice Training"):
                create_placeholder_tab("Voice Training", 8)

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
    print("   Tabs 2-10: 🚧 Placeholder (Coming Soon)")
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
