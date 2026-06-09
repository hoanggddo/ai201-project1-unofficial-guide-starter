import gradio as gr
from rag import ask


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    # result["answer"] is now a plain string (fixed in rag.py)
    answer = result["answer"]
    sources = "\n".join(result["sources"]) if result["sources"] else "No sources found."

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# CS Professor Reviews (RAG System)")

    inp = gr.Textbox(label="Ask a question about a professor or course")
    btn = gr.Button("Search")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Sources", lines=3)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()