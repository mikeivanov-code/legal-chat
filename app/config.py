from pathlib import Path

DATA_ROOT = Path("data")
DB_PATH = Path("storage/chroma_db")
COLLECTION = "legal_docs"

GEN_MODEL = "llama3.1:8b"
EMB_MODEL = "nomic-embed-text"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 6
MAX_CONTEXT_CHARS = 6000  # лимит для prompt
