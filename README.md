Legal Chat (RAG, local, Ollama)

A local chat application for legal documents with client-level isolation.
Uses: Python, Ollama (llama3.1:8b), local embeddings (nomic-embed-text), ChromaDB.

Structure
legal-chat/
├─ data/
│  └─ client_example/
├─ storage/
│  └─ chroma_db/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ parsers.py
│  ├─ chunking.py
│  ├─ embeddings.py
│  ├─ vectordb.py
│  ├─ ingest.py
│  ├─ retrieval.py
│  ├─ prompts.py
│  ├─ chat.py
│  └─ pipeline.py
├─ main.py
└─ requirements.txt

Installation

Install Ollama and run it (https://ollama.com/
).

Download the models:

ollama pull llama3.1:8b
ollama pull nomic-embed-text


Install Python dependencies:

pip install -r requirements.txt


Place client documents in data/<client_id>/ (supports .pdf, .docx, .txt).

Indexing
python main.py index --client client_example

Running the chat
python main.py chat --client client_example

Notes

Search and context are filtered by client_id to prevent mixing documents between clients.

Chunking and context limiting improve accuracy and performance.

The model adds short source references in responses ([filename:chunk]).
