from wrapper.chunk_loader import load_chunks, save_chunks
from wrapper.chunk_search import search_chunks
from wrapper.chunk_editor import update_chunk
from wrapper.chunk_player import play_chunk_audio
from wrapper.chunk_synthesizer import synthesize_chunk
from wrapper.chunk_revisions import accept_revision
import os
from config.config import AUDIOBOOK_ROOT
AUDIO_DIR = AUDIOBOOK_ROOT

def select_book_for_repair():
    """Let user select which book to repair"""
    from pathlib import Path
    
    # Look for books in both locations: TTS processing dirs and Text_Input
    available_books = []
    
    # First check TTS processing directories
    audiobook_root = Path(AUDIOBOOK_ROOT)
    if audiobook_root.exists():
        for book_dir in audiobook_root.iterdir():
            if book_dir.is_dir():
                tts_chunks_dir = book_dir / "TTS" / "text_chunks"
                json_path = tts_chunks_dir / "chunks_info.json"
                if json_path.exists():
                    available_books.append((book_dir.name, json_path, "TTS"))
    
    # Then check Text_Input directory for fallback
    text_input_dir = Path("Text_Input")
    if text_input_dir.exists():
        for chunk_file in text_input_dir.glob("*_chunks.json"):
            book_name = chunk_file.stem.replace("_chunks", "")
            # Only add if not already found in TTS directories
            if not any(book[0] == book_name for book in available_books):
                available_books.append((book_name, chunk_file, "Text_Input"))
    
    if not available_books:
        print("❌ No chunk files found in TTS processing directories or Text_Input/")
        return None, None
    
    print("\n📚 Available books for repair:")
    for i, (book_name, json_path, source) in enumerate(available_books):
        print(f"  [{i}] {book_name} ({source}: {json_path.name})")
    
    while True:
        try:
            choice = input(f"\nSelect book index [0-{len(available_books)-1}]: ").strip()
            idx = int(choice)
            if 0 <= idx < len(available_books):
                book_name, json_path, source = available_books[idx]
                return book_name, json_path
            else:
                print(f"❌ Please enter a number between 0 and {len(available_books)-1}")
        except (ValueError, EOFError, KeyboardInterrupt):
            print("❌ Invalid selection or cancelled")
            return None, None

def run_chunk_repair_tool():
    print("\n🛠️ Chunk Repair & Revision Tool")
    
    # Ask user to select book
    book_name, chunk_path = select_book_for_repair()
    if not chunk_path:
        return
    
    print(f"\n📖 Loading chunks from: {chunk_path.name}")
    chunks = load_chunks(str(chunk_path))
    
    # Determine audio directory path based on book structure
    from pathlib import Path
    audiobook_root = Path(AUDIOBOOK_ROOT)
    book_audio_dir = audiobook_root / book_name / "TTS" / "audio_chunks"
    
    if not book_audio_dir.exists():
        print(f"❌ Audio directory not found: {book_audio_dir}")
        print(f"📁 Looked for: {book_audio_dir}")
        return
    
    print(f"📁 Using audio directory: {book_audio_dir}")

    while True:
        query = input("\nSearch for text fragment (or 'Q' to quit): ").strip()
        if query.lower() == "q":
            print("Exiting revision tool.")
            break

        results = search_chunks(chunks, query)
        if not results:
            print("❌ No matching chunks found.")
            continue

        print(f"\n🔍 Found {len(results)} match(es):")
        for i, chunk in enumerate(results):
            print(f"[{i}] \"{chunk['text'][:60]}...\" | Index: {chunk['index']}")

        sel = input("Select chunk index to revise: ").strip()
        if not sel.isdigit() or int(sel) >= len(results):
            print("Invalid selection.")
            continue

        chunk = results[int(sel)]
        index = chunk['index']
        # Use 5-digit chunk numbering and correct directory path
        chunk_audio_path = book_audio_dir / f"chunk_{index+1:05d}.wav"
        chunk_audio_path_str = str(chunk_audio_path)

        while True:
            print(f"\n📝 Chunk: \"{chunk['text']}\"")
            
            # Display current chunk metadata
            sentiment_compound = chunk.get('sentiment_compound', chunk.get('sentiment_score', 'N/A'))
            tts_params = chunk.get('tts_params', {})
            
            print(f"  📍 Index: {index}, Boundary: {chunk['boundary_type']}")
            print(f"  😊 Sentiment: {sentiment_compound}")
            print(f"  🎛️  TTS Params: exag={tts_params.get('exaggeration', 'N/A')}, cfg={tts_params.get('cfg_weight', 'N/A')}, temp={tts_params.get('temperature', 'N/A')}")
            print(f"  📁 Audio file: chunk_{index+1:05d}.wav")
            print("\nOptions:")
            print(" 1. Play original audio")
            print(" 2. Edit text content")
            print(" 3. Edit chunk metadata (boundary, sentiment)")
            print(" 4. Edit TTS parameters (exaggeration, cfg_weight, temperature)")
            print(" 5. Resynthesize audio with current settings")
            print(" 6. Play revised audio")
            print(" 7. Accept revision (replace original with revised)")
            print(" 8. Back to search")

            try:
                choice = input("\n💡 Enter option number [1-8]: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Input cancelled")
                return
            if choice == "1":
                print(f"\n🔊 Playing original audio: {chunk_audio_path.name}")
                play_chunk_audio(chunk_audio_path_str)
            elif choice == "2":
                print("\n✏️ Edit Text Content:")
                print(f"Current text: \"{chunk['text']}\"")
                print("💡 Enter new text (or Enter to cancel):")
                new_text = input(">>> ").strip()
                
                if new_text:
                    chunk['text'] = new_text
                    chunk['word_count'] = len(new_text.split())
                    save_chunks(str(chunk_path), chunks)
                    print("✅ Text content updated successfully")
                    print(f"📊 New word count: {chunk['word_count']}")
                else:
                    print("❌ No changes made")
            elif choice == "3":
                print("\n✏️ Edit Chunk Metadata:")
                print(f"Current boundary type: {chunk['boundary_type']}")
                boundary = input("New boundary type (none/paragraph_end/chapter_start/chapter_end/section_break) [Enter to skip]: ").strip()
                
                current_sentiment = chunk.get('sentiment_compound', chunk.get('sentiment_score', 'N/A'))
                print(f"Current sentiment score: {current_sentiment}")
                sentiment = input("New sentiment compound score (-1.0 to 1.0) [Enter to skip]: ").strip()

                try:
                    if boundary:
                        chunk['boundary_type'] = boundary
                        print(f"✅ Updated boundary type to: {boundary}")
                    
                    if sentiment:
                        sentiment_val = float(sentiment)
                        if -1.0 <= sentiment_val <= 1.0:
                            chunk['sentiment_compound'] = sentiment_val
                            # Also update old key for compatibility
                            chunk['sentiment_score'] = sentiment_val
                            print(f"✅ Updated sentiment score to: {sentiment_val}")
                        else:
                            print("❌ Sentiment score must be between -1.0 and 1.0")
                    
                    save_chunks(str(chunk_path), chunks)
                    print("✅ Chunk metadata updated successfully")
                except ValueError as e:
                    print(f"❌ Invalid input: {e}")
                except Exception as e:
                    print(f"❌ Error updating chunk: {e}")
            elif choice == "4":
                print("\n🎛️ Edit TTS Parameters:")
                current_tts_params = chunk.get('tts_params', {})
                
                def get_float_input(param_name, current_val, min_val=None, max_val=None):
                    while True:
                        try:
                            prompt = f"New {param_name} [{current_val}]: "
                            value = input(prompt).strip()
                            if not value:
                                return current_val
                            new_val = float(value)
                            if min_val is not None and new_val < min_val:
                                print(f"❌ {param_name} must be >= {min_val}")
                                continue
                            if max_val is not None and new_val > max_val:
                                print(f"❌ {param_name} must be <= {max_val}")
                                continue
                            return new_val
                        except ValueError:
                            print(f"❌ Invalid input. Please enter a valid number.")
                
                # Edit TTS parameters
                print(f"Current TTS parameters:")
                current_exag = current_tts_params.get('exaggeration', 1.0)
                current_cfg = current_tts_params.get('cfg_weight', 0.7)
                current_temp = current_tts_params.get('temperature', 0.7)
                
                print(f"  Exaggeration: {current_exag}")
                print(f"  CFG Weight: {current_cfg}")
                print(f"  Temperature: {current_temp}")
                
                new_exag = get_float_input("exaggeration", current_exag, 0.0, 3.0)
                new_cfg = get_float_input("CFG weight", current_cfg, 0.0, 2.0)
                new_temp = get_float_input("temperature", current_temp, 0.0, 2.0)
                
                # Update chunk TTS parameters
                if 'tts_params' not in chunk:
                    chunk['tts_params'] = {}
                
                chunk['tts_params']['exaggeration'] = new_exag
                chunk['tts_params']['cfg_weight'] = new_cfg
                chunk['tts_params']['temperature'] = new_temp
                
                save_chunks(str(chunk_path), chunks)
                print(f"✅ TTS parameters updated: exag={new_exag}, cfg={new_cfg}, temp={new_temp}")
            elif choice == "5":
                print(f"\n🎤 Resynthesizing chunk {index+1:05d}...")
                revised_path = synthesize_chunk(chunk, index, book_name, book_audio_dir, revision=True)
                if revised_path:
                    print(f"✅ Chunk resynthesized: {revised_path}")
                else:
                    print("❌ Failed to resynthesize chunk")
            elif choice == "6":
                rev_path = book_audio_dir / f"chunk_{index+1:05d}_rev.wav"
                print(f"\n🔊 Playing revised audio: {rev_path.name}")
                play_chunk_audio(str(rev_path))
            elif choice == "7":
                print(f"\n📦 Accepting revision for chunk {index+1:05d}...")
                accept_revision(index, book_audio_dir)
                print("✅ Revision accepted successfully")
                break
            elif choice == "8":
                print("🔙 Returning to search...")
                break
            elif choice.lower() == 'q':
                print("🚪 Exiting chunk repair tool...")
                return
            else:
                print(f"❌ Invalid option '{choice}'. Please enter a number 1-8 (or 'q' to quit).")
