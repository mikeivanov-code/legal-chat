from pathlib import Path
from .parsers import read_any
from .chunking import chunk_text
from .embeddings import embed_texts
from .vectordb import get_collection, upsert_chunks
from .config import DB_PATH, COLLECTION, CHUNK_SIZE, CHUNK_OVERLAP, EMB_MODEL

def index_client(data_root: Path, client_id: str):
    folder = data_root / client_id
    if not folder.is_dir():
        raise FileNotFoundError(f"No folder for {client_id}: {folder}")

    coll = get_collection(DB_PATH, COLLECTION)
    files = list(folder.rglob("*"))
    supported = [p for p in files if p.suffix.lower() in (".txt", ".pdf", ".docx")]

    count_chunks = 0
    for path in supported:
        text = read_any(path)
        if not text.strip():
            continue
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        vecs = embed_texts(chunks, EMB_MODEL)
        upsert_chunks(coll, client_id, path, chunks, vecs)
        count_chunks += len(chunks)
    print(f"Indexed {len(supported)} files ({count_chunks} chunks) for client {client_id}.")
