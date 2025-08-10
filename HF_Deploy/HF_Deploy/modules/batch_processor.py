"""
Batch Processing Module
Handles multi-book batch processing operations
"""

import torch
from modules.tts_engine import process_book_folder

def pipeline_book_processing(book_queue):
    """Process multiple books in sequence"""
    completed_books = []
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    for book_info in book_queue:
        book_dir = book_info['book_dir']
        voice_path = book_info['voice_path'] 
        tts_params = book_info['tts_params']
        
        print(f"\n🎯 Processing: {book_dir.name}")
        
        try:
            result = process_book_folder(book_dir, voice_path, tts_params, device)
            if result[0]:  # Check if final_m4b_path exists
                completed_books.append(book_info)
                print(f"✅ Completed: {book_dir.name}")
            else:
                print(f"❌ Failed: {book_dir.name}")
        except Exception as e:
            print(f"❌ Error processing {book_dir.name}: {e}")
    
    return completed_books