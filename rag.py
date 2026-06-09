import os
from groq import Groq
from retriever import retrieve, filter_by_professor
from dotenv import load_dotenv

load_dotenv()

# FIX: only instantiate the client once
client = Groq(api_key=os.environ["GROQ_API_KEY"])


def format_context(chunks):
    context_parts = []
    sources = set()

    for i, c in enumerate(chunks):
        meta = c["metadata"]

        review_block = (
            f"==============================\n"
            f"REVIEW {i + 1}\n"
            f"==============================\n"
            f"Professor: {meta.get('professor', 'Unknown')}\n"
            f"Course: {meta.get('course', 'Unknown')}\n"
            f"\nSTUDENT REVIEW:\n{c['text']}\n"
        )

        context_parts.append(review_block)
        sources.add(meta.get("source", "Unknown"))

    return "\n".join(context_parts), list(sources)


SYSTEM_PROMPT = """
You are a university assistant that answers questions about professors based solely on student reviews.

RULES:
- Answer ONLY using the provided context. Do not add outside knowledge.
- If the question names a specific professor, use only reviews for that professor.
- If multiple reviews disagree, present each perspective separately — do not average or summarize them into one conclusion.
- Do not use phrases like "overall", "generally", or "in conclusion".
- Do not number or label individual reviews in your answer.
- Do not expose source filenames or internal metadata to the user.
- If the context does not contain enough information to answer, respond with:
  "I don't have enough information from the student reviews to answer that."
"""


def generate_answer(question, chunks):
    context, sources = format_context(chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"Question: {question}\n\n"
            f"Context:\n{context}\n\n"
            "Answer using only the context above."
        )}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2
    )

    # FIX: extract the text content from the response object
    answer_text = response.choices[0].message.content

    return {
        "answer": answer_text,
        "sources": sources
    }


def ask(question, k=10):
    chunks = retrieve(question, k=k)

    # FIX: use the shared filter from retriever instead of duplicating it
    chunks = filter_by_professor(chunks, question)
    chunks = chunks[:4]

    return generate_answer(question, chunks)