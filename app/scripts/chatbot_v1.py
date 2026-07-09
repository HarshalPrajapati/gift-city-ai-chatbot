from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import time

# -----------------------------------
# Load PDF
# -----------------------------------

print("Loading PDF...")

reader = PdfReader(
    "app/data/gift_guidebook.pdf"
)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

# -----------------------------------
# Create Chunks
# -----------------------------------

CHUNK_SIZE = 500
OVERLAP = 100

chunks = []

start = 0

while start < len(text):

    chunk = text[start:start + CHUNK_SIZE]

    chunks.append(chunk)

    start += (CHUNK_SIZE - OVERLAP)

print(f"Loaded {len(chunks)} chunks")

# -----------------------------------
# Load Embedding Model
# -----------------------------------

print("Loading embedding model...")

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# Load FAISS Index
# -----------------------------------

print("Loading FAISS index...")

index = faiss.read_index(
    "app/vector_store/gift_index.faiss"
)

print("Ready!\n")

# -----------------------------------
# Chat Loop
# -----------------------------------

while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    if question.lower() == "exit":
        print("Goodbye!")
        break

    # -------------------------------
    # Convert question to embedding
    # -------------------------------

    query_embedding = embed_model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # -------------------------------
    # Search FAISS
    # -------------------------------

    distances, indices = index.search(
        query_embedding,
        2
    )

    print("\nRetrieved Chunk IDs:")
    print(indices)

    context = "\n\n".join(
        [chunks[i] for i in indices[0]]
    )

    print("\n===== RETRIEVED CONTEXT =====\n")
    print(context)
    print("\n=============================\n")

    # -------------------------------
    # Build Prompt
    # -------------------------------

    prompt = f"""
You are a GIFT City assistant.

Use ONLY the provided context.

Answer in 2-3 sentences maximum.

If information is unavailable, reply:

"Information not found in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    # -------------------------------
    # Call Ollama
    # -------------------------------

    start_time = time.time()

    try:

        response = requests.post(
            "http://172.30.192.1:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        end_time = time.time()

        answer = response.json()["response"]

        print(
            f"\nResponse Time: "
            f"{end_time - start_time:.2f} seconds"
        )

        print("\n===== ANSWER =====\n")

        print(answer)

        print("\n==================\n")

    except Exception as e:

        print("\nERROR:")
        print(e)