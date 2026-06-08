import chromadb
from sentence_transformers import SentenceTransformer
import uuid

# 1. Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize ChromaDB (Persistent storage so data survives between runs)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="professor_reviews")

def add_chunks_to_db(chunks):
    """
    Chunks is a list of dicts: {'professor': ..., 'course': ..., 'text': ..., 'source': ...}
    """
    for chunk in chunks:
        # Generate embedding for the text
        embedding = model.encode(chunk['text']).tolist()
        
        # Add to ChromaDB
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk['text']],
            metadatas=[{
                "professor": chunk['professor'],
                "course": chunk['course'],
                "source": chunk['source']
            }]
        )
    print(f"Successfully added {len(chunks)} chunks to the database.")

def retrieve(query, k=4):
    """
    Embeds the query and fetches the top-k most similar chunks.
    """
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    # Format the results for readability
    retrieved_data = []
    for i in range(len(results['documents'][0])):
        retrieved_data.append({
            "text": results['documents'][0][i],
            "metadata": results['metadatas'][0][i],
            "distance": results['distances'][0][i]
        })
    return retrieved_data

# --- Verification ---
if __name__ == "__main__":
    # Example: run this after your ingest.py finishes
    # test_results = retrieve("Which CS professor is best for beginners?", k=2)
    # for res in test_results:
    #     print(f"Match (Dist: {res['distance']:.3f}): {res['metadata']['professor']} - {res['text'][:100]}...")