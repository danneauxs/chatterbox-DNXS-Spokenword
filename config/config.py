"""
GenTTS Configuration Module
Central location for all settings, paths, and feature toggles
"""

import os
from pathlib import Path

# ============================================================================
# CORE DIRECTORIES
# ============================================================================
TEXT_INPUT_ROOT = Path("Text_Input")
AUDIOBOOK_ROOT = Path("Audiobook")
VOICE_SAMPLES_DIR = Path("Voice_Samples")

# ============================================================================
# TEXT PROCESSING SETTINGS
# ============================================================================
MAX_CHUNK_WORDS = 28
MIN_CHUNK_WORDS = 4

# ============================================================================
# WORKER AND PERFORMANCE SETTINGS
# ============================================================================
MAX_WORKERS = 2                       # Keep at 2 - GPU utilization already high
TEST_MAX_WORKERS = 6                  # For experimentation
USE_DYNAMIC_WORKERS = False           # Toggle for testing
VRAM_SAFETY_THRESHOLD = 6.5           # GB

# ============================================================================
# AUDIO QUALITY SETTINGS
# ============================================================================
ENABLE_MID_DROP_CHECK = False
ENABLE_ASR = False
ASR_WORKERS = 4                       # Parallel ASR on CPU threads

# ============================================================================
# TTS HUM DETECTION SETTINGS
# ============================================================================
ENABLE_HUM_DETECTION = False          # Disabled for speed (re-enable if quality issues)
HUM_FREQ_MIN = 50                     # Hz - Lower frequency bound for hum detection
HUM_FREQ_MAX = 200                    # Hz - Upper frequency bound for hum detection
HUM_ENERGY_THRESHOLD = 0.3            # Ratio of hum energy to total energy (0.1-0.5 range)
HUM_STEADY_THRESHOLD = 0.6            # Ratio of segments with steady amplitude (0.5-0.8 range)
HUM_AMPLITUDE_MIN = 0.005             # Minimum RMS for steady hum detection
HUM_AMPLITUDE_MAX = 0.1               # Maximum RMS for steady hum detection

# ============================================================================
# AUDIO TRIMMING SETTINGS
# ============================================================================
ENABLE_AUDIO_TRIMMING = True          # Enable automatic audio trimming after TTS
SPEECH_ENDPOINT_THRESHOLD = 0.005     # RMS threshold to detect end of speech (more aggressive)
TRIMMING_BUFFER_MS = 50               # Small buffer after detected speech endpoint

# ============================================================================
# SILENCE DURATION SETTINGS (milliseconds)
# ============================================================================
SILENCE_CHAPTER_START = 500           # Half second for chapter beginnings
SILENCE_CHAPTER_END = 400             # Longer pause before new chapter
SILENCE_SECTION_BREAK = 300           # Section transitions
SILENCE_PARAGRAPH_END = 300           # Standard paragraph breaks

# Punctuation-specific silence settings (milliseconds)
SILENCE_COMMA = 150                   # Brief pause after commas
SILENCE_SEMICOLON = 150               # Medium pause after semicolons
SILENCE_COLON = 150                   # Pause after colons
SILENCE_PERIOD = 200                  # Sentence end pause
SILENCE_QUESTION_MARK = 350           # Question pause (slightly longer)
SILENCE_EXCLAMATION = 300             # Exclamation pause
SILENCE_DASH = 200                    # Em dash pause
SILENCE_ELLIPSIS = 80                # Ellipsis pause (suspense)
SILENCE_QUOTE_END = 150               # End of quoted speech

# Chunk-level silence settings
ENABLE_CHUNK_END_SILENCE = True       # Add silence to end of every chunk
CHUNK_END_SILENCE_MS = 200            # Default silence at end of each chunk

# Content boundary silence settings (milliseconds)
SILENCE_PARAGRAPH_FALLBACK = 500      # Original paragraph logic fallback

# ============================================================================
# AUDIO NORMALIZATION SETTINGS
# ============================================================================
ENABLE_NORMALIZATION = True           # Global ON/OFF switch for normalization
NORMALIZATION_TYPE = "peak"           # Options: "loudness", "peak", "simple", "none"
TARGET_LUFS = -16                     # Target loudness (LUFS) for broadcast standard
TARGET_PEAK_DB = -1.5                 # Target peak level (dB) to prevent clipping
TARGET_LRA = 11                       # Target loudness range for consistency

# ============================================================================
# AUDIO PLAYBACK SPEED SETTINGS
# ============================================================================
ATEMPO_SPEED = 0.95                    # Playback speed multiplier (0.5-2.0 range, 1.0 = normal speed)

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"
os.environ["TRANSFORMERS_NO_PROGRESS_BAR"] = "1"
os.environ["HF_TRANSFORMERS_NO_TQDM"] = "1"
os.environ["TORCH_HUB_DIR"] = "/tmp/torch_hub_silent"

# ============================================================================
# COLOR CODES FOR TERMINAL OUTPUT
# ============================================================================
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

# ============================================================================
# TTS MODEL PARAMETERS (DEFAULTS)
# ============================================================================
DEFAULT_EXAGGERATION = 0.4            # Emotion intensity (0.0-2.0 range)
DEFAULT_CFG_WEIGHT = 0.3            # Faithfulness to text (0.0-1.0 range)
DEFAULT_TEMPERATURE = 0.4         # Randomness/creativity (0.0-1.0 range)

# ============================================================================
# VADER SENTIMENT TO TTS PARAMETER MAPPING
# ============================================================================
# These settings control how VADER sentiment analysis dynamically adjusts TTS parameters.
# The formula used is: new_param = base_param + (compound_score * sensitivity)
# The result is then clamped within the defined MIN/MAX range.

# --- Base TTS Parameters (used as the starting point) ---
# These are the same as the main defaults, but listed here for clarity.
BASE_EXAGGERATION = DEFAULT_EXAGGERATION  # Default: 1.0
BASE_CFG_WEIGHT = DEFAULT_CFG_WEIGHT      # Default: 0.7
BASE_TEMPERATURE = DEFAULT_TEMPERATURE    # Default: 0.7

# --- Sensitivity ---
# How much VADER's compound score affects each parameter.
# Higher values mean more dramatic changes based on sentiment.
VADER_EXAGGERATION_SENSITIVITY = 0.3  # e.g., compound of 0.8 -> 1.0 + (0.8 * 0.5) = 1.4
VADER_CFG_WEIGHT_SENSITIVITY = 0.833 # Negative: more emotional text is less strict
VADER_TEMPERATURE_SENSITIVITY = 0.35  # More emotional text gets slightly more creative

# --- Min/Max Clamps ---
# Hard limits to prevent extreme, undesirable audio artifacts.
TTS_PARAM_MIN_EXAGGERATION = 0.3
TTS_PARAM_MAX_EXAGGERATION = 0.85
TTS_PARAM_MIN_CFG_WEIGHT = 0.2
TTS_PARAM_MAX_CFG_WEIGHT = 0.9

TTS_PARAM_MIN_TEMPERATURE = 0.3
TTS_PARAM_MAX_TEMPERATURE = 0.7

# ============================================================================
# BATCH PROCESSING SETTINGS
# ============================================================================
BATCH_SIZE = 250                      # Larger batches for better speed (monitor VRAM)
CLEANUP_INTERVAL = 500                # Deep cleanup every N chunks (reduced frequency for speed)

# ============================================================================
# FEATURE TOGGLES
# ============================================================================
shutdown_requested = False           # Global shutdown flag
