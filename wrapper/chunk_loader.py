import json

def load_chunks(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chunks(path, chunks):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
