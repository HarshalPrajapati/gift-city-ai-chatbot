from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ------------------
# Reload PDF chunks
# ------------------

reader = PdfReader("app/data/gift_guidebook.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

CHUNK_SIZE = 500
OVERLAP = 100

chunks = []

start = 0

while start < len(text):
    chunks.append(text[start:start + CHUNK_SIZE])
    start += (CHUNK_SIZE - OVERLAP)

# ------------------
# Load model & index
# ------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index(
    "app/vector_store/gift_index.faiss"
)

# ------------------
# Ask question
# ------------------

query = input("Ask a question: ")

query_embedding = model.encode([query])

query_embedding = np.array(
    query_embedding
).astype("float32")

# Top 3 results
k = 3

distances, indices = index.search(
    query_embedding,
    k
)

print("\n\n===== RESULTS =====\n")

for i in indices[0]:
    print(chunks[i])
    print("\n-----------------\n")