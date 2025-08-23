"""
ChatterboxTTS Text Processing Module
====================================

OVERVIEW:
This module is the core text preprocessing system for ChatterboxTTS audiobook generation.
It handles intelligent text chunking, abbreviation replacement, and punctuation normalization
to prepare raw text for high-quality TTS synthesis.

MAIN COMPONENTS:
1. ABBREVIATION SYSTEM: Converts TTS-unfriendly abbreviations (Dr. -> Doctor)
2. TEXT CHUNKING: Breaks text into optimal chunks respecting sentence boundaries
3. PUNCTUATION NORMALIZATION: Standardizes quotes, adds missing periods
4. BOUNDARY DETECTION: Identifies chapter/paragraph breaks for silence insertion

CRITICAL ALGORITHM FIXES:
- Fixed sentence chunking to respect punctuation boundaries (not word counts)
- Enhanced dialogue handling to prevent quote corruption
- Improved abbreviation replacement with external file loading
- Added smart punctuation detection for precise silence timing

USAGE FLOW:
Text Input → Abbreviation Replacement → Punctuation Normalization → 
Sentence Chunking → Boundary Detection → JSON Output for TTS

PERFORMANCE IMPACT:
Proper chunking prevents TTS model confusion and maintains voice consistency
across long audiobooks by preserving natural speech boundaries.
"""

import re
import logging
from pathlib import Path
from config.config import MAX_CHUNK_WORDS, MIN_CHUNK_WORDS, YELLOW, RESET


# ============================================================================
# ABBREVIATION REPLACEMENT SYSTEM
# ============================================================================
# 
# PURPOSE: Replace TTS-unfriendly abbreviations with pronounceable text
# EXAMPLES: "Dr. Smith" -> "Doctor Smith", "U.S.A." -> "USA"
# BENEFITS: Prevents awkward pronunciation and improves audio quality

def load_abbreviations(file_path="utils/abbreviations.txt"):
    """
    Load abbreviation-to-replacement mappings from external text file.
    
    PURPOSE:
    - Centralizes abbreviation management in an editable text file
    - Allows users to customize TTS pronunciations without code changes
    - Supports comment lines and flexible formatting
    
    FILE FORMAT:
    # Comments start with #
    Dr. -> Doctor
    U.S. -> US
    etc. -> et cetera
    
    PARAMETERS:
    - file_path: Path to abbreviations file (default: utils/abbreviations.txt)
    
    RETURNS:
    - dict: Mapping of abbreviation -> replacement text
    
    BEHAVIOR:
    - Creates sample file if none exists
    - Skips malformed lines with warnings
    - Returns empty dict on file errors (graceful degradation)
    """
    replacements = {}
    abbrev_file = Path(file_path)

    if not abbrev_file.exists():
        print(f"⚠️ {YELLOW}Abbreviations file not found: {file_path}{RESET}")
        print(f"📝 Creating sample file...")
        create_sample_abbreviations_file(abbrev_file)
        return replacements

    try:
        with open(abbrev_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse "abbrev -> replacement" format
                if ' -> ' in line:
                    abbrev, replacement = line.split(' -> ', 1)
                    replacements[abbrev.strip()] = replacement.strip()
                else:
                    print(f"⚠️ Invalid format on line {line_num}: {line}")

        print(f"✅ Loaded {len(replacements)} abbreviation replacements from {file_path}")

    except Exception as e:
        print(f"❌ Error loading abbreviations: {e}")

    return replacements

def create_sample_abbreviations_file(file_path):
    """Create a sample abbreviations file with common replacements"""
    sample_content = """# Abbreviation Replacements for TTS
# Format: abbreviation -> replacement
# Lines starting with # are comments

# Common titles and abbreviations
Dr. -> Doctor
Mr. -> Mister
Mrs. -> Missus
Ms. -> Miss
Prof. -> Professor
Rev. -> Reverend
Lt. -> Lieutenant
Capt. -> Captain
Gen. -> General
Col. -> Colonel
Jr. -> Junior
Sr. -> Senior

# Political and organizations
M.P. -> MP
U.S. -> US
U.K. -> UK
U.N. -> UN
F.B.I. -> FBI
C.I.A. -> CIA
N.A.S.A. -> NASA

# Common abbreviations
etc. -> et cetera
vs. -> versus
e.g. -> for example
i.e. -> that is
Inc. -> Incorporated
Corp. -> Corporation
Ltd. -> Limited
Co. -> Company

# Numbers and ordinals
1st -> first
2nd -> second
3rd -> third
4th -> fourth
5th -> fifth
10th -> tenth
20th -> twentieth
21st -> twenty-first
30th -> thirtieth
40th -> fortieth
50th -> fiftieth
60th -> sixtieth
70th -> seventieth
80th -> eightieth
90th -> ninetieth
100th -> one hundredth

# Time abbreviations
a.m. -> AM
p.m. -> PM
A.M. -> AM
P.M. -> PM
"""

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"📝 Created sample abbreviations file: {file_path}")
        print(f"💡 Edit this file to add your own replacements!")
    except Exception as e:
        print(f"❌ Error creating sample file: {e}")

def preprocess_abbreviations(text, replacements):
    """Replace abbreviations with TTS-friendly versions"""
    if not replacements:
        return text

    original_text = text
    replacements_made = 0

    # Apply replacements (order matters for overlapping patterns)
    for abbrev, replacement in replacements.items():
        if abbrev in text:
            text = text.replace(abbrev, replacement)
            replacements_made += 1

    if replacements_made > 0:
        logging.info(f"📝 Applied {replacements_made} abbreviation replacements")

    return text

# ============================================================================
# TEXT PREPROCESSING AND CHUNKING
# ============================================================================

def smart_punctuate(text):
    """
    Enhanced punctuation normalization with abbreviation replacement.
    
    PROCESSING REQUIREMENTS:
    - Load and apply abbreviation replacements (Dr. -> Doctor, etc.)
    - Add periods to lines that don't end with punctuation
    - Replace Unicode smart quotes with ASCII quotes (", ')
    - Remove problematic formatting (bold markdown, underlines)
    - Preserve paragraph breaks (empty lines)
    
    This prepares text for consistent TTS processing.
    """

    # Load abbreviations and apply them
    abbreviation_replacements = load_abbreviations()
    text = preprocess_abbreviations(text, abbreviation_replacements)

    # Then continue with existing punctuation logic
    lines = text.splitlines()
    out = []

    for l in lines:
        stripped = l.strip()

        # Preserve empty lines (paragraph breaks)
        if not stripped:
            out.append("")  # Keep the blank line
        # Process non-empty lines
        elif not re.search(r'[.!?]$', stripped) and not re.search(r'[.!?]["\']$', stripped):
            out.append(stripped + ".")
        else:
            out.append(stripped)

    result = "\n".join(out)

    # Enhanced text preprocessing - replace curly quotes with straight quotes
    result = result.replace('\u201c', '"').replace('\u201d', '"')  # Replace smart double quotes " "
    result = result.replace('\u2018', "'").replace('\u2019', "'")  # Replace smart single quotes ' '

    # Remove problematic formatting
    result = re.sub(r'\*\*([^*]+)\*\*', r'\1', result)  # Remove bold markdown
    result = re.sub(r'_{2,}', '', result)  # Remove underlines
    
    # Fix any escaped quotes that might appear in the text
    result = result.replace('\\"', '"').replace("\\'", "'")
    
    # Additional quote normalization to prevent recurring dialogue corruption
    result = re.sub(r'(["\'])\s*,\s*(["\'])', r'\1, \2', result)  # Fix quote spacing around commas
    result = re.sub(r'(["\'])\s*\.\s*(["\'])', r'\1. \2', result)  # Fix quote spacing around periods
    result = re.sub(r'(["\'])\s*([,.])\s*(["\'])\s*([,.])', r'\1\2 \3', result)  # Remove duplicate punctuation
    
    # Debug logging for dialogue patterns
    if '"' in result and ('replied' in result or 'said' in result):
        print(f"🗣️ DEBUG: Dialogue detected in smart_punctuate: {result[:100]}...")

    return result

def fix_short_sentence_artifacts(chunk_text):
    """
    Fix multiple short sentences that cause TTS errors.
    Example: "Yes. No. Maybe." → "Yes, no, maybe."
             "Right." → "Right," (if it's a single-word chunk)
    """
    # Handle full chunk that is just one short sentence
    words = chunk_text.strip().split()
    if len(words) == 1 and chunk_text.strip().endswith('.'):
        return chunk_text.strip()[:-1] + ','  # Replace period with comma

    parts = re.split(r'([.!?])', chunk_text.strip())
    if len(parts) < 2:
        return chunk_text  # nothing to fix

    # Reconstruct sentence-punctuation pairs
    sentences = []
    for i in range(0, len(parts)-1, 2):
        sentence = parts[i].strip()
        punct = parts[i+1]
        if sentence:
            word_count = len(sentence.split())
            sentences.append((sentence, punct, word_count))

    # Handle multiple short sentences
    short_count = sum(1 for _, _, wc in sentences if wc <= 3)

    if short_count >= 2 and len(sentences) >= 2:
        merged = ", ".join(s for s, _, _ in sentences) + "."
        return merged

    # Handle case where first sentence is a single word
    if len(sentences) >= 2 and sentences[0][2] == 1 and sentences[0][1] == ".":
        # Replace period with comma
        first, second = sentences[0][0], sentences[1][0]
        rest = " ".join(s for s, _, _ in sentences[2:])
        new_text = f"{first}, {second}"
        if rest:
            new_text += " " + rest
        return new_text

    return chunk_text

def _is_apostrophe(text, pos):
    """Check if a single quote at position pos is likely an apostrophe (not speech quote)"""
    if pos == 0 or pos >= len(text) - 1:
        return False
    
    # Check characters before and after
    before = text[pos - 1] if pos > 0 else ' '
    after = text[pos + 1] if pos < len(text) - 1 else ' '
    
    # It's likely an apostrophe if:
    # 1. Preceded and followed by letters (contractions like "don't", possessives like "John's")
    # 2. Or preceded by letter and followed by 's' or 't' (common contractions)
    if before.isalpha() and after.isalpha():
        return True
    if before.isalpha() and after in 's':
        return True
    
    return False

def sentence_chunk_text(text, max_words=MAX_CHUNK_WORDS, min_words=MIN_CHUNK_WORDS):
    """
    CRITICAL CHUNKING ALGORITHM - Heart of the TTS preprocessing system
    ================================================================
    
    ALGORITHM OVERVIEW:
    This function is the most important component for TTS quality. It breaks raw text 
    into optimal chunks that respect natural speech boundaries, preventing TTS model 
    confusion and maintaining consistent voice characteristics.
    
    CORE PRINCIPLE: SENTENCE BOUNDARIES FIRST, WORD COUNTS SECOND
    - Always prioritize complete sentences over arbitrary word limits
    - Break long sentences at natural pauses (punctuation hierarchy)
    - Combine short chunks to meet minimum requirements
    - Preserve semantic coherence and emotional consistency
    
    TEXT CHUNKING RULES (in priority order):
    1. Break at sentence boundaries (. ! ?) first (HIGHEST PRIORITY)
    2. If sentence > max_words, break at punctuation working backwards
    3. If no punctuation available, preserve sentence intact (coherence over limits)
    4. Ensure all chunks meet min_words requirement by combining small chunks
    
    PUNCTUATION HIERARCHY (for breaking overlong sentences):
    1. . ! ? (sentence boundaries) - handled at sentence level first
    2. ; (semicolon) - major pause, good break point
    3. — – (em/en dashes) - major pause, narrative breaks
    4. , (comma) - minor pause, last resort for breaks
    5. NO PUNCTUATION = preserve intact (maintains emotional/semantic unity)
    
    WHY THIS APPROACH:
    - Prevents choppy, robotic speech from mid-sentence breaks
    - Maintains narrative flow and character voice consistency  
    - Respects author's punctuation for natural pauses
    - Reduces TTS model confusion from incomplete thoughts
    - Essential for long-form audiobook quality
    
    PARAMETERS:
    - text: Raw input text to be chunked
    - max_words: Target maximum words per chunk (flexible for complete sentences)
    - min_words: Minimum words per chunk (enforced by combining)
    
    RETURNS:
    - List of (chunk_text, is_paragraph_end) tuples for TTS processing
    """
    import re
    
    # Process text paragraph by paragraph to preserve structure
    paragraphs = text.split('\n\n')
    all_final_chunks = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Check if this is a chapter/section header
        para_lower = paragraph.lower().strip()
        is_chapter_header = (
            any(word in para_lower for word in ['chapter', 'section', 'part', 'prologue', 'epilogue']) and
            len(paragraph.split()) <= 10
        )
        
        if is_chapter_header:
            # Chapter headers are their own chunks and always paragraph ends
            all_final_chunks.append((paragraph, True))
            continue
        
        # Split into sentences using periods, exclamation marks, question marks
        # This avoids the complex quote detection that was causing problems
        sentences = re.split(r'([.!?])\s+', paragraph.strip())
        
        # Reconstruct sentences with their punctuation
        reconstructed_sentences = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i].strip()
            if i + 1 < len(sentences):
                punct = sentences[i + 1]
                sentence += punct
            if sentence:
                reconstructed_sentences.append(sentence)
        
        # Handle any remaining text (no ending punctuation)
        if sentences and sentences[-1].strip():
            last_part = sentences[-1].strip()
            if last_part and not last_part in '.!?':
                reconstructed_sentences.append(last_part)
        
        # Process each sentence
        paragraph_chunks = []
        for sent_idx, sentence in enumerate(reconstructed_sentences):
            is_last_sentence = (sent_idx == len(reconstructed_sentences) - 1)
            words = sentence.split()
            
            if len(words) <= max_words:
                # Sentence fits, use as-is
                paragraph_chunks.append((sentence.strip(), is_last_sentence))
            else:
                # Sentence too long, break it using punctuation
                broken_chunks = _break_long_sentence_simple(sentence, max_words)
                # Only mark the last broken chunk as sentence end
                for i, chunk in enumerate(broken_chunks):
                    is_chunk_end = (is_last_sentence and i == len(broken_chunks) - 1)
                    paragraph_chunks.append((chunk.strip(), is_chunk_end))
        
        all_final_chunks.extend(paragraph_chunks)
    
    # Combine small chunks that don't meet min_words requirement
    combined_chunks = _combine_small_chunks(all_final_chunks, min_words, max_words)
    
    return combined_chunks

def _break_long_sentence_simple(sentence, max_words):
    """Break a long sentence at punctuation marks, working backwards"""
    import re
    
    # Punctuation patterns in priority order
    patterns = [
        r';\s*',      # semicolon + optional space
        r'—\s*',      # em dash + optional space  
        r'–\s*',      # en dash + optional space
        r',\s*',      # comma + optional space
    ]
    
    chunks = []
    remaining = sentence.strip()
    
    while remaining:
        words = remaining.split()
        if len(words) <= max_words:
            chunks.append(remaining)
            break
        
        # Find best break point working backwards
        best_break = -1
        
        # Try each punctuation pattern
        for pattern in patterns:
            matches = list(re.finditer(pattern, remaining))
            if matches:
                # Find rightmost match that results in chunk <= max_words
                for match in reversed(matches):
                    test_chunk = remaining[:match.end()].strip()
                    if len(test_chunk.split()) <= max_words:
                        best_break = match.end()
                        break
                if best_break != -1:
                    break
        
        if best_break != -1:
            # Found good break point
            chunk = remaining[:best_break].strip()
            chunks.append(chunk)
            remaining = remaining[best_break:].strip()
        else:
            # No punctuation found - preserve sentence coherence by keeping it intact
            # This prevents splitting sentences with potentially different sentiment
            chunks.append(remaining)
            break
    
    return chunks

def _combine_small_chunks(chunks, min_words, max_words):
    """Combine chunks that are too small"""
    combined = []
    current_chunk = ""
    current_is_para_end = False
    
    for chunk_text, is_para_end in chunks:
        chunk_words = len(chunk_text.split())
        current_words = len(current_chunk.split()) if current_chunk else 0
        
        if not current_chunk:
            # First chunk
            current_chunk = chunk_text
            current_is_para_end = is_para_end
        elif current_words + chunk_words <= max_words:
            # Can combine
            current_chunk = current_chunk + " " + chunk_text
            current_is_para_end = is_para_end  # Use the latest para_end flag
        else:
            # Can't combine, flush current and start new
            if current_words >= min_words:
                combined.append((current_chunk, current_is_para_end))
                current_chunk = chunk_text
                current_is_para_end = is_para_end
            else:
                # Current chunk too small, force combine anyway
                current_chunk = current_chunk + " " + chunk_text
                current_is_para_end = is_para_end
    
    # Handle remaining chunk
    if current_chunk:
        combined.append((current_chunk, current_is_para_end))
    
    return combined

def break_long_sentence_backwards(sentence, max_words, min_words):
    """
    Break a long sentence working backwards from the end to find natural punctuation.
    
    ALGORITHM:
    1. Start from sentence end, work backwards to find punctuation within max_words
    2. Break at the latest (rightmost) punctuation that keeps chunk <= max_words
    3. This preserves natural pauses and speech rhythm
    4. Continue processing remaining text normally
    
    PUNCTUATION HIERARCHY (in order of preference):
    1. . ! ? (sentence boundaries) - highest priority
    2. ; (semicolon) - major pause
    3. — (em dash) - major pause  
    4. , (comma) - minor pause
    5. Force break at word limit (last resort)
    """
    
    # Punctuation patterns to search for (in order of preference)
    punctuation_patterns = [
        r'[.!?]\s+',  # sentence boundaries + required space (highest priority)
        r';\s*',      # semicolon + optional space
        r'—\s*',      # em dash + optional space
        r'–\s*',      # en dash + optional space
        r',\s*',      # comma + optional space
    ]
    
    chunks = []
    remaining_text = sentence.strip()
    
    while remaining_text:
        words = remaining_text.split()
        
        if len(words) <= max_words:
            # Remaining text fits within limit
            chunks.append(remaining_text.strip())
            break
            
        # Text exceeds max_words - find backwards break point
        # Search for punctuation within the current 'remaining_text' up to max_words
        # We need to find the *last* punctuation mark that results in a chunk <= max_words
        best_break_index = -1 # Index in 'words' list
        best_break_pos_in_text = -1 # Character position in 'remaining_text'

        # Iterate backwards from max_words down to min_words (or 1 if min_words is very small)
        # to find the latest punctuation that keeps the chunk within limits.
        for i in range(min(max_words, len(words)) -1, 0, -1):
            sub_text = " ".join(words[:i+1]) # Text up to current word
            
            found_punctuation = False
            for pattern in punctuation_patterns:
                matches = list(re.finditer(pattern, sub_text))
                if matches:
                    # Take the rightmost match in this sub_text
                    last_match = matches[-1]
                    # Ensure the break is within the max_words limit
                    if len(sub_text[:last_match.end()].split()) <= max_words:
                        best_break_index = i # Store word index
                        best_break_pos_in_text = last_match.end() # Store char position
                        found_punctuation = True
                        break # Found a good break for this sub_text, move to next i
            if found_punctuation:
                break # Found the best break for the overall chunk, exit outer loop

        if best_break_pos_in_text != -1:
            # Found punctuation - break after it, keeping punctuation with preceding text
            chunk_text = remaining_text[:best_break_pos_in_text].strip()
            chunks.append(chunk_text)
            remaining_text = remaining_text[best_break_pos_in_text:].strip()
        else:
            # No punctuation found within the desired range - keep sentence intact
            # This preserves sentence coherence over word count limits
            chunks.append(remaining_text.strip())
            break
    
    return chunks

# ============================================================================
# CONTENT BOUNDARY DETECTION
# ============================================================================

def detect_punctuation_boundary(chunk_text):
    """
    Detect the ending punctuation of a text chunk for precise silence insertion.
    
    Returns specific punctuation boundary types:
    - "comma" -> Brief pause after commas
    - "semicolon" -> Medium pause after semicolons  
    - "colon" -> Pause after colons
    - "period" -> Sentence end pause
    - "question_mark" -> Question pause
    - "exclamation" -> Exclamation pause
    - "dash" -> Em dash pause
    - "ellipsis" -> Ellipsis pause (suspense)
    - "quote_end" -> End of quoted speech
    - None -> No specific punctuation detected
    """
    # Strip whitespace and newlines for accurate detection
    text = chunk_text.strip()
    
    if not text:
        return None
    
    # Check ending punctuation patterns (in order of specificity)
    if text.endswith('...'):
        return "ellipsis"
    elif text.endswith('"') or text.endswith("'"):
        return "quote_end"
    elif text.endswith('!'):
        return "exclamation"
    elif text.endswith('?'):
        return "question_mark"
    elif text.endswith('.'):
        return "period"
    elif text.endswith(':'):
        return "colon"
    elif text.endswith(';'):
        return "semicolon"
    elif text.endswith(','):
        return "comma"
    elif text.endswith('—') or text.endswith('–'):
        return "dash"
    
    return None

def detect_content_boundaries(chunk_text, chunk_index, all_chunks, is_paragraph_end=False):
    """
    Detect chapter breaks and paragraph endings for appropriate silence insertion.
    Now enhanced with punctuation-specific boundary detection.
    
    BOUNDARY DETECTION REQUIREMENTS:
    - Chapter start: "Chapter N", "Ch. N", "I.", "1." patterns
    - Chapter end: Next chunk is a chapter start
    - Section break: Multiple asterisks, hashes, or em-dashes
    - Paragraph end: Detected via chunking process flag or content analysis
    - Punctuation: Specific ending punctuation for precise silence timing
    
    Returns boundary_type for silence insertion:
    - "chapter_start" -> Long pause before chapter
    - "chapter_end" -> Long pause after chapter
    - "section_break" -> Medium pause for section breaks  
    - "paragraph_end" -> Short pause for paragraph breaks
    - Punctuation types: "comma", "period", "question_mark", etc.
    - None -> No special boundary detected
    """
    boundary_type = None

    # Chapter detection (flexible patterns)
    chapter_patterns = [
        r'^(Chapter \d+|CHAPTER \d+)',
        r'^(Ch\. \d+|CH\. \d+)',
        r'^\d+\.',  # Simple "1." numbering
        r'^[IVX]+\.',  # Roman numerals "I.", "II.", etc.
    ]

    for pattern in chapter_patterns:
        if re.search(pattern, chunk_text.strip(), re.MULTILINE):
            boundary_type = "chapter_start"
            break

    # Look ahead for chapter start (current chunk ends chapter)
    if chunk_index + 1 < len(all_chunks):
        next_chunk = all_chunks[chunk_index + 1]
        for pattern in chapter_patterns:
            if re.search(pattern, next_chunk.strip()):
                boundary_type = "chapter_end"
                break

    # Section breaks (asterisks, multiple line breaks)
    if re.search(r'\*{3,}|\#{3,}|—{3,}', chunk_text):
        boundary_type = "section_break"

    # Paragraph ending detection
    # Use the is_paragraph_end flag from chunking process since newlines are stripped
    if is_paragraph_end and boundary_type is None:
        boundary_type = "paragraph_end"

    # If no major structural boundary found, check punctuation
    if boundary_type is None:
        boundary_type = detect_punctuation_boundary(chunk_text)

    return boundary_type

def _split_long_dialogue(sentence, max_words, recursion_depth=0):
    """
    Split long dialogue sections that exceed word limits.
    Tries to break at natural points: attribution, internal punctuation, then word boundaries.
    """
    # Prevent infinite recursion
    if recursion_depth > 3:
        # Force word boundary split if recursion gets too deep
        words = sentence.split()
        sentences = []
        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunk_words = words[start:end]
            sentences.append(' '.join(chunk_words))
            start = end
        return sentences
    
    words = sentence.split()
    if len(words) <= max_words:
        return [sentence]
    
    sentences = []
    
    # Strategy 1: Break at dialogue attribution (he said, she replied, etc.)
    attribution_pattern = r'(\s+(?:he|she|I|they|[A-Z][a-z]+)\s+(?:said|replied|asked|shouted|whispered|continued|added|interrupted)[^.!?]*?[.!?]?\s*)'
    attribution_matches = list(re.finditer(attribution_pattern, sentence, re.IGNORECASE))
    
    if attribution_matches:
        start = 0
        for match in attribution_matches:
            # Check if breaking here keeps chunks under limit
            before_attr = sentence[start:match.end()].strip()
            if before_attr and len(before_attr.split()) <= max_words:
                sentences.append(before_attr)
                start = match.end()
        
        # Add remaining text
        if start < len(sentence):
            remaining = sentence[start:].strip()
            if remaining:
                if len(remaining.split()) > max_words:
                    # Recursively split if still too long, but with depth tracking
                    sentences.extend(_split_long_dialogue(remaining, max_words, recursion_depth + 1))
                else:
                    sentences.append(remaining)
        
        if sentences:  # If we successfully split, return result
            return sentences
    
    # Strategy 2: Break at internal punctuation (commas, semicolons within quotes)
    punct_pattern = r'([,;:]\s+)'
    parts = re.split(punct_pattern, sentence)
    
    current_chunk = ""
    sentences = []
    for i, part in enumerate(parts):
        test_chunk = current_chunk + part
        if len(test_chunk.split()) > max_words and current_chunk:
            sentences.append(current_chunk.strip())
            current_chunk = part
        else:
            current_chunk = test_chunk
    
    if current_chunk.strip():
        sentences.append(current_chunk.strip())
    
    # Check if any resulting chunk is still too long and needs further splitting
    final_sentences = []
    for chunk in sentences:
        if len(chunk.split()) > max_words:
            # Split oversized chunks using word boundaries
            chunk_words = chunk.split()
            start = 0
            while start < len(chunk_words):
                end = min(start + max_words, len(chunk_words))
                sub_chunk_words = chunk_words[start:end]
                final_sentences.append(' '.join(sub_chunk_words))
                start = end
        else:
            final_sentences.append(chunk)
    
    if len(final_sentences) > 1:  # If we successfully split, return result
        return final_sentences
    
    # Strategy 3: Force break at word boundaries (guaranteed to work)
    sentences = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunk_words = words[start:end]
        sentences.append(' '.join(chunk_words))
        start = end
    
    return sentences

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def reload_abbreviations():
    """Reload abbreviations from file (useful for testing changes)"""
    return load_abbreviations()

def test_abbreviations(test_text="Dr. Smith met with the M.P. at 3:30 p.m. on the 21st."):
    """Test abbreviation replacements on sample text"""
    abbreviation_replacements = load_abbreviations()
    print(f"Original: {test_text}")
    processed = preprocess_abbreviations(test_text, abbreviation_replacements)
    print(f"Processed: {processed}")
    return processed

def test_chunking(test_text=None, max_words=20, min_words=4):
    """Test the enhanced chunking with sample or custom text"""
    if test_text is None:
        test_text = '''Though perfectly worldly-wise, and able, as she expressed it, to take care of herself, there was yet something curiously ingenuous in her single-minded attitude towards life, and her whole-hearted determination to "make good." This glimpse of a world unknown to me was not without its charm, and I enjoyed seeing her vivid little face light up as she talked.'''

    chunks = sentence_chunk_text(test_text, max_words=max_words, min_words=min_words)

    print("Enhanced Chunking Results:")
    for i, (chunk, is_para) in enumerate(chunks):
        word_count = len(chunk.split())
        print(f"Chunk {i+1} ({word_count} words): {chunk}")
        if word_count > max_words:
            print(f"  ✅ Over {max_words} words but complete sentence (follows punctuation rules)")
        print()

    return chunks
