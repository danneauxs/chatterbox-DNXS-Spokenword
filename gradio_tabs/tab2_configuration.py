#!/usr/bin/env python3
"""
Gradio Tab 2: Configuration Settings
Matches PyQt5 GUI Tab 2 functionality with all configuration options
"""

import gradio as gr
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Import ChatterboxTTS configuration
try:
    from config.config import *
    CONFIG_AVAILABLE = True
except ImportError:
    print("⚠️  Config not available - using defaults")
    CONFIG_AVAILABLE = False
    MAX_WORKERS = 2
    BATCH_SIZE = 100
    MIN_CHUNK_WORDS = 5
    MAX_CHUNK_WORDS = 25
    ENABLE_NORMALIZATION = True
    TARGET_LUFS = -16
    ENABLE_AUDIO_TRIMMING = True
    SPEECH_ENDPOINT_THRESHOLD = 0.005
    TRIMMING_BUFFER_MS = 100
    TTS_PARAM_MIN_EXAGGERATION = 0.0
    TTS_PARAM_MAX_EXAGGERATION = 2.0
    TTS_PARAM_MIN_CFG_WEIGHT = 0.0
    TTS_PARAM_MAX_CFG_WEIGHT = 1.0
    TTS_PARAM_MIN_TEMPERATURE = 0.0
    TTS_PARAM_MAX_TEMPERATURE = 5.0
    DEFAULT_EXAGGERATION = 0.5
    DEFAULT_CFG_WEIGHT = 0.5
    DEFAULT_TEMPERATURE = 0.8
    VADER_EXAGGERATION_SENSITIVITY = 0.3
    VADER_CFG_WEIGHT_SENSITIVITY = 0.3
    VADER_TEMPERATURE_SENSITIVITY = 0.3
    SILENCE_CHAPTER_START = 1000
    SILENCE_CHAPTER_END = 1500
    SILENCE_SECTION_BREAK = 800
    SILENCE_PARAGRAPH_END = 500
    SILENCE_COMMA = 200
    SILENCE_PERIOD = 400
    SILENCE_QUESTION_MARK = 500
    SILENCE_EXCLAMATION = 500
    CHUNK_END_SILENCE_MS = 0

def create_configuration_tab():
    """Create Tab 2: Configuration Settings with all GUI functionality"""
    
    with gr.Column():
        gr.Markdown("# ⚙️ Configuration Settings")
        gr.Markdown("*System configuration and parameter management - matches GUI Tab 2*")
        
        # Top Row - Core Settings with Group Boxes
        with gr.Row():
            # Workers/Batch Settings Group
            with gr.Column():
                gr.Markdown("### 🔧 Workers & Batch Settings")
                gr.Markdown("*Set # workers for parallel processing. Too many workers will use up VRAM. Only increase if VRAM and GPU % are below 60% utilized. Batch size: set to determine when model is reloaded to flush VRAM and avoid recursive problems and slowdowns.*")
                
                workers_spin = gr.Slider(
                    label="Workers",
                    minimum=1, maximum=8, step=1,
                    value=MAX_WORKERS,
                    info="Number of parallel processing threads"
                )
                
                batch_size_spin = gr.Slider(
                    label="Batch Size",
                    minimum=50, maximum=500, step=50,
                    value=BATCH_SIZE,
                    info="Chunks processed before model reload"
                )
            
            # Min/Max Words Group
            with gr.Column():
                gr.Markdown("### 📝 Chunk Word Limits")
                gr.Markdown("*Set Min/Max for words in a text chunk. Too many words can lead to poor TTS.*")
                
                min_chunk_words_spin = gr.Slider(
                    label="Min Words",
                    minimum=1, maximum=50, step=1,
                    value=MIN_CHUNK_WORDS,
                    info="Minimum words per chunk"
                )
                
                max_chunk_words_spin = gr.Slider(
                    label="Max Words", 
                    minimum=10, maximum=100, step=1,
                    value=MAX_CHUNK_WORDS,
                    info="Maximum words per chunk"
                )
            
            # Audio Detection Group
            with gr.Column():
                gr.Markdown("### 🔊 Audio Processing")
                gr.Markdown("*Detects when audio speech stops and just noise or silence follow at end of audio chunk. Use threshold to change detection range of voice. Buffer adds ms silence to end of audio chunk.*")
                
                normalization_check = gr.Checkbox(
                    label="Audio normalization",
                    value=ENABLE_NORMALIZATION,
                    info="Enable loudness normalization"
                )
                
                target_lufs_spin = gr.Slider(
                    label="Target LUFS (dB)",
                    minimum=-30, maximum=-6, step=1,
                    value=TARGET_LUFS,
                    info="Target loudness level"
                )
                
                audio_trimming_check = gr.Checkbox(
                    label="Automatic audio trimming",
                    value=ENABLE_AUDIO_TRIMMING,
                    info="Trim silence from audio chunks"
                )
                
                speech_threshold_spin = gr.Slider(
                    label="Speech Threshold",
                    minimum=0.001, maximum=0.1, step=0.001,
                    value=SPEECH_ENDPOINT_THRESHOLD,
                    info="Speech detection sensitivity"
                )
                
                trimming_buffer_spin = gr.Slider(
                    label="Buffer (ms)",
                    minimum=0, maximum=500, step=10,
                    value=TRIMMING_BUFFER_MS,
                    info="Silence buffer after speech"
                )
        
        # TTS Parameter Limits Group
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔒 TTS Parameter Limits")
                gr.Markdown("*Set the upper and lower limits that TTS Params can be automatically adjusted to by VADER and other functions.*")
                
                with gr.Row():
                    exag_min_spin = gr.Slider(
                        label="Exag Min",
                        minimum=0.0, maximum=2.0, step=0.05,
                        value=TTS_PARAM_MIN_EXAGGERATION,
                        info="Minimum exaggeration limit"
                    )
                    
                    exag_max_spin = gr.Slider(
                        label="Exag Max",
                        minimum=0.0, maximum=2.0, step=0.05,
                        value=TTS_PARAM_MAX_EXAGGERATION,
                        info="Maximum exaggeration limit"
                    )
                
                with gr.Row():
                    cfg_min_spin = gr.Slider(
                        label="CFG Min",
                        minimum=0.0, maximum=1.0, step=0.05,
                        value=TTS_PARAM_MIN_CFG_WEIGHT,
                        info="Minimum CFG weight limit"
                    )
                    
                    cfg_max_spin = gr.Slider(
                        label="CFG Max",
                        minimum=0.0, maximum=1.0, step=0.05,
                        value=TTS_PARAM_MAX_CFG_WEIGHT,
                        info="Maximum CFG weight limit"
                    )
                
                with gr.Row():
                    temp_min_spin = gr.Slider(
                        label="Temp Min",
                        minimum=0.0, maximum=5.0, step=0.05,
                        value=TTS_PARAM_MIN_TEMPERATURE,
                        info="Minimum temperature limit"
                    )
                    
                    temp_max_spin = gr.Slider(
                        label="Temp Max",
                        minimum=0.0, maximum=5.0, step=0.05,
                        value=TTS_PARAM_MAX_TEMPERATURE,
                        info="Maximum temperature limit"
                    )
        
        # TTS Defaults and VADER Sensitivity Section
        with gr.Row():
            # TTS Defaults Group
            with gr.Column():
                gr.Markdown("### 🎯 TTS Defaults")
                gr.Markdown("*Default values: Exag: 0.50, CFG: 0.50, Temp: 0.80*")
                
                default_exag_spin = gr.Slider(
                    label="Default Exaggeration",
                    minimum=0.0, maximum=2.0, step=0.05,
                    value=DEFAULT_EXAGGERATION,
                    info="Base exaggeration value"
                )
                
                default_cfg_spin = gr.Slider(
                    label="Default CFG Weight",
                    minimum=0.0, maximum=1.0, step=0.05,
                    value=DEFAULT_CFG_WEIGHT,
                    info="Base CFG weight value"
                )
                
                default_temp_spin = gr.Slider(
                    label="Default Temperature",
                    minimum=0.0, maximum=5.0, step=0.05,
                    value=DEFAULT_TEMPERATURE,
                    info="Base temperature value"
                )
            
            # VADER Sensitivity Group
            with gr.Column():
                gr.Markdown("### 🎭 VADER Sensitivity")
                gr.Markdown("*Default values: Exag Sens: 0.30, CFG Sens: 0.30, Temp Sens: 0.30*")
                gr.Markdown("*VADER Sensitivity sets how much VADER adjusts the TTS params based on emotional weight.*")
                
                vader_exag_sens_spin = gr.Slider(
                    label="Exag Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_EXAGGERATION_SENSITIVITY,
                    info="VADER exaggeration adjustment strength"
                )
                
                vader_cfg_sens_spin = gr.Slider(
                    label="CFG Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_CFG_WEIGHT_SENSITIVITY,
                    info="VADER CFG weight adjustment strength"
                )
                
                vader_temp_sens_spin = gr.Slider(
                    label="Temp Sensitivity",
                    minimum=0.0, maximum=1.0, step=0.01,
                    value=VADER_TEMPERATURE_SENSITIVITY,
                    info="VADER temperature adjustment strength"
                )
        
        # Silence Settings Group
        with gr.Column():
            gr.Markdown("### 🔇 Silence Settings")
            gr.Markdown("*Set the silence added to audio chunks for each type of chunk. ie chapter start/end, period, paragraph. For each setting silence is added for pacing.*")
            
            # Chapter/Section silence
            with gr.Row():
                silence_chapter_start_spin = gr.Slider(
                    label="Chapter Start (ms)",
                    minimum=0, maximum=9999, step=100,
                    value=SILENCE_CHAPTER_START,
                    info="Silence before chapter starts"
                )
                
                silence_chapter_end_spin = gr.Slider(
                    label="Chapter End (ms)",
                    minimum=0, maximum=9999, step=100,
                    value=SILENCE_CHAPTER_END,
                    info="Silence after chapter ends"
                )
                
                silence_section_spin = gr.Slider(
                    label="Section Break (ms)",
                    minimum=0, maximum=9999, step=100,
                    value=SILENCE_SECTION_BREAK,
                    info="Silence for section breaks"
                )
                
                silence_paragraph_spin = gr.Slider(
                    label="Paragraph End (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=SILENCE_PARAGRAPH_END,
                    info="Silence after paragraphs"
                )
            
            # Punctuation silence
            with gr.Row():
                silence_comma_spin = gr.Slider(
                    label="Comma (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=SILENCE_COMMA,
                    info="Silence after commas"
                )
                
                silence_period_spin = gr.Slider(
                    label="Period (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=SILENCE_PERIOD,
                    info="Silence after periods"
                )
                
                silence_question_spin = gr.Slider(
                    label="Question Mark (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=SILENCE_QUESTION_MARK,
                    info="Silence after questions"
                )
                
                silence_exclamation_spin = gr.Slider(
                    label="Exclamation (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=SILENCE_EXCLAMATION,
                    info="Silence after exclamations"
                )
            
            # Chunk silence settings
            with gr.Row():
                chunk_end_silence_check = gr.Checkbox(
                    label="Enable Chunk End Silence",
                    value=CHUNK_END_SILENCE_MS > 0,
                    info="Add silence to end of every chunk"
                )
                
                chunk_end_silence_spin = gr.Slider(
                    label="Chunk End Silence (ms)",
                    minimum=0, maximum=9999, step=50,
                    value=CHUNK_END_SILENCE_MS,
                    info="Silence added to chunk ends"
                )
        
        # Config action buttons
        with gr.Row():
            save_config_btn = gr.Button(
                "💾 Save Configuration",
                variant="primary",
                size="lg"
            )
            
            reset_config_btn = gr.Button(
                "🔄 Reset to Defaults",
                variant="secondary",
                size="lg"
            )
            
            reload_config_btn = gr.Button(
                "♻️ Reload Configuration",
                variant="secondary",
                size="lg"
            )
        
        # Status display
        config_status = gr.Textbox(
            label="Configuration Status",
            value="Ready to save or load configuration",
            interactive=False,
            lines=2
        )
    
    # Event Handlers
    def save_configuration(*values):
        """Save current configuration settings"""
        try:
            if not CONFIG_AVAILABLE:
                return "❌ Configuration module not available"
            
            # Map values back to config variables
            config_values = {
                'MAX_WORKERS': int(values[0]),
                'BATCH_SIZE': int(values[1]),
                'MIN_CHUNK_WORDS': int(values[2]),
                'MAX_CHUNK_WORDS': int(values[3]),
                'ENABLE_NORMALIZATION': values[4],
                'TARGET_LUFS': int(values[5]),
                'ENABLE_AUDIO_TRIMMING': values[6],
                'SPEECH_ENDPOINT_THRESHOLD': values[7],
                'TRIMMING_BUFFER_MS': int(values[8]),
                'TTS_PARAM_MIN_EXAGGERATION': values[9],
                'TTS_PARAM_MAX_EXAGGERATION': values[10],
                'TTS_PARAM_MIN_CFG_WEIGHT': values[11],
                'TTS_PARAM_MAX_CFG_WEIGHT': values[12],
                'TTS_PARAM_MIN_TEMPERATURE': values[13],
                'TTS_PARAM_MAX_TEMPERATURE': values[14],
                'DEFAULT_EXAGGERATION': values[15],
                'DEFAULT_CFG_WEIGHT': values[16],
                'DEFAULT_TEMPERATURE': values[17],
                'VADER_EXAGGERATION_SENSITIVITY': values[18],
                'VADER_CFG_WEIGHT_SENSITIVITY': values[19],
                'VADER_TEMPERATURE_SENSITIVITY': values[20],
                'SILENCE_CHAPTER_START': int(values[21]),
                'SILENCE_CHAPTER_END': int(values[22]),
                'SILENCE_SECTION_BREAK': int(values[23]),
                'SILENCE_PARAGRAPH_END': int(values[24]),
                'SILENCE_COMMA': int(values[25]),
                'SILENCE_PERIOD': int(values[26]),
                'SILENCE_QUESTION_MARK': int(values[27]),
                'SILENCE_EXCLAMATION': int(values[28]),
                'CHUNK_END_SILENCE_MS': int(values[30]) if values[29] else 0
            }
            
            # Import the config module and update values using safe import
            try:
                from .gradio_imports import safe_import
                config_module = safe_import('config', 'config')
                for key, value in config_values.items():
                    if hasattr(config_module, key):
                        setattr(config_module, key, value)
            except ImportError:
                # Fallback to direct import
                from config import config
                for key, value in config_values.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
            
            return "✅ Configuration saved successfully!\n🔄 Settings updated in memory. Restart application to persist changes."
            
        except Exception as e:
            return f"❌ Error saving configuration: {str(e)}"
    
    def reset_configuration():
        """Reset all configuration values to defaults"""
        try:
            # Return default values for all controls
            return (
                2,      # MAX_WORKERS
                100,    # BATCH_SIZE
                5,      # MIN_CHUNK_WORDS
                25,     # MAX_CHUNK_WORDS
                True,   # ENABLE_NORMALIZATION
                -16,    # TARGET_LUFS
                True,   # ENABLE_AUDIO_TRIMMING
                0.005,  # SPEECH_ENDPOINT_THRESHOLD
                100,    # TRIMMING_BUFFER_MS
                0.0,    # TTS_PARAM_MIN_EXAGGERATION
                2.0,    # TTS_PARAM_MAX_EXAGGERATION
                0.0,    # TTS_PARAM_MIN_CFG_WEIGHT
                1.0,    # TTS_PARAM_MAX_CFG_WEIGHT
                0.0,    # TTS_PARAM_MIN_TEMPERATURE
                5.0,    # TTS_PARAM_MAX_TEMPERATURE
                0.5,    # DEFAULT_EXAGGERATION
                0.5,    # DEFAULT_CFG_WEIGHT
                0.8,    # DEFAULT_TEMPERATURE
                0.3,    # VADER_EXAGGERATION_SENSITIVITY
                0.3,    # VADER_CFG_WEIGHT_SENSITIVITY
                0.3,    # VADER_TEMPERATURE_SENSITIVITY
                1000,   # SILENCE_CHAPTER_START
                1500,   # SILENCE_CHAPTER_END
                800,    # SILENCE_SECTION_BREAK
                500,    # SILENCE_PARAGRAPH_END
                200,    # SILENCE_COMMA
                400,    # SILENCE_PERIOD
                500,    # SILENCE_QUESTION_MARK
                500,    # SILENCE_EXCLAMATION
                False,  # chunk_end_silence_check
                0,      # CHUNK_END_SILENCE_MS
                "🔄 Configuration reset to default values"
            )
            
        except Exception as e:
            return tuple([None] * 30 + [f"❌ Error resetting configuration: {str(e)}"])
    
    def reload_configuration():
        """Reload configuration from file"""
        try:
            if not CONFIG_AVAILABLE:
                return "❌ Configuration module not available"
            
            # Reload config module using safe import
            import importlib
            try:
                from .gradio_imports import safe_import
                config_module = safe_import('config', 'config')
                importlib.reload(config_module)
            except ImportError:
                # Fallback to direct import
                from config import config
                config_module = config
                importlib.reload(config)
            
            # Return reloaded values
            return (
                config_module.MAX_WORKERS,
                config_module.BATCH_SIZE,
                config_module.MIN_CHUNK_WORDS,
                config_module.MAX_CHUNK_WORDS,
                config_module.ENABLE_NORMALIZATION,
                config_module.TARGET_LUFS,
                config_module.ENABLE_AUDIO_TRIMMING,
                config_module.SPEECH_ENDPOINT_THRESHOLD,
                config_module.TRIMMING_BUFFER_MS,
                config_module.TTS_PARAM_MIN_EXAGGERATION,
                config_module.TTS_PARAM_MAX_EXAGGERATION,
                config_module.TTS_PARAM_MIN_CFG_WEIGHT,
                config_module.TTS_PARAM_MAX_CFG_WEIGHT,
                config_module.TTS_PARAM_MIN_TEMPERATURE,
                config_module.TTS_PARAM_MAX_TEMPERATURE,
                config_module.DEFAULT_EXAGGERATION,
                config_module.DEFAULT_CFG_WEIGHT,
                config_module.DEFAULT_TEMPERATURE,
                config_module.VADER_EXAGGERATION_SENSITIVITY,
                config_module.VADER_CFG_WEIGHT_SENSITIVITY,
                config_module.VADER_TEMPERATURE_SENSITIVITY,
                config_module.SILENCE_CHAPTER_START,
                config_module.SILENCE_CHAPTER_END,
                config_module.SILENCE_SECTION_BREAK,
                config_module.SILENCE_PARAGRAPH_END,
                config_module.SILENCE_COMMA,
                config_module.SILENCE_PERIOD,
                config_module.SILENCE_QUESTION_MARK,
                config_module.SILENCE_EXCLAMATION,
                config_module.CHUNK_END_SILENCE_MS > 0,
                config_module.CHUNK_END_SILENCE_MS,
                "✅ Configuration reloaded from file"
            )
            
        except Exception as e:
            return tuple([None] * 30 + [f"❌ Error reloading configuration: {str(e)}"])
    
    # All input components for save operation
    all_inputs = [
        workers_spin, batch_size_spin, min_chunk_words_spin, max_chunk_words_spin,
        normalization_check, target_lufs_spin, audio_trimming_check, 
        speech_threshold_spin, trimming_buffer_spin,
        exag_min_spin, exag_max_spin, cfg_min_spin, cfg_max_spin,
        temp_min_spin, temp_max_spin,
        default_exag_spin, default_cfg_spin, default_temp_spin,
        vader_exag_sens_spin, vader_cfg_sens_spin, vader_temp_sens_spin,
        silence_chapter_start_spin, silence_chapter_end_spin, 
        silence_section_spin, silence_paragraph_spin,
        silence_comma_spin, silence_period_spin, 
        silence_question_spin, silence_exclamation_spin,
        chunk_end_silence_check, chunk_end_silence_spin
    ]
    
    # All output components for reset/reload operations
    all_outputs = all_inputs + [config_status]
    
    # Connect event handlers
    save_config_btn.click(
        save_configuration,
        inputs=all_inputs,
        outputs=[config_status]
    )
    
    reset_config_btn.click(
        reset_configuration,
        inputs=[],
        outputs=all_outputs
    )
    
    reload_config_btn.click(
        reload_configuration,
        inputs=[],
        outputs=all_outputs
    )
    
    return {
        'save_button': save_config_btn,
        'reset_button': reset_config_btn,
        'reload_button': reload_config_btn,
        'status_display': config_status
    }

if __name__ == "__main__":
    # Test the tab
    with gr.Blocks() as demo:
        create_configuration_tab()
    
    demo.launch()