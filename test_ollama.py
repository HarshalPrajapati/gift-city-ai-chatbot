import requests

response = requests.post(
    "http://172.30.192.1:11434/api/generate",
    json={
        "model": "qwen3:4b",
        "prompt": "What is FastAPI in 2 lines?",
        "stream": False
    },
)

print(response.status_code)
print(response.text)