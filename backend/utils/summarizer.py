# genai-doc-assistant/backend/utils/summarizer.py
import ollama

def generate_summary(document_text: str) -> str:
    prompt = (
        """
        Summarize the following document in 150 words or less:

        ---
        {text}
        ---
        """.strip().format(text=document_text[:4000])  # limit input to fit context window
    )

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()