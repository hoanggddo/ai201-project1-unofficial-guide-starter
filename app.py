import os
import gradio as gr
from groq import Groq
from retriever import retrieve  # Assuming your retriever logic is in retriever.py
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_question(question):
    # 1. Retrieve context
    results = retrieve(question, k=4)
    context_text = "\n\n".join([f"Source: {r['metadata']['source']}\nContent: {r['text']}" for r in results])
    sources = list(set([r['metadata']['source'] for r in results]))

    # 2. Build Prompt
    prompt = f"""
    You are an expert academic advisor at GMU. Answer the question using ONLY the provided documents.
    If the answer is not in the documents, say "I don't have enough information on that."
    Always cite the source document for every claim you make.

    Documents:
    {context_text}

    Question: {question}
    """

    # 3. Call LLM
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    
    answer = response.choices[0].message.content
    return answer, ", ".join(sources)

# 4. Gradio Interface
demo = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Ask a question about CS professors"),
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Sources Used")
    ],
    title="The Unofficial Guide: CS Professor Edition"
)

if __name__ == "__main__":
    demo.launch()