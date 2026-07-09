# test_qwen.py

import requests
import time

start = time.time()

response = requests.post(
    "http://172.30.192.1:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": "What is Python?",
        "stream": False
    }
)

print(response.json()["response"])

print(
    f"\nTime: {time.time() - start:.2f}s"
)