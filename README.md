## genai-doc-assisstant
- An AI assistant to summarize, answer, and quiz on documents using Ollama and LangChain.
---
## Features
- **Upload Document**: *Easily upload PDF or txt files.*
- **AI-Generated summaries**: *Get concise summaries of your documents.*
- **Natural Language Q@A**: *Ask intelligent questions based on the uploaded content.*
- **Challenge Mode**: *Test your understanding with auto-generated questions and instant feedback.*
---
## Built with
- **FastAPI**: *Powers robust backend API.*
- **Streamlit**: *Provides and inuitive and interactive user interface.*
- **Ollama**: *Enables local execution of LLM (llama3).*
- **Vector Stores**: *Utilized for efficient document search and retrieval (FAISS, Langchain).*
---
## Setup Instructions
1. Clone the Repository
   ```
   git clone https://github.com/Nitish-kr01/genai-doc-assisstant.git
   cd genai-doc-assisstant
   ```
2. Create virtual environment & install dependencies
   ```
   python -m venv venv'
   venv\Scripts\activate # On mac: source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Install Ollama and pull model
   Install ollama from itys officail website: **link(https://ollama.com/downloa)d**.
   After installation, pull a lightweight LLM (llama3) needed free 4gb RAM.
   ```
   ollama pull llama3
   ```
   Start ollama model in separate terminal an keep it running.
   ```
   ollama run llama3 # Ollama run llama2:13b for better performance
   ```
6. Run the Application
   Once ollama in running, you can start the backend and frontend:
   **Start FastAPI Backend**
   In one terminal, navigate to the project's root directory and run:
   ```
   uvicorn app:app --reload
   ```
   **Start Streamlit Frontend**
   In another terminal, navigate to the project's root directory and run:
   ```
   streamlit run streamlit_app.py
   ```
---
## How It Works
1. Upload a document.
2. A summary is auto generated fromt he documents's content.
3. You can ask questions about the document.
4. Initiate Challenge Mode: three questions are generated based on the docuemnt.
5. Write your answers and click "Evaluate".
6. Receive instant feedback for each answer, evaluated against the document's context.
---
## Credits
- Created by **[Nitish Kumar Singh](https://github.com/Nitish-kr01)**.
- Powered by fantastic  open-source tools: FastAPI, Streamlit, LangChain, and Ollama.

