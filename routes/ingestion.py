from flask import Blueprint, request, jsonify
import os
from services.pdf_loader import extract_text
from services.chunker import chunk_text
from services.embeddings import get_embeddings
from services.vector_store import build_vector_store
from config import PDF_DIR

ingest_bp = Blueprint('ingest', __name__)

@ingest_bp.route('/ingest', methods=['POST'])
def ingest_document():
    """
    PHASE 5: Thin, dumb glue for ingestion.
    """
    print("[PHASE 5] POST /ingest hit")
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    filepath = os.path.join(PDF_DIR, file.filename)
    file.save(filepath)
    
    # Sequential execution of phases 1-2
    text = extract_text(filepath)
    chunks = chunk_text(text)
    
    chunk_texts = [c['text'] for c in chunks]
    embeddings = get_embeddings(chunk_texts)
    
    build_vector_store(embeddings)
    
    return jsonify({
        "status": "success",
        "chunks": len(chunks)
    }), 200
