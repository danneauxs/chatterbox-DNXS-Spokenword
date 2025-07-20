def search_chunks(chunks, query):
    results = []
    query_lower = query.lower()

    for chunk in chunks:
        if query_lower in chunk['text'].lower():
            results.append(chunk)

    return results
