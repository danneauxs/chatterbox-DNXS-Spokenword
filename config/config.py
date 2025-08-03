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
MAX_WORKERS = 2
TEST_MAX_WORKERS = 6                  # For experimentation
USE_DYNAMIC_WORKERS = False           # Toggle for testing
VRAM_SAFETY_THRESHOLD = 6.5           # GB

# ============================================================================
# AUDIO QUALITY SETTINGS
# ============================================================================
ENABLE_MID_DROP_CHECK = False
ENABLE_ASR = False  # Disabled by default due to tensor dimension errors
ASR_WORKERS = 4                       # Parallel ASR on CPU threads
DEFAULT_ASR_MODEL = "base"            # Default Whisper model for ASR validation

# ASR Model Memory Requirements (approximate)
ASR_MODEL_VRAM_MB = {
    "tiny": 39,
    "base": 74, 
    "small": 244,
    "medium": 769,
    "large": 1550,
    "large-v2": 1550,
    "large-v3": 1550
}

ASR_MODEL_RAM_MB = {
    "tiny": 150,
    "base": 300,
    "small": 800, 
    "medium": 2000,
    "large": 4000,
    "large-v2": 4000,
    "large-v3": 4000
}

# ============================================================================
# TTS HUM DETECTION SETTINGS
# ============================================================================
ENABLE_HUM_DETECTION = False
HUM_FREQ_MIN = 50                     # Hz - Lower frequency bound for hum detection
HUM_FREQ_MAX = 200                    # Hz - Upper frequency bound for hum detection
HUM_ENERGY_THRESHOLD = 0.3            # Ratio of hum energy to total energy (0.1-0.5 range)
HUM_STEADY_THRESHOLD = 0.6            # Ratio of segments with steady amplitude (0.5-0.8 range)
HUM_AMPLITUDE_MIN = 0.005             # Minimum RMS for steady hum detection
HUM_AMPLITUDE_MAX = 0.1               # Maximum RMS for steady hum detection

# ============================================================================
# AUDIO TRIMMING SETTINGS
# ============================================================================
ENABLE_AUDIO_TRIMMING = True
SPEECH_ENDPOINT_THRESHOLD = 0.005
TRIMMING_BUFFER_MS = 50

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
ENABLE_NORMALIZATION = True
NORMALIZATION_TYPE = "peak"
TARGET_LUFS = -16
TARGET_PEAK_DB = -1.5
TARGET_LRA = 11                       # Target loudness range for consistency

# ============================================================================
# AUDIO PLAYBACK SPEED SETTINGS
# ============================================================================
ATEMPO_SPEED = 0.95

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"
os.environ["TRANSFORMERS_NO_PROGRESS_BAR"] = "1"
os.environ["HF_TRANSFORMERS_NO_TQDM"] = "1"
# Cache handling is now done by launcher scripts:
# - launch_gradio_local.sh: Sets shared cache for development
# - launch_gradio.sh: Uses PyTorch defaults for containers/deployment

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
DEFAULT_EXAGGERATION = 0.5
DEFAULT_CFG_WEIGHT = 0.5
DEFAULT_TEMPERATURE = 0.8

# Advanced Sampling Parameters (Min_P Sampler Support)
DEFAULT_MIN_P = 0.05                   # Min probability threshold (0.0 disables)
DEFAULT_TOP_P = 1.0                    # Top-p sampling (1.0 disables)
DEFAULT_REPETITION_PENALTY = 1.2      # Repetition penalty (1.0 = no penalty)

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
VADER_EXAGGERATION_SENSITIVITY = 0.3
VADER_CFG_WEIGHT_SENSITIVITY = 0.3
VADER_TEMPERATURE_SENSITIVITY = 0.3
VADER_MIN_P_SENSITIVITY = 0.01         # Reduced from 0.02 to prevent sampling issues
VADER_REPETITION_PENALTY_SENSITIVITY = 0.05  # Reduced from 0.1 to be more conservative

# --- Min/Max Clamps ---
# Hard limits to prevent extreme, undesirable audio artifacts.
TTS_PARAM_MIN_EXAGGERATION = 0.10000000000000002
TTS_PARAM_MAX_EXAGGERATION = 0.65
TTS_PARAM_MIN_CFG_WEIGHT = 0.10000000000000002
TTS_PARAM_MAX_CFG_WEIGHT = 0.9

TTS_PARAM_MIN_TEMPERATURE = 0.1
TTS_PARAM_MAX_TEMPERATURE = 1.8

TTS_PARAM_MIN_MIN_P = 0.02             # Increased from 0.0 to prevent sampling issues
TTS_PARAM_MAX_MIN_P = 0.3              # Reduced from MAX 0.5 to prevent over-restriction
TTS_PARAM_MIN_TOP_P = 0.5              # Too low causes repetition
TTS_PARAM_MAX_TOP_P = 1.0              # MAX 1.0 disables top_p
TTS_PARAM_MIN_REPETITION_PENALTY = 1.0 # 1.0 = no penalty
TTS_PARAM_MAX_REPETITION_PENALTY = 2.0 # Higher values too restrictive MAX 2

# ============================================================================
# BATCH PROCESSING SETTINGS
# ============================================================================
BATCH_SIZE = 250
CLEANUP_INTERVAL = 500                # Deep cleanup every N chunks (reduced frequency for speed)

# ============================================================================
# QUALITY ENHANCEMENT SETTINGS (Phase 1)
# ============================================================================

# --- Regeneration Loop Settings ---
ENABLE_REGENERATION_LOOP = True      # Enable automatic chunk regeneration on quality failure
MAX_REGENERATION_ATTEMPTS = 3        # Maximum retry attempts per chunk
QUALITY_THRESHOLD = 0.30              # TEMPORARILY LOWERED - Composite quality score threshold (0.0-1.0)

# --- Sentiment Smoothing Settings ---
ENABLE_SENTIMENT_SMOOTHING = True    # Re-enabled - GUI controls now working properly
SENTIMENT_SMOOTHING_WINDOW = 3       # Number of previous chunks to consider
SENTIMENT_SMOOTHING_METHOD = "rolling"  # "rolling" or "exp_decay"

# Exponential decay weights for smoothing (used if method is "exp_decay")
SENTIMENT_EXP_DECAY_WEIGHTS = [0.5, 0.3, 0.2]  # Most recent to oldest

# --- Enhanced Anomaly Detection ---
SPECTRAL_ANOMALY_THRESHOLD = 0.6     # Spectral anomaly score threshold (0.0-1.0)
ENABLE_MFCC_VALIDATION = True        # Enable MFCC-based spectral analysis
SPECTRAL_VARIANCE_LIMIT = 100.0      # Maximum spectral variance before flagging as artifact

# --- Output Validation Settings ---
ENABLE_OUTPUT_VALIDATION = True      # Enable quality control clearinghouse (runs individual checks when enabled)
OUTPUT_VALIDATION_THRESHOLD = 0.6    # Minimum F1 score for output validation (reduced for punctuation tolerance)

# --- Parameter Adjustment for Regeneration ---
REGEN_TEMPERATURE_ADJUSTMENT = 0.1   # How much to adjust temperature per retry (increased for visibility)
REGEN_EXAGGERATION_ADJUSTMENT = 0.15 # How much to adjust exaggeration per retry (increased for visibility)
REGEN_CFG_ADJUSTMENT = 0.1           # How much to adjust cfg_weight per retry (increased for visibility)

# ============================================================================
# FEATURE TOGGLES
# ============================================================================
shutdown_requested = False           # Global shutdown flag
