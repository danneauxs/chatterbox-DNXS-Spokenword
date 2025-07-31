"""
Voice Sample Analyzer for ChatterboxTTS
Analyzes voice samples for TTS suitability using Praat and audio analysis libraries.
"""

__version__ = "1.0.0"
__author__ = "ChatterboxTTS Team"

# Main analysis function for external imports
from voice_analyzer.analyzer import analyze_voice_sample, VoiceAnalysisResult

__all__ = ['analyze_voice_sample', 'VoiceAnalysisResult']