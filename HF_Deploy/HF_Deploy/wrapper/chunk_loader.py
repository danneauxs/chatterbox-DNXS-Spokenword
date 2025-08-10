import json

def load_chunks(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # Filter out metadata entries (they start with _metadata: True)
        if isinstance(data, list):
            chunks = [item for item in data if not (isinstance(item, dict) and item.get('_metadata', False))]
            return chunks
        
        return data

def load_metadata(path):
    """Extract metadata from JSON file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list) and data:
            # Look for metadata in first element
            first_item = data[0]
            if isinstance(first_item, dict) and first_item.get('_metadata', False):
                return first_item
                
    except Exception as e:
        print(f"⚠️ Error loading metadata from {path}: {e}")
    
    return None

def save_chunks(path, chunks):
    # Validate and clean chunks before saving
    from collections import OrderedDict
    import copy
    
    cleaned_chunks = []
    for chunk in chunks:
        if isinstance(chunk, dict) and 'text' in chunk:
            original_text = chunk['text']
            # Clean up any quote corruption
            cleaned_text = original_text.replace('\\"', '"').replace("\\'", "'")
            
            # Check for dialogue corruption patterns
            if ('replied' in cleaned_text or 'said' in cleaned_text) and '"' in cleaned_text:
                # Additional cleanup for dialogue
                import re
                cleaned_text = re.sub(r'(["\'])\s*,\s*(["\'])\s*\.', r'\1.', cleaned_text)  # Fix ", ". pattern
                cleaned_text = re.sub(r'(["\'])\s*,\s*(["\'])\s*$', r'\1.', cleaned_text)  # Fix trailing ", "
                
                if cleaned_text != original_text:
                    print(f"🔧 FIXED dialogue corruption:")
                    print(f"   Before: {original_text}")
                    print(f"   After:  {cleaned_text}")
            
            # Preserve structure (OrderedDict or regular dict)
            if isinstance(chunk, OrderedDict):
                chunk_copy = OrderedDict()
                for key, value in chunk.items():
                    if key == 'text':
                        chunk_copy[key] = cleaned_text
                    else:
                        chunk_copy[key] = copy.deepcopy(value)
            else:
                chunk_copy = chunk.copy()
                chunk_copy['text'] = cleaned_text
                
            cleaned_chunks.append(chunk_copy)
        else:
            cleaned_chunks.append(chunk)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_chunks, f, indent=2, ensure_ascii=False)
