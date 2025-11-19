from pathlib import Path
from .embeddings import embed_texts
from .vectordb import get_collection, query_topk
from .config import DB_PATH, COLLECTION, TOP_K, EMB_MODEL, MAX_CONTEXT_CHARS

def build_context(client_id: str, question: str):
    coll = get_collection(DB_PATH, COLLECTION)
    q_emb = embed_texts([question], EMB_MODEL)[0]
    res = query_topk(coll, client_id, q_emb, TOP_K)

    if not res or not res.get("documents"):
        return "", ""

    docs = res["documents"][0]
    metas = res["metadatas"][0]

    context_parts = []
    citations = []
    total = 0
    for d, m in zip(docs, metas):
        if total + len(d) > MAX_CONTEXT_CHARS:
            break
        context_parts.append(d)
        citations.append(f"[{Path(m['source']).name}:{m['chunk_index']}]")
        total += len(d)

    return "\n---\n".join(context_parts), " ".join(citations)
