import chromadb, httpx
import torch
from sentence_transformers import SentenceTransformer
from .settings import settings

# Detect available device with optimizations
def _get_device():
    import os
    # Check for CUDA
    if torch.cuda.is_available() and torch.cuda.device_count() > 0:
        device = "cuda"
        print(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
        return device
    
    # Check for Apple Silicon MPS (Metal Performance Shaders)
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = "mps"
        print(f"🍎 Apple Metal GPU detected, using MPS acceleration")
        return device
    
    else:
        # Optimize CPU inference
        cpu_threads = os.cpu_count()
        if cpu_threads:
            torch.set_num_threads(min(cpu_threads, 8))  # Limit to 8 threads max
            print(f"💻 Using CPU with {min(cpu_threads, 8)} threads optimized")
        return "cpu"

# Global variables for lazy loading
_client = None
_txt_model = None
_img_model = None
_text_col = None
_img_col = None

def _get_client():
    global _client
    if _client is None:
        host = settings.chroma_url.split("//")[1].split(":")[0]
        port = int(settings.chroma_url.split(":")[-1])
        _client = chromadb.HttpClient(host=host, port=port)
    return _client

def _get_txt_model():
    global _txt_model
    if _txt_model is None:
        device = _get_device()
        _txt_model = SentenceTransformer(settings.embedding_model, device=device)
        print(f"✅ Loaded text embedding model on {device}")
    return _txt_model

def _get_img_model():
    global _img_model
    if _img_model is None:
        device = _get_device()
        _img_model = SentenceTransformer(settings.image_embedding_model, device=device)
        print(f"✅ Loaded image embedding model on {device}")
    return _img_model

def _get_text_col():
    global _text_col
    if _text_col is None:
        # Get embedding model dimension to ensure compatibility
        model = _get_txt_model()
        sample_embedding = model.encode(["test"], normalize_embeddings=True)[0]
        embedding_dim = len(sample_embedding)
        print(f"✅ Text embedding dimension: {embedding_dim}")
        
        try:
            # Try to get existing collection
            _text_col = _get_client().get_collection("text_chunks")
        except Exception:
            # Create new collection if it doesn't exist
            _text_col = _get_client().create_collection(
                name="text_chunks",
                metadata={"dimension": embedding_dim, "hnsw:space": "cosine"}
            )
            print(f"✅ Created new text collection with dimension {embedding_dim}")
    return _text_col

def _get_img_col():
    global _img_col
    if _img_col is None:
        # Get embedding model dimension to ensure compatibility
        model = _get_img_model()
        sample_embedding = model.encode(["test"], normalize_embeddings=True)[0]
        embedding_dim = len(sample_embedding)
        print(f"✅ Image embedding dimension: {embedding_dim}")
        
        try:
            # Try to get existing collection
            _img_col = _get_client().get_collection("image_chunks")
        except Exception:
            # Create new collection if it doesn't exist
            _img_col = _get_client().create_collection(
                name="image_chunks",
                metadata={"dimension": embedding_dim, "hnsw:space": "cosine"}
            )
            print(f"✅ Created new image collection with dimension {embedding_dim}")
    return _img_col

def upsert_text(doc_id, title, page, section, chunks):
    if not chunks: return
    ids = [f"{doc_id}:{page}:{i}" for i,_ in enumerate(chunks)]
    embs = _get_txt_model().encode(chunks, normalize_embeddings=True).tolist()
    metas= [{"doc_id":doc_id,"title":title,"page":page,"section":section or "","type":"text"} for _ in chunks]
    _get_text_col().upsert(ids=ids, embeddings=embs, metadatas=metas, documents=chunks)

def upsert_images(imgs):
    if not imgs: return
    captions = [f"Figure p.{i['page']}" for i in imgs]
    embs = _get_img_model().encode(captions, normalize_embeddings=True).tolist()
    ids  = [f"{i['doc_id']}:img:{i['page']}:{k}" for k,i in enumerate(imgs)]
    metas= [{"doc_id":i["doc_id"],"page":i["page"],"url":i["url"],"type":"image"} for i in imgs]
    _get_img_col().upsert(ids=ids, embeddings=embs, metadatas=metas, documents=captions)

async def search(query: str, k: int = 6, want_images: bool = True):
    qvec = _get_txt_model().encode([query], normalize_embeddings=True)[0].tolist()
    text = _get_text_col().query(query_embeddings=[qvec], n_results=k)
    hits = []
    if text.get("ids") and text["ids"][0]:
        for did, meta, doc, dist in zip(text["ids"][0], text["metadatas"][0], text["documents"][0], text["distances"][0]):
            hits.append({
              "doc_id":meta["doc_id"],"title":meta["title"],
              "page":meta["page"],"section":meta.get("section"),
              "snippet":doc[:600],"score":1.0 - dist
            })
    images = []
    if want_images:
        img = _get_img_col().query(query_embeddings=[qvec], n_results=min(4,k))
        if img.get("ids") and img["ids"][0]:
            for meta in img["metadatas"][0]:
                images.append(meta["url"])
    return hits, images

async def call_llm(prompt: str, context_blocks):
    sys = ("You are a medical assistant. Use provided context if helpful; "
           "cite sources as [title p.X]. Keep answers concise.")
    ctx = "\n\n".join([f"[CTX {i+1}]\n{c}" for i,c in enumerate(context_blocks)])
    messages = [
      {"role":"system","content":sys},
      {"role":"user","content": f"{prompt}\n\nContext:\n{ctx}"}
    ]
    payload = {"model": settings.openai_chat_model, "messages": messages, "temperature": 0.2, "max_tokens": 512}
    
    print(f"🤖 Calling LLM: {settings.openai_chat_model} at {settings.openai_base_url}")
    
    try:
        headers = {"Content-Type": "application/json"}
        if settings.openai_api_key:
            headers["Authorization"] = f"Bearer {settings.openai_api_key}"
        
        async with httpx.AsyncClient(timeout=120) as ax:
            r = await ax.post(f"{settings.openai_base_url}/chat/completions", json=payload, headers=headers)
            r.raise_for_status()
            result = r.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"No response choices in LLM result: {result}")
    except httpx.ConnectError as e:
        print(f"❌ LLM Connection Error: {str(e)}")
        raise Exception(f"Cannot connect to LLM server at {settings.openai_base_url}. Please ensure LM Studio is running with network access enabled. Error: {str(e)}")
    except httpx.TimeoutException as e:
        print(f"❌ LLM Timeout Error: {str(e)}")
        raise Exception(f"LLM server timeout. The model may be too slow or overloaded. Error: {str(e)}")
    except httpx.HTTPStatusError as e:
        print(f"❌ LLM HTTP Error {e.response.status_code}: {e.response.text}")
        raise Exception(f"LLM server returned error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"❌ LLM General Error: {str(e)}")
        raise Exception(f"LLM error: {str(e)}")
