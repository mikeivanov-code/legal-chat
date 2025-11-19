from PyPDF2 import PdfReader
try:
    import docx  # python-docx
except Exception:
    docx = None

def read_txt(path):
    return open(path, "r", encoding="utf-8", errors="ignore").read()

def read_pdf(path):
    text = []
    reader = PdfReader(str(path))
    for p in reader.pages:
        t = p.extract_text() or ""
        text.append(t)
    return "\n".join(text)

def read_docx(path):
    if docx is None:
        raise RuntimeError("Install python-docx")
    d = docx.Document(str(path))
    return "\n".join(p.text for p in d.paragraphs)

def read_any(path):
    ext = path.suffix.lower()
    if ext == ".txt":  return read_txt(path)
    if ext == ".pdf":  return read_pdf(path)
    if ext == ".docx": return read_docx(path)
    return ""
