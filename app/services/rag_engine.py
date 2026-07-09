import os
import time
import pickle
import json
import faiss
import numpy as np
import requests
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://172.30.192.1:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:1.5b"
)

print("================================")
print("LOADING RAG ENGINE")
print("================================")

# -----------------------------------
# Load PDFs
# -----------------------------------

text = ""

pdf_folder = "app/data"

pdf_files = [
    file
    for file in os.listdir(pdf_folder)
    if file.endswith(".pdf")
]

print(f"\nFound {len(pdf_files)} PDF(s)\n")

print("Loaded PDFs:")

for pdf_file in pdf_files:

    print(f" - {pdf_file}")

    pdf_path = os.path.join(
        pdf_folder,
        pdf_file
    )

    reader = PdfReader(pdf_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

# -----------------------------------
# Load Chunks
# -----------------------------------

print("\nLoading chunks...")

with open(
    "app/vector_store/chunks.pkl",
    "rb"
) as file:

    chunks = pickle.load(file)

print(f"Loaded {len(chunks)} chunks")

# -----------------------------------
# Load Embedding Model
# -----------------------------------

print("\nLoading embedding model...")

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# Load FAISS Index
# -----------------------------------

print("\nLoading FAISS index...")

index = faiss.read_index(
    "app/vector_store/gift_index.faiss"
)

print("\n================================")
print("RAG ENGINE READY")
print("================================")


# -----------------------------------
# Ask Question
# -----------------------------------

def ask_question_stream(question: str):

    total_start = time.time()

    print("\n================================")
    print("ASK_QUESTION CALLED")
    print("QUESTION:", question)
    print("================================")

    # -----------------------------
    # Generate Embedding
    # -----------------------------

    embedding_start = time.time()

    query_embedding = embed_model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    print(
        f"Embedding Time: {time.time() - embedding_start:.2f} sec"
    )

    # -----------------------------
    # FAISS Search
    # -----------------------------

    faiss_start = time.time()

    distances, indices = index.search(
        query_embedding,
        4
    )

    print(
        f"FAISS Search Time: {time.time() - faiss_start:.4f} sec"
    )

    retrieved_chunks = [
        chunks[i]
        for i in indices[0]
    ]

    print("\n==============================")
    print("RETRIEVED CHUNKS")
    print("==============================")

    for i, chunk in enumerate(retrieved_chunks):

        print(f"\n---------- Chunk {i+1} ----------")
        print(chunk[:500])
        print("---------------------------------")

    context = "\n\n".join(
        retrieved_chunks
    )

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
You are the official AI assistant for GIFT City.

Answer ONLY using the provided context.

Rules:

- Never use outside knowledge.
- Never make assumptions.
- If the answer is not found, reply exactly:
Information not found in the provided documents.

Formatting Rules:

- Do NOT write one long paragraph.
- Always organize the answer.
- Use short paragraphs.
- Use headings where appropriate.
- Use bullet points for lists.
- Use numbered steps for procedures.
- Highlight important terms using Markdown bold (**text**).
- Keep answers professional and easy to read.

Context:
{context}

Question:
{question}

Answer:
"""
    # -----------------------------
    # Call Ollama
    # -----------------------------

    try:

        response = requests.post(

            f"{OLLAMA_URL}/api/generate",

            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": True
            },

            stream=True,

            timeout=120

        )

        response.raise_for_status()

        for line in response.iter_lines():

            if line:

                line = line.decode("utf-8")

                try:

                    data = json.loads(line)

                    if "response" in data:

                        yield data["response"]

                except Exception:

                    continue

    except Exception as error:

        print(error)

        yield "Error contacting language model."