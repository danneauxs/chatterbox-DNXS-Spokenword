#!/usr/bin/env python3
"""
Common import utilities for Gradio tabs - HuggingFace deployment compatibility
"""

import os
import sys

def safe_import(module_name, package=None):
    """Safely import modules with HuggingFace deployment compatibility"""
    try:
        if package:
            return __import__(f"{package}.{module_name}", fromlist=[module_name])
        else:
            return __import__(module_name, fromlist=[''])
    except ImportError:
        # Try adding parent directory to path for HuggingFace deployment
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.join(current_dir, '..')
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        try:
            if package:
                return __import__(f"{package}.{module_name}", fromlist=[module_name])
            else:
                return __import__(module_name, fromlist=[''])
        except ImportError:
            raise

def safe_import_config():
    """Safely import config module and return all config variables"""
    try:
        config_module = safe_import('config', 'config')
        # Return dictionary of all config variables
        return {name: getattr(config_module, name) for name in dir(config_module) if not name.startswith('_')}, True
    except ImportError as e:
        print(f"⚠️  Config not available: {e} - using defaults")
        return {}, False

def get_default_config():
    """Return default configuration values for when config is not available"""
    return {
        'AUDIOBOOK_ROOT': 'Audiobook',
        'TEXT_INPUT_ROOT': 'Text_Input', 
        'VOICE_SAMPLES_DIR': 'Voice_Samples',
        'MAX_WORKERS': 2,
        'BATCH_SIZE': 100,
        'MIN_CHUNK_WORDS': 5,
        'MAX_CHUNK_WORDS': 25,
        'ENABLE_NORMALIZATION': True,
        'TARGET_LUFS': -16,
        'ENABLE_AUDIO_TRIMMING': True,
        'SPEECH_ENDPOINT_THRESHOLD': 0.005,
        'TRIMMING_BUFFER_MS': 100,
        'TTS_PARAM_MIN_EXAGGERATION': 0.0,
        'TTS_PARAM_MAX_EXAGGERATION': 2.0,
        'TTS_PARAM_MIN_CFG_WEIGHT': 0.0,
        'TTS_PARAM_MAX_CFG_WEIGHT': 1.0,
        'TTS_PARAM_MIN_TEMPERATURE': 0.0,
        'TTS_PARAM_MAX_TEMPERATURE': 5.0,
        'DEFAULT_EXAGGERATION': 0.5,
        'DEFAULT_CFG_WEIGHT': 0.5,
        'DEFAULT_TEMPERATURE': 0.8,
        'VADER_EXAGGERATION_SENSITIVITY': 0.3,
        'VADER_CFG_WEIGHT_SENSITIVITY': 0.3,
        'VADER_TEMPERATURE_SENSITIVITY': 0.3,
        'SILENCE_CHAPTER_START': 1000,
        'SILENCE_CHAPTER_END': 1500,
        'SILENCE_SECTION_BREAK': 800,
        'SILENCE_PARAGRAPH_END': 500,
        'SILENCE_COMMA': 200,
        'SILENCE_PERIOD': 400,
        'SILENCE_QUESTION_MARK': 500,
        'SILENCE_EXCLAMATION': 500,
        'CHUNK_END_SILENCE_MS': 0,
        'ENABLE_SENTIMENT_SMOOTHING': True,
        'SENTIMENT_SMOOTHING_WINDOW': 3,
        'SENTIMENT_SMOOTHING_METHOD': 'gaussian',
        'BASE_EXAGGERATION': 0.5,
        'BASE_CFG_WEIGHT': 0.5,
        'BASE_TEMPERATURE': 0.8,
        'DEFAULT_MIN_P': 0.1,
        'DEFAULT_TOP_P': 0.9,
        'DEFAULT_REPETITION_PENALTY': 1.0
    }