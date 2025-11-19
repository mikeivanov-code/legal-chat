import chromadb
from typing import List

def get_collection(db_path, collection_name):
    client = chromadb.PersistentClient(path=str(db_path))
    try:
        return client.get_collection(collection_name)
    except Exception:
        return client.create_collection(collection_name, metadata={"hnsw:space": "cosine"})

def upsert_chunks(coll, client_id: str, source_path, chunks: List[str], embeddings: List[List[float]]):
    base = source_path.stem
    ids, metas = [], []
    for i, _ in enumerate(chunks):
        ids.append(f"{client_id}::{base}::{i}")
        metas.append({"client_id": client_id, "source": str(source_path), "chunk_index": i})
    coll.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metas)

def query_topk(coll, client_id: str, query_emb, k: int):
    return coll.query(query_embeddings=[query_emb], n_results=k, where={"client_id": client_id})
