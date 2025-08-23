#!/usr/bin/env python3
"""
Path Checker Tool
Scans existing audiobook directories for problematic paths
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from modules.path_validator import check_existing_audiobook_paths, format_path_warning_text
from config.config import AUDIOBOOK_ROOT

def main():
    print("🔍 Scanning audiobook directories for problematic paths...")
    print(f"📁 Audiobook root: {AUDIOBOOK_ROOT}")
    print("=" * 60)
    
    problematic_books = check_existing_audiobook_paths()
    
    if not problematic_books:
        print("✅ All audiobook directories have safe paths!")
        return
    
    print(f"⚠️  Found {len(problematic_books)} directories with problematic paths:\n")
    
    for i, (original, suggested, issues) in enumerate(problematic_books, 1):
        print(f"{i}. PROBLEMATIC: \"{original}\"")
        print(f"   SUGGESTED:   \"{suggested}\"")
        print(f"   ISSUES:      {issues}")
        print()
    
    print("=" * 60)
    print("🛠️  RECOMMENDED ACTIONS:")
    print()
    print("Option 1: Rename directories manually")
    for original, suggested, _ in problematic_books:
        print(f"   mv \"Audiobook/{original}\" \"Audiobook/{suggested}\"")
    
    print()
    print("Option 2: Use the GUI with new books")
    print("   - Create new book folders with safe names")
    print("   - Copy content from old folders")
    print("   - Delete old problematic folders")
    
    print()
    print("Option 3: Force-fix paths (advanced)")
    print("   - The system will automatically sanitize paths during processing")
    print("   - Existing problematic directories may still cause issues")

if __name__ == "__main__":
    main()