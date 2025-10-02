# chatterbox.multilingual_app

## Public API


### Functions
- **default_audio_for_ui**
- **default_text_for_ui**
- **get_supported_languages_display** — Generate a formatted display of all supported languages.
- **get_or_load_model** — Loads the ChatterboxMultilingualTTS model if it hasn't been loaded already,
- **set_seed** — Sets the random seed for reproducibility across torch, numpy, and random.
- **resolve_audio_prompt** — Decide which audio prompt to use:
- **generate_tts_audio** — Generate high-quality speech audio from text using Chatterbox Multilingual model with optional reference audio styling.
- **on_language_change**

## Imports (local guesses)
- chatterbox.mtl_tts, gradio, numpy, random, torch