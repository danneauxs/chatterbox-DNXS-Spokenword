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

        # Dialogue-aware sentence splitting with word limit protection
        sentences = []
        
        # First pass: find natural sentence boundaries outside quotes
        sentence_boundaries = []
        in_quotes = False
        quote_char = None
        
        for i, char in enumerate(paragraph):
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
            elif char in '.!?' and not in_quotes:
                # Check if this is followed by whitespace or end of string
                if i + 1 >= len(paragraph) or paragraph[i + 1:i + 2].isspace():
                    sentence_boundaries.append(i + 1)
        
        # Split at natural boundaries first
        start = 0
        for boundary in sentence_boundaries:
            sentence = paragraph[start:boundary].strip()
            if sentence:
                # Always check if sentence needs splitting regardless of length
                # This ensures long sentences are properly handled
                if len(sentence.split()) > max_words:
                    sub_sentences = _split_long_dialogue(sentence, max_words)
                    sentences.extend(sub_sentences)
                else:
                    sentences.append(sentence)
            start = boundary
        
        # Handle any remaining text
        if start < len(paragraph):
            remaining = paragraph[start:].strip()
            if remaining:
                if len(remaining.split()) > max_words:
                    sub_sentences = _split_long_dialogue(remaining, max_words)
                    sentences.extend(sub_sentences)
                else:
                    sentences.append(remaining)

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

    final_chunks = []
    current_chunk_parts = []
    current_chunk_is_para_end = False

    for i, (sentence_text, is_sentence_para_end) in enumerate(all_processed_chunks):
        sentence_word_count = len(sentence_text.split())

        is_chapter_header = (
            any(word in sentence_text.lower() for word in ['chapter', 'section', 'part', 'prologue', 'epilogue']) and
            sentence_word_count <= 10
        )

        # If it's a chapter header, flush current buffer and add it as a standalone chunk
        if is_chapter_header:
            if current_chunk_parts:
                combined_text = " ".join(current_chunk_parts)
                final_chunks.append((combined_text, current_chunk_is_para_end))
                current_chunk_parts = []
                current_chunk_is_para_end = False
            final_chunks.append((sentence_text, True)) # Chapter headers are always paragraph ends
            continue

        # Calculate word count if we add this sentence to the current buffer
        current_word_count = sum(len(p.split()) for p in current_chunk_parts)
        potential_word_count_with_new_sentence = current_word_count + sentence_word_count

        # Condition to flush the current chunk (without the new sentence)
        # This happens if adding the new sentence would make the current chunk too long
        if current_chunk_parts and potential_word_count_with_new_sentence > max_words:
            combined_text = " ".join(current_chunk_parts)
            final_chunks.append((combined_text, current_chunk_is_para_end))
            current_chunk_parts = []
            current_chunk_is_para_end = False # Reset for the new chunk

        # Add the current sentence to the buffer
        current_chunk_parts.append(sentence_text)
        if is_sentence_para_end:
            current_chunk_is_para_end = True

        # Now, after adding the current sentence, check if we should flush the *newly formed* current_chunk_parts
        # This happens if it's a paragraph end AND the current chunk meets min_words
        # Or if it's the very last sentence and the chunk meets min_words (handled by final flush)
        if is_sentence_para_end and sum(len(p.split()) for p in current_chunk_parts) >= min_words:
            combined_text = " ".join(current_chunk_parts)
            final_chunks.append((combined_text, current_chunk_is_para_end))
            current_chunk_parts = []
            current_chunk_is_para_end = False

    # After the loop, handle any remaining content in the buffer
    if current_chunk_parts:
        combined_text = " ".join(current_chunk_parts)
        # The very last chunk of the text is always considered a paragraph end
        final_chunks.append((combined_text, True))

    # Apply short sentence cleanup (this function might need review too)
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
    4. Force break at word limit (last resort)
    """
    
    # Punctuation patterns to search for (in order of preference)
    punctuation_patterns = [
        r';\s*',     # semicolon + optional space
        r'—\s*',     # em dash + optional space
        r'–\s*',     # en dash + optional space
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
