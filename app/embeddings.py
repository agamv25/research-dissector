from sentence_transformers import SentenceTransformer
_model = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model

def _embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    model = _get_model
    vectors = model.encode(texts, convert_to_numpy=True)
    return vectors.tolist() 