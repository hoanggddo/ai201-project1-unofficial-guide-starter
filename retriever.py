import json
import uuid

import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="professor_reviews"
)


def add_chunks_to_db(chunks):
    """
    Adds chunks from chunks.json into ChromaDB.
    Encodes all texts in one batch for speed.
    """
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    for chunk, embedding in zip(chunks, embeddings):
        try:
            collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[{
                    "professor": chunk["professor"],
                    "course": chunk["course"],
                    "source": chunk["source"]
                }]
            )
        except Exception as e:
            print(f"Warning: failed to add chunk '{chunk.get('review_id')}': {e}")

    print(f"Successfully added {len(chunks)} chunks.")


def retrieve(query, k=4):
    """
    Returns the top-k most similar chunks to the query.
    Caps k at the number of documents in the collection.
    """
    count = collection.count()
    if count == 0:
        print("Warning: collection is empty.")
        return []

    k = min(k, count)
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_data = []

    for i in range(len(results["documents"][0])):
        retrieved_data.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_data


def filter_by_professor(chunks, question):
    """
    Filters retrieved chunks to only those matching a professor
    explicitly named in the question. Returns all chunks if no
    professor name is detected.
    """
    q = question.lower()

    professors_mentioned = [
        c["metadata"].get("professor", "")
        for c in chunks
        if c["metadata"].get("professor", "").lower() in q
    ]

    if not professors_mentioned:
        return chunks

    # Use the first matched professor (most specific match)
    target_prof = professors_mentioned[0]

    return [
        c for c in chunks
        if c["metadata"].get("professor") == target_prof
    ]


if __name__ == "__main__":

    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Delete old data before re-adding to avoid duplicates
    try:
        client.delete_collection("professor_reviews")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="professor_reviews"
    )

    add_chunks_to_db(chunks)

    print("\nDatabase ready.\n")

    query = input("Enter a question: ")

    results = retrieve(query, k=10)
    results = filter_by_professor(results, query)
    results = results[:4]

    for r in results:
        print(r["metadata"])
        print(r["text"][:200])
        print("---")