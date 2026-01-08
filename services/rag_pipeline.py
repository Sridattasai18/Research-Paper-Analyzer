import json
import os
import time
import random
from services.embeddings import get_query_embedding
from services.vector_store import load_vector_store, search_vectors
from config import GENERATIVE_MODEL, client

# Improvement 1.1: Section-Aware Boosting
SECTION_PRIORITY = {
    "Abstract": 0.6,       # Strong preference
    "Introduction": 0.7,
    "Conclusion": 0.75,
    "Discussion": 0.9,
    "Methodology": 1.0,
    "Results": 1.0,
    "Background": 1.0,
    "General": 1.3,        # Penalty for unknown
    "Appendix": 2.0,       # Heavy penalty
    "References": 3.0      # Exclude
}

# Improvement 1.2: Question Type Heuristic
def classify_question(q):
    q = q.lower()
    if any(x in q for x in ["what is", "about", "overview", "summary", "explain"]):
        return "overview"
    if any(x in q for x in ["dataset", "data", "corpus", "collection"]):
        return "dataset"
    if any(x in q for x in ["result", "accuracy", "performance", "metric", "score"]):
        return "results"
    if any(x in q for x in ["method", "how", "algorithm", "approach"]):
        return "methodology"
    return "general"

def retrieve(query, k=8): # Retrieve more initially to allow filtering
    print(f"\n[PHASE 3.1] QUERY: {query}")
    qtype = classify_question(query)
    print(f"[PHASE 3.1] Q-TYPE: {qtype}")
    
    with open(os.path.join("data", "chunks.json"), 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    index = load_vector_store()
    if index is None:
        return []
    
    query_emb = get_query_embedding(query)
    distances, indices = search_vectors(index, query_emb, k)
    
    candidates = []
    for i, idx in enumerate(indices):
        if idx < len(chunks):
            chunk = chunks[idx]
            raw_score = distances[i]
            
            # Improvement 1.1: Boosting
            boost = SECTION_PRIORITY.get(chunk['section'], 1.0)
            
            # Improvement 1.2: Preferred Sections
            if qtype == "overview" and chunk['section'] in ["Abstract", "Introduction", "Conclusion"]:
                boost *= 0.8 # Lower score is better in L2
            
            final_score = raw_score * boost
            candidates.append((final_score, chunk))

    # Sort by boosted score
    candidates.sort(key=lambda x: x[0])
    
    # Priority 2: Context Sanitization & Filtering
    filtered_chunks = []
    for score, chunk in candidates:
        # Improvement 2.1: Drop low-value
        text = chunk['text']
        if text.count("Figure") > 3 or text.count("Table") > 3:
            continue
        if len(text.split()) < 30: # Too short
            continue
            
        # Improvement 3.2: Confidence Gate (L2 distance threshold)
        if score > 1.9 and len(filtered_chunks) >= 3:
            print(f"[PHASE 3.1] Confidence threshold reached at score {score:.4f}")
            break
            
        filtered_chunks.append(chunk)

    # Limit to top 5 after filtering
    top_chunks = filtered_chunks[:5]
    
    print("[PHASE 3.1] TOP RETRIEVED CHUNKS:")
    for i, c in enumerate(top_chunks):
        print(f"[{i}] section={c['section']} chunk_id={c['chunk_id']}")
    
    return top_chunks

def generate_answer(retrieved_chunks, question):
    """
    PHASE 4.2: Gemini Call with safety guardrails (P3) and sources (P4)
    """
    # Improvement 3.1: Empty Retrieval Guard
    if not retrieved_chunks:
        return {
            "answer": "No relevant context found in the paper to answer this question accurately.",
            "sources": []
        }

    # Improvement 2.2: Context Compression - Reduced for better output
    compressed_contexts = []
    for c in retrieved_chunks[:3]:  # Limit to top 3 chunks for focused context
        compressed_text = c['text'][:800]  # Reduced from 1200
        compressed_contexts.append(f"[{c['section']}]: {compressed_text}")
    
    context_block = "\n\n".join(compressed_contexts)
    
    # Improved Phase 4.1 Prompt - Formatted, structured responses
    prompt = f"""You are a helpful research assistant analyzing an academic paper. 
Your job is to provide clear, well-structured, and comprehensive answers.

**Formatting Guidelines:**
- Use **bold** for key terms and important concepts
- Structure your answer with clear sections when appropriate
- Use bullet points or numbered lists for multiple items
- Write in complete paragraphs with clear explanations
- Always provide a complete answer - never end mid-sentence
- If the context lacks information, say: "The paper doesn't provide enough detail on this topic."

**Response Structure (when applicable):**
- Start with a brief overview/summary
- Provide detailed explanation
- Include specific findings or examples from the paper
- Conclude with key takeaways

Context from the paper:
{context_block}

User's Question: {question}

Your Response (well-formatted and complete):"""

    print(f"[PHASE 4.2] Generating answer. Model: {GENERATIVE_MODEL}")
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GENERATIVE_MODEL,
                contents=prompt,
                config={"max_output_tokens": 2000}
            )
            
            # Improvement 4.1: Return sources with answer
            sources = [{"section": c['section'], "chunk_id": c['chunk_id']} for c in retrieved_chunks]
            
            return {
                "answer": response.text,
                "sources": sources
            }
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"[PHASE 4.2] Quota hit. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
            else:
                return {
                    "answer": f"Not found in the paper (API Error: {str(e)[:100]})",
                    "sources": []
                }
