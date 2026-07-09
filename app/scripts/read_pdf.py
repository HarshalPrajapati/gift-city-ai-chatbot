from pypdf import PdfReader

pdf_path = "app/data/gift_guidebook.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

print(text[:5000])
print("\n\nTOTAL CHARACTERS:", len(text))