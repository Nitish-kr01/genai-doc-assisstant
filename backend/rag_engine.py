# genai-doc-assistant/backend/rag_engine.py
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
import random

# Initialize LLM and Embeddings
llm = OllamaLLM(model="llama3")
embeddings = OllamaEmbeddings(model="llama3")

def initialize_vector_store(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    return FAISS.from_documents(docs, embeddings)

'''def ask_question(query: str, vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", k=4)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.invoke(query)
    return {"answer": result}'''

def ask_question(query: str, vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", k=4)
    
    # Debug: log retrieved chunks
    docs = retriever.get_relevant_documents(query)
    print("\n--- Retrieved Chunks ---")
    for i, doc in enumerate(docs):
        print(f"Chunk {i+1}: {doc.page_content[:300]}...\n")

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.invoke({"query": query})
    return {"answer": result}

def challenge_user(user_answers, vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", k=6)
    sample_docs = retriever.get_relevant_documents("core ideas from the document")
    context = "\n".join([doc.page_content for doc in sample_docs])

    # Generate 3 questions from the doc context
    q_prompt = f"Generate 3 comprehension or logic-based questions from this content:\n{context}"
    questions = llm.invoke(q_prompt).strip().split("\n")

    feedback = []
    for i, answer in enumerate(user_answers):
        eval_prompt = f"Evaluate this answer: '{answer}' for the question: '{questions[i]}'\nUse the context:\n{context}"
        eval_response = llm.invoke(eval_prompt).strip()
        feedback.append(eval_response)

    return questions, feedback