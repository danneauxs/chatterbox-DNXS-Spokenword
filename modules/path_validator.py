"""
Path Validation Module
Validates and suggests safe alternatives for problematic file paths
"""

import re
from pathlib import Path
from typing import Tuple, List

def detect_problematic_characters(path_name: str) -> List[str]:
    """Detect problematic characters in a path name"""
    problematic_chars = []
    
    # Characters that cause FFmpeg issues
    if "'" in path_name:
        problematic_chars.append("apostrophe (')")
    
    # Characters that may cause filesystem issues
    if '"' in path_name:
        problematic_chars.append('double quote (")')
    
    # Other potentially problematic characters
    problematic_patterns = {
        r'[<>|?*]': 'invalid filesystem characters',
        r'[\x00-\x1f]': 'control characters',
        r'\\': 'backslashes (Windows path separators)',
    }
    
    for pattern, description in problematic_patterns.items():
        if re.search(pattern, path_name):
            problematic_chars.append(description)
    
    return problematic_chars

def suggest_safe_path(path_name: str) -> str:
    """Suggest a safe alternative for a problematic path name"""
    from modules.file_manager import sanitize_filename
    return sanitize_filename(path_name)

def validate_book_path(book_name: str) -> Tuple[bool, str, str]:
    """
    Validate a book name for path safety
    
    Returns:
        (is_safe, warning_message, suggested_name)
    """
    problematic_chars = detect_problematic_characters(book_name)
    
    if not problematic_chars:
        return True, "", book_name
    
    suggested_name = suggest_safe_path(book_name)
    
    # Create warning message
    char_list = ", ".join(problematic_chars)
    warning_msg = f"⚠️ Path contains problematic characters: {char_list}\n\n"
    warning_msg += f"This may cause:\n"
    warning_msg += f"• FFmpeg concatenation failures\n"
    warning_msg += f"• File system compatibility issues\n"
    warning_msg += f"• Audio processing errors\n\n"
    warning_msg += f"Suggested safe name: '{suggested_name}'"
    
    return False, warning_msg, suggested_name

def validate_and_create_audiobook_path(book_name: str, force_safe: bool = False) -> Tuple[Path, str]:
    """
    Validate book name and create safe audiobook path
    
    Args:
        book_name: Original book name from user input
        force_safe: If True, automatically use safe name without asking
        
    Returns:
        (safe_audiobook_path, actual_name_used)
    """
    from config.config import AUDIOBOOK_ROOT
    
    is_safe, warning, suggested_name = validate_book_path(book_name)
    
    if is_safe or force_safe:
        final_name = suggested_name if force_safe and not is_safe else book_name
        audiobook_path = AUDIOBOOK_ROOT / final_name
        return audiobook_path, final_name
    else:
        # Return suggested path but indicate validation failed
        suggested_path = AUDIOBOOK_ROOT / suggested_name
        return suggested_path, suggested_name

def check_existing_audiobook_paths() -> List[Tuple[str, str, str]]:
    """
    Check existing audiobook directories for problematic paths
    
    Returns:
        List of (original_name, suggested_name, issues) tuples
    """
    from config.config import AUDIOBOOK_ROOT
    
    problematic_books = []
    
    if not AUDIOBOOK_ROOT.exists():
        return problematic_books
    
    for book_dir in AUDIOBOOK_ROOT.iterdir():
        if book_dir.is_dir():
            book_name = book_dir.name
            problematic_chars = detect_problematic_characters(book_name)
            
            if problematic_chars:
                suggested_name = suggest_safe_path(book_name)
                issues = ", ".join(problematic_chars)
                problematic_books.append((book_name, suggested_name, issues))
    
    return problematic_books

# Utility functions for GUI integration
def format_path_warning_html(book_name: str) -> str:
    """Format path validation warning as HTML for Gradio"""
    is_safe, warning, suggested = validate_book_path(book_name)
    
    if is_safe:
        return f'<span style="color: green;">✅ Path is safe: "{book_name}"</span>'
    else:
        html = f'<div style="color: orange; background: #fff3cd; padding: 10px; border-radius: 5px; border: 1px solid #ffeaa7;">'
        html += f'<strong>⚠️ Problematic Path Detected</strong><br>'
        html += f'<strong>Original:</strong> "{book_name}"<br>'
        html += f'<strong>Suggested:</strong> "{suggested}"<br><br>'
        html += f'<strong>Issues Found:</strong><br>'
        
        for char in detect_problematic_characters(book_name):
            html += f'• {char}<br>'
        
        html += f'<br><em>Tip: Use the suggested name to avoid audio processing errors.</em>'
        html += f'</div>'
        return html

def format_path_warning_text(book_name: str) -> str:
    """Format path validation warning as plain text"""
    is_safe, warning, suggested = validate_book_path(book_name)
    
    if is_safe:
        return f'✅ Path is safe: "{book_name}"'
    else:
        return f'⚠️ PROBLEMATIC PATH: "{book_name}"\nSUGGESTED: "{suggested}"\n\n{warning}'