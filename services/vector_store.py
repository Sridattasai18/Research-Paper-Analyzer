import faiss
import numpy as np
import os

# PHASE 2.2: Vector Store
VECTOR_DB_PATH = os.path.join("data", "index.faiss")

def build_vector_store(embeddings):
    print(f"[PHASE 2.2] Building FAISS index with {len(embeddings)} vectors...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    # Save deliverable
    faiss.write_index(index, VECTOR_DB_PATH)
    print(f"[PHASE 2.2] Index saved to {VECTOR_DB_PATH}")
    return index

def load_vector_store():
    if not os.path.exists(VECTOR_DB_PATH):
        print(f"[PHASE 2.2] Index file not found: {VECTOR_DB_PATH}")
        return None
    
    print(f"[PHASE 2.2] Loading index from {VECTOR_DB_PATH}")
    return faiss.read_index(VECTOR_DB_PATH)

def search_vectors(index, query_embedding, k=5):
    """
    PHASE 3.1: Retrieval logic
    """
    if index is None:
        return [], []
    
    query_vector = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_vector, k)
    
    print(f"[PHASE 3.1] Retrieval complete. Found {len(indices[0])} results.")
    return distances[0], indices[0]
