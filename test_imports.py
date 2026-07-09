from fastapi import FastAPI
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import requests

print("All imports successful!")