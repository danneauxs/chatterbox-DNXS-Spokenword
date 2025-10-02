# speed.tools.emotional_audio_enhancer

> Emotional Audio Enhancer for ChatterboxTTS

## Public API

### Classes
- **EmotionalAudioEnhancer**  
  Methods: setup_ui, create_tooltip, select_input_file, select_output_file, update_emotion_presets, check_audio_tools, start_processing, process_audio, apply_pitch_shift, apply_formant_shift, apply_compression, apply_eq, apply_tempo_change, apply_reverb, apply_tremolo, apply_vibrato, update_status, cleanup_temp_files, preview_audio, reset_settings, save_preset, load_preset

### Functions
- **main** — Main entry point.
- **setup_ui** — Create the main user interface.
- **create_tooltip** — Create a simple tooltip for a widget.
- **select_input_file** — Open file picker for input audio file.
- **select_output_file** — Open file picker for output audio file.
- **update_emotion_presets** — Update enhancement settings based on selected emotion.
- **check_audio_tools** — Check if required audio processing tools are available.
- **start_processing** — Start audio processing in a separate thread.
- **process_audio** — Process the audio file with selected enhancements.
- **apply_pitch_shift** — Apply pitch shifting using sox.
- **apply_formant_shift** — Apply formant shifting using sox bend effect.
- **apply_compression** — Apply dynamic range compression.
- **apply_eq** — Apply EQ/harmonic emphasis.
- **apply_tempo_change** — Apply tempo change.
- **apply_reverb** — Apply reverb effect.
- **apply_tremolo** — Apply tremolo effect.
- **apply_vibrato** — Apply vibrato effect.
- **update_status** — Update status label in thread-safe way.
- **cleanup_temp_files** — Clean up temporary files.
- **preview_audio** — Preview the processed audio (if tools available).
- **reset_settings** — Reset all settings to defaults.
- **save_preset** — Save current settings as a preset.
- **load_preset** — Load settings from a preset file.
- **on_closing**
- **on_enter**
- **on_leave**
- **update_display**

## Imports (local guesses)
- json, logging, os, pathlib, shutil, subprocess, tempfile, threading, tkinter, typing

## Side-effect signals
- subprocess

## Entrypoint
- Contains `if __name__ == '__main__':` block