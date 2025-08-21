import chromadb, time
from sentence_transformers import SentenceTransformer
from .settings import settings

_client = None
_mem_embed = None

def _get_client():
    global _client
    if _client is None:
        _host = settings.chroma_url.split("//")[1].split(":")[0]
        _port = int(settings.chroma_url.split(":")[-1])
        _client = chromadb.HttpClient(host=_host, port=_port)
    return _client

def _get_embed_model():
    global _mem_embed
    if _mem_embed is None:
        # Use device detection for consistency
        import torch
        import os
        if torch.cuda.is_available():
            device = "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
        _mem_embed = SentenceTransformer(settings.embedding_model, device=device)
        print(f"✅ Loaded memory embedding model on {device}")
    return _mem_embed

def _mem_col(user_id: str):
    collection_name = f"mem_{user_id}"
    try:
        # Try to get existing collection
        return _get_client().get_collection(collection_name)
    except Exception:
        # Create new collection if it doesn't exist
        model = _get_embed_model()
        sample_embedding = model.encode(["test"], normalize_embeddings=True)[0]
        embedding_dim = len(sample_embedding)
        print(f"✅ Creating memory collection for {user_id} with dimension {embedding_dim}")
        return _get_client().create_collection(
            name=collection_name,
            metadata={"dimension": embedding_dim, "hnsw:space": "cosine"}
        )

def remember(user_id: str, role: str, text: str):
    col = _mem_col(user_id)
    ts = time.time()
    doc = f"[{role} @ {ts:.0f}] {text}"
    emb = _get_embed_model().encode([doc], normalize_embeddings=True).tolist()[0]
    col.upsert(
        ids=[f"{user_id}:{ts:.0f}"],
        embeddings=[emb],
        documents=[doc],
        metadatas=[{"user_id": user_id, "role": role, "ts": ts}],
    )

def recall(user_id: str, query: str, n: int = 6):
    col = _mem_col(user_id)
    q = _get_embed_model().encode([query], normalize_embeddings=True).tolist()
    try:
        res = col.query(query_embeddings=q, n_results=n)
    except Exception:
        return []
    return res.get("documents", [[]])[0] or []
