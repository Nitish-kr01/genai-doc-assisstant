'''# genai-doc-assistant/frontend/streamlit_app.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="GenAI Document Assistant", layout="wide")
st.title("📄 GenAI Document Assistant")

# File Upload Section
st.header("1️⃣ Upload Document")
file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if file:
    with st.spinner("Processing and summarizing..."):
        response = requests.post(
            f"{API_BASE}/upload",
            files={"file": file}
        )
        if response.ok:
            summary = response.json()["summary"]
            st.subheader("📌 Summary")
            st.write(summary)
        else:
            st.error("Upload failed")

    # Ask Anything Section
    st.header("2️⃣ Ask Anything")
    query = st.text_input("Type a question about the document")
    if st.button("Ask") and query:
        res = requests.post(f"{API_BASE}/ask", data={"query": query})
        st.markdown(f"**Answer:** {res.json()['answer']}")

    # Challenge Me Section
    st.header("3️⃣ Challenge Me")
    st.markdown("You'll receive 3 questions based on the document. Please answer them below:")

    a1 = st.text_input("Answer for Question 1")
    a2 = st.text_input("Answer for Question 2")
    a3 = st.text_input("Answer for Question 3")

    if st.button("Submit Answers"):
        challenge_res = requests.post(
            f"{API_BASE}/challenge",
            data={"answer1": a1, "answer2": a2, "answer3": a3}
        )
        if challenge_res.ok:
            result = challenge_res.json()
            st.subheader("🧠 Questions")
            for i, q in enumerate(result['questions']):
                st.write(f"Q{i+1}: {q}")

            st.subheader("🔍 Feedback")
            for i, f in enumerate(result['feedback']):
                st.write(f"Answer {i+1} Feedback: {f}")
        else:
            st.error("Challenge mode failed.")
'''
# genai-doc-assistant/frontend/streamlit_app.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="GenAI Document Assistant", layout="wide")
st.title("📄 GenAI Document Assistant")

# File Upload Section
st.header("1️⃣ Upload Document")
file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# Cache summary after upload
if file and "summary" not in st.session_state:
    with st.spinner("Processing and summarizing..."):
        response = requests.post(
            f"{API_BASE}/upload",
            files={"file": file}
        )
        if response.ok:
            st.session_state["summary"] = response.json()["summary"]
        else:
            st.error("Upload failed")

if "summary" in st.session_state:
    st.subheader("📌 Summary")
    st.write(st.session_state["summary"])

    # Ask Anything Section
    st.header("2️⃣ Ask Anything")
    query = st.text_input("Type a question about the document")
    if st.button("Ask") and query:
        res = requests.post(f"{API_BASE}/ask", data={"query": query})
        st.markdown(f"**Answer:** {res.json()['answer']}")

    # Challenge Me Section
    st.header("3️⃣ Challenge Me")

    if "questions" not in st.session_state:
        if st.button("Start Challenge"):
            challenge_res = requests.post(f"{API_BASE}/challenge", data={
                "answer1": "", "answer2": "", "answer3": ""
            })
            if challenge_res.ok:
                result = challenge_res.json()
                st.session_state["questions"] = result["questions"]
                st.session_state["feedback"] = ["", "", ""]

    if "questions" in st.session_state:
        st.subheader("🧠 Questions")
        answers = []
        for i, q in enumerate(st.session_state["questions"]):
            st.markdown(f"**Q{i+1}:** {q}")
            answers.append(st.text_input(f"Answer {i+1}", key=f"answer_{i}"))

        if st.button("Submit Answers"):
            challenge_res = requests.post(
                f"{API_BASE}/challenge",
                data={"answer1": answers[0], "answer2": answers[1], "answer3": answers[2]}
            )
            if challenge_res.ok:
                result = challenge_res.json()
                st.session_state["feedback"] = result["feedback"]

        if "feedback" in st.session_state:
            st.subheader("🔍 Feedback")
            for i, f in enumerate(st.session_state["feedback"]):
                st.markdown(f"**Answer {i+1} Feedback:** {f}")
