import ollama
from typing import List

def embed_texts(texts: List[str], model: str) -> List[List[float]]:
    vecs = []
    for t in texts:
        res = ollama.embeddings(model=model, prompt=t)
        vecs.append(res["embedding"])
    return vecs
