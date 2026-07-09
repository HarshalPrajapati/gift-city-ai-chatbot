from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

pdf_path = "app/data/gift_guidebook.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

# Chunking
CHUNK_SIZE = 500
OVERLAP = 100

chunks = []

start = 0

while start < len(text):
    chunk = text[start:start + CHUNK_SIZE]
    chunks.append(chunk)
    start += (CHUNK_SIZE - OVERLAP)

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Vectors stored:", index.ntotal)

faiss.write_index(index, "app/vector_store/gift_index.faiss")

print("FAISS index saved successfully")