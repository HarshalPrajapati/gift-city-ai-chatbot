# 🤖 GIFT City AI Knowledge Assistant

An AI-powered enterprise chatbot built using **Retrieval-Augmented Generation (RAG)** and a locally hosted **Small Language Model (Qwen 2.5)**. The chatbot answers company-specific queries by retrieving relevant information from GIFT City documents and generating accurate, context-aware responses.

---

## 📌 Features

- AI-powered document question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using FAISS
- Sentence Transformer embeddings
- Local inference with Ollama (Qwen 2.5)
- Multi-PDF document support
- Modern responsive chatbot interface
- Markdown-formatted responses
- Copy response functionality
- FastAPI backend
- Docker-ready project structure

---

## 🏗️ Project Architecture

```
                User
                  │
                  ▼
          FastAPI Backend
                  │
                  ▼
         Sentence Transformer
                  │
                  ▼
            Query Embedding
                  │
                  ▼
              FAISS Index
                  │
                  ▼
        Relevant Document Chunks
                  │
                  ▼
      Qwen 2.5 (Ollama - Local LLM)
                  │
                  ▼
          AI Generated Response
                  │
                  ▼
               Frontend
```

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- REST API

### AI & Machine Learning

- Retrieval-Augmented Generation (RAG)
- Ollama
- Qwen 2.5
- Sentence Transformers
- FAISS
- Prompt Engineering

### Frontend

- HTML
- CSS
- JavaScript

### Database / Storage

- FAISS Vector Store
- Pickle

### Tools

- Git
- Docker
- VS Code
- Ubuntu (WSL)

---

## 📂 Project Structure

```
company-faq-chatbot/
│
├── app/
│   ├── api/
│   ├── data/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── vector_store/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/HarshalPrajapati/gift-city-ai-chatbot.git
```

```bash
cd gift-city-ai-chatbot
```

---

### Create Virtual Environment

Linux / WSL

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Install Ollama

Download Ollama from

https://ollama.com

Pull the model

```bash
ollama pull qwen2.5:1.5b
```

---

### Run the Application

```bash
uvicorn app.api.main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

## 📄 Supported Documents

The chatbot can answer questions from:

- Residential Guidebook
- Commercial Building Guidebook
- Operational Documents
- Company PDFs

Additional PDFs can be added to the `app/data/` directory and indexed.

---

## 💬 Example Questions

- What is CRM?
- How do I apply for a power connection?
- How can I obtain a water connection?
- What facilities are available in residential buildings?
- What telecom services are available?
- Explain fire safety procedures.

---

## 🚀 Future Improvements

- Streaming responses
- Source citation
- Dark mode
- User authentication
- Conversation history
- Fine-Tuning + RAG
- Docker deployment
- Cloud deployment (AWS)

---

## 📸 Screenshots

> Add screenshots of the chatbot UI here.

---

## 👨‍💻 Author

**Harshal Prajapati**

M.Sc. Information Technology  
DA-IICT

GitHub:

https://github.com/HarshalPrajapati

---

## ⭐ Acknowledgements

- FastAPI
- Ollama
- Qwen
- Sentence Transformers
- FAISS
- Hugging Face
