from flask import Blueprint, request, jsonify
from services.rag_pipeline import retrieve, generate_answer
import os
import json

query_bp = Blueprint('query', __name__)

@query_bp.route('/ask', methods=['POST'])
def ask_question():
    print("[PHASE 5] POST /ask hit")
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question"}), 400
    
    retrieved = retrieve(question)
    result = generate_answer(retrieved, question)
    
    # result is a dict now: {"answer": "...", "sources": [...]}
    return jsonify(result), 200

# Improvement 4.2: /debug/retrieval endpoint
@query_bp.route('/debug/retrieval', methods=['POST'])
def debug_retrieval():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question"}), 400
        
    retrieved = retrieve(question, k=10)
    
    debug_info = {
        "query": question,
        "results_count": len(retrieved),
        "top_match_section": retrieved[0]['section'] if retrieved else None,
        "retrieved_nodes": [
            {
                "chunk_id": r['chunk_id'],
                "section": r['section'],
                "text_snippet": r['text'][:100] + "..."
            } for r in retrieved
        ]
    }
    return jsonify(debug_info), 200
