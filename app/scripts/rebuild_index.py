from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

print("================================")
print("REBUILDING VECTOR DATABASE")
print("================================")

# -------------------------
# Load PDFs
# -------------------------

pdf_folder = "app/data"

pdf_files = [
    file
    for file in os.listdir(pdf_folder)
    if file.endswith(".pdf")
]

print(f"\nFound {len(pdf_files)} PDF(s)\n")

text = ""

for pdf_file in pdf_files:

    print(f"Loading: {pdf_file}")

    pdf_path = os.path.join(
        pdf_folder,
        pdf_file
    )

    reader = PdfReader(pdf_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

# -------------------------
# Create Chunks
# -------------------------

CHUNK_SIZE = 500
OVERLAP = 100

chunks = []

start = 0

while start < len(text):

    chunk = text[
        start:start + CHUNK_SIZE
    ]

    chunks.append(chunk)

    start += (
        CHUNK_SIZE - OVERLAP
    )

print(
    f"\nCreated {len(chunks)} chunks"
)

# -------------------------
# Save Chunks
# -------------------------

os.makedirs(
    "app/vector_store",
    exist_ok=True
)

with open(
    "app/vector_store/chunks.pkl",
    "wb"
) as f:

    pickle.dump(
        chunks,
        f
    )

print(
    "Saved chunks.pkl"
)

# -------------------------
# Embeddings
# -------------------------

print(
    "\nLoading embedding model..."
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print(
    "Generating embeddings..."
)

embeddings = model.encode(
    chunks,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings
).astype("float32")

print(
    f"Embedding Shape: {embeddings.shape}"
)

# -------------------------
# FAISS Index
# -------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    "app/vector_store/gift_index.faiss"
)

print(
    "\nSaved gift_index.faiss"
)

print(
    "\nVECTOR DATABASE READY"
)