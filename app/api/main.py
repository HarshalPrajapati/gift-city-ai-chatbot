from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.rag_engine import ask_question_stream

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static Files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(
    directory="app/templates"
)

# -----------------------------
# Models
# -----------------------------

class Question(BaseModel):
    question: str

# -----------------------------
# Routes
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/chat")
def chat(data: Question):

    return StreamingResponse(
        ask_question_stream(data.question),
        media_type="text/plain"
    )

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }