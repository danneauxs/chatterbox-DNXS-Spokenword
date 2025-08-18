"""
Text Processing Module
Handles text chunking, abbreviations, and preprocessing for TTS
"""

import re
import logging
from pathlib import Path
from config.config import MAX_CHUNK_WORDS, MIN_CHUNK_WORDS, YELLOW, RESET



# ============================================================================
# ABBREVIATION REPLACEMENT SYSTEM
# ============================================================================

def load_abbreviations(file_path="utils/abbreviations.txt"):
    """Load abbreviation replacements from external file"""
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
        elif not re.search(r'[.!?]$', stripped):
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

def sentence_chunk_text(text, max_words=MAX_CHUNK_WORDS, min_words=MIN_CHUNK_WORDS):
    """
    Enhanced sentence chunking that respects paragraph boundaries and punctuation rules.
    
    TEXT CHUNKING RULES:
    Text will be chunked by sentence, adhering to the following criteria:
    
    1. Chunks must contain a minimum of 4 words, even if this means merging very short sentences.
    2. Chunks must not exceed 30 words.
    3. For sentences longer than 30 words, the chunk will be truncated at the most recent 
       punctuation mark (e.g., comma, semicolon) that falls within the 1-29 word range, 
       effectively breaking the sentence there.
    
    TECHNICAL IMPLEMENTATION:
    - Minimum 4 words per chunk (configurable via min_words)
    - Maximum 30 words per chunk (configurable via max_words)
    - Break at sentence endings (.!?) when possible
    - For sentences > max_words: work backwards from sentence end to find punctuation
    - Break AFTER punctuation (comma, semicolon, etc.) even if chunk < max_words
    - CRITICAL: Punctuation stays WITH PRECEDING TEXT for proper TTS pause timing
    - Example: "...failed," | "so she..." NOT "...failed" | ", so she..."
    - This preserves natural pauses and speech rhythm for TTS processing
    - Resume chunking from break point and continue normally
    
    PUNCTUATION HIERARCHY (for breaking long sentences):
    1. Period, exclamation, question mark (sentence boundaries)
    2. Semicolon, em-dash (major pauses)  
    3. Comma (minor pauses)
    4. Force break at word limit (last resort)
    """

    # Process text paragraph by paragraph to preserve structure
    paragraphs = text.split('\n\n')
    all_processed_chunks = []
    
    for para_idx, paragraph in enumerate(paragraphs):
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
            all_processed_chunks.append((paragraph, True))
            continue

        # Split paragraph into sentences
        sentence_end_re = re.compile(r'([.!?][\"\'\)]*\s+)')
        sentences = []
        start_index = 0

        for match in sentence_end_re.finditer(paragraph):
            end_index = match.end()
            sentence = paragraph[start_index:end_index].strip()
            if sentence:
                sentences.append(sentence)
            start_index = end_index

        if start_index < len(paragraph):
            remainder = paragraph[start_index:].strip()
            if remainder:
                sentences.append(remainder)

        # Process sentences within this paragraph
        paragraph_chunks = []
        
        for sent_idx, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if sentence exceeds word limit
            sentence_words = sentence.split()
            is_last_sentence_in_para = (sent_idx == len(sentences) - 1)

            if len(sentence_words) <= max_words:
                # Sentence fits within limit - use as-is
                paragraph_chunks.append((sentence, is_last_sentence_in_para))
            else:
                # Sentence exceeds max_words - break at natural punctuation working backwards
                broken_chunks = break_long_sentence_backwards(sentence, max_words, min_words)
                # Only the last broken chunk gets paragraph end marking if it's the last sentence
                for i, chunk_text in enumerate(broken_chunks):
                    is_chunk_para_end = (is_last_sentence_in_para and i == len(broken_chunks) - 1)
                    paragraph_chunks.append((chunk_text, is_chunk_para_end))
        
        # Add this paragraph's chunks to the overall list
        all_processed_chunks.extend(paragraph_chunks)

    # Respect punctuation rules: combine complete sentences only, never break mid-sentence
    final_chunks = []
    accumulator = []
    accumulator_word_count = 0

    for chunk_text, is_para_end in all_processed_chunks:
        word_count = len(chunk_text.split())
        
        # If this complete sentence would fit within limits when combined
        if accumulator_word_count + word_count <= max_words and not is_para_end:
            accumulator.append(chunk_text)
            accumulator_word_count += word_count
        else:
            # Flush accumulator if it has content
            if accumulator:
                # Join complete sentences with spaces (preserving original punctuation)
                combined = " ".join(accumulator)
                final_chunks.append((combined, False))
                accumulator = []
                accumulator_word_count = 0
            
            # Add current chunk
            if word_count >= min_words or is_para_end:
                # Chunk meets minimum or is paragraph end - use as-is  
                final_chunks.append((chunk_text, is_para_end))
            else:
                # Start new accumulator with this short complete sentence
                accumulator = [chunk_text]
                accumulator_word_count = word_count

    # Handle any remaining accumulator
    if accumulator:
        combined = " ".join(accumulator)
        final_chunks.append((combined, True))  # Mark as paragraph end

    # Apply short sentence cleanup
    fixed_chunks = []
    for chunk_text, is_para_end in final_chunks:
        fixed_text = fix_short_sentence_artifacts(chunk_text)
        fixed_chunks.append((fixed_text, is_para_end))

    return fixed_chunks

def break_long_sentence_backwards(sentence, max_words, min_words):
    """
    Break a long sentence working backwards from the end to find natural punctuation.
    
    ALGORITHM:
    1. Start from sentence end, work backwards to find punctuation within max_words
    2. Break at the latest (rightmost) punctuation that keeps chunk <= max_words
    3. This preserves natural pauses and speech rhythm
    4. Continue processing remaining text normally
    
    PUNCTUATION HIERARCHY (in order of preference):
    1. ; (semicolon) - major pause
    2. — (em dash) - major pause  
    3. , (comma) - minor pause
    4. Force break at max_words (last resort)
    """
    
    # Punctuation patterns to search for (in order of preference)
    punctuation_patterns = [
        r';\s*',     # semicolon + optional space
        r'—\s*',     # em dash + optional space  
        r',\s*',     # comma + optional space
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
        # Start from max_words position and work backwards
        test_words = words[:max_words]
        test_text = " ".join(test_words)
        
        best_break_pos = None
        best_break_pattern = None
        
        # Try each punctuation pattern, working backwards from end
        for pattern in punctuation_patterns:
            # Find all matches of this pattern in the test text
            matches = list(re.finditer(pattern, test_text))
            if matches:
                # Take the rightmost (latest) match - this preserves most content
                last_match = matches[-1]
                best_break_pos = last_match.end()
                best_break_pattern = pattern
                break
        
        if best_break_pos:
            # Found punctuation - break after it, keeping punctuation with preceding text
            chunk_text = test_text[:best_break_pos].strip()
            chunks.append(chunk_text)
            
            # Resume from after the punctuation (skip the punctuation character)
            remaining_text = test_text[best_break_pos:].strip()
        else:
            # No punctuation found - force break at max_words
            chunk_text = " ".join(words[:max_words])
            chunks.append(chunk_text)
            remaining_text = " ".join(words[max_words:]).strip()
    
    return chunks

# ============================================================================
# CONTENT BOUNDARY DETECTION
# ============================================================================

def detect_content_boundaries(chunk_text, chunk_index, all_chunks):
    """
    Detect chapter breaks and paragraph endings for appropriate silence insertion.
    
    BOUNDARY DETECTION REQUIREMENTS:
    - Chapter start: "Chapter N", "Ch. N", "I.", "1." patterns
    - Chapter end: Next chunk is a chapter start
    - Section break: Multiple asterisks, hashes, or em-dashes
    - Paragraph end: Text ends with newlines or is marked as paragraph boundary
    
    Returns boundary_type for silence insertion:
    - "chapter_start" -> Long pause before chapter
    - "chapter_end" -> Long pause after chapter
    - "section_break" -> Medium pause for section breaks  
    - "paragraph_end" -> Short pause for paragraph breaks
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

    # Paragraph ending (already detected in chunking)
    if chunk_text.endswith('\n\n') or chunk_text.endswith('\n'):
        if boundary_type is None:
            boundary_type = "paragraph_end"

    return boundary_type

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
