from sentence_transformers import SentenceTransformer
import numpy as np
import os

# PHASE 2.1: Local Embeddings
# Using a local model as instructed to avoid API loops.
MODEL_NAME = 'all-MiniLM-L6-v2' # 384 dimensions
model = None

def get_embeddings(texts):
    global model
    if model is None:
        print(f"[PHASE 2.1] Loading local model: {MODEL_NAME}")
        model = SentenceTransformer(MODEL_NAME)
    
    print(f"[PHASE 2.1] Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts)
    
    # Validation per roadmap
    assert embeddings.shape[0] == len(texts), "Embeddings count mismatch"
    assert embeddings.shape[1] == 384, f"Embeddings dimension mismatch: {embeddings.shape[1]} != 384"
    
    # Save deliverable
    output_path = os.path.join("data", "embeddings.npy")
    np.save(output_path, embeddings)
    print(f"[PHASE 2.1] Embeddings saved to {output_path}")
    
    return embeddings

def get_query_embedding(query):
    global model
    if model is None:
        model = SentenceTransformer(MODEL_NAME)
    return model.encode([query])[0]
