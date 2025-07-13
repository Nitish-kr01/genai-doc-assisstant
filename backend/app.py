# genai-doc-assistant/backend/app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.doc_parser import parse_document
from backend.utils.summarizer import generate_summary
from backend.rag_engine import initialize_vector_store, ask_question, challenge_user

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory state
vector_store = None

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    text = await parse_document(file)
    summary = generate_summary(text)
    global vector_store
    vector_store = initialize_vector_store(text)
    return {"summary": summary}

@app.post("/ask")
async def ask(query: str = Form(...)):
    response = ask_question(query, vector_store)
    return response

@app.post("/challenge")
async def challenge(answer1: str = Form(...), answer2: str = Form(...), answer3: str = Form(...)):
    questions, feedback = challenge_user([answer1, answer2, answer3], vector_store)
    return {"questions": questions, "feedback": feedback}