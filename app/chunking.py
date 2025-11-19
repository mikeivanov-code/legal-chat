def chunk_text(text: str, size: int, overlap: int):
    text = "\n".join(line.strip() for line in text.splitlines())
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + size, n)
        chunks.append(text[start:end])
        if end == n: break
        start = max(0, end - overlap)
    return chunks
