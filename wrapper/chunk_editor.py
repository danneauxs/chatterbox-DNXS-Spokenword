def update_chunk(chunk, boundary_type=None, pause_duration=None, sentiment_score=None):
    if boundary_type is not None:
        chunk['boundary_type'] = boundary_type
    if pause_duration is not None:
        chunk['pause_duration'] = pause_duration
    if sentiment_score is not None:
        chunk['sentiment_score'] = sentiment_score
    return chunk
