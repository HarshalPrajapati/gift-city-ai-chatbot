from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

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

print("Creating embeddings...")

embeddings = model.encode(chunks)

print("Total Chunks:", len(chunks))
print("Embedding Shape:", embeddings.shape)