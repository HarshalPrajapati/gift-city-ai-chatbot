from pypdf import PdfReader

pdf_path = "app/data/gift_guidebook.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

# Chunk settings
CHUNK_SIZE = 500
OVERLAP = 100

chunks = []

start = 0

while start < len(text):
    end = start + CHUNK_SIZE

    chunk = text[start:end]

    chunks.append(chunk)

    start += (CHUNK_SIZE - OVERLAP)

print(f"Total Chunks: {len(chunks)}")

print("\n--- SAMPLE CHUNK ---\n")
print(chunks[0])

print("\nChunk Length:", len(chunks[0]))