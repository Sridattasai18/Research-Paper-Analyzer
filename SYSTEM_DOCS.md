# Research Paper RAG System - Final Documentation

## ✅ System Status: FULLY OPERATIONAL

### 🎯 Current Configuration
- **Model:** `gemini-flash-latest` (verified compatible)
- **API Key:** Active and working
- **Embeddings:** Local (sentence-transformers) - NO API CALLS
- **Server:** Running on http://localhost:5000

### 📊 System Architecture

#### Phase 1: Data Pipeline
- **PDF Extraction** (`services/pdf_loader.py`): Extracts text with page markers
- **Chunking** (`services/chunker.py`): 700-token chunks with section detection
  - Detects: Abstract, Introduction, Methodology, Results, Conclusion

#### Phase 2: Vector Store
- **Embeddings** (`services/embeddings.py`): Local model (all-MiniLM-L6-v2, 384-dim)
- **FAISS Index** (`services/vector_store.py`): Persistent L2 index

#### Phase 3-4: Retrieval & Generation
- **Smart Retrieval** (`services/rag_pipeline.py`):
  - Section-aware boosting (Abstract/Intro/Conclusion prioritized)
  - Question type classification (overview/dataset/results/methodology)
  - Noise filtering (removes figure captions, tables)
  - Confidence gating (threshold: 1.9)
- **LLM Generation**: Max 300 tokens, context-strict prompting

#### Phase 5: Flask API
- `POST /ingest` - Upload and index PDF
- `POST /ask` - Ask questions (returns answer + sources)
- `POST /debug/retrieval` - Debug endpoint for retrieval inspection
- `GET /health` - Health check

### 🎨 Frontend Features
- Single-page application (SPA)
- Drag-and-drop PDF upload
- Real-time chat interface
- **Source citations** displayed with each answer
- Typing indicators and smooth animations

### 🛡️ Safety & Efficiency Features
1. **Token Optimization:**
   - Local embeddings (no API calls for vectors)
   - Context compression (~40% reduction)
   - 300-token response limit
   
2. **Error Handling:**
   - Exponential backoff for 429 errors
   - Empty retrieval guards
   - Confidence thresholds to prevent hallucination

3. **Quality Improvements:**
   - Section-aware retrieval
   - Question type heuristics
   - Low-value chunk filtering

### 📁 Project Structure
```
rag/
├── app.py                  # Flask entry point
├── config.py               # API key & settings
├── requirements.txt        # Dependencies
├── .env                    # API key (gitignored)
├── routes/
│   ├── ingestion.py       # /ingest endpoint
│   └── query.py           # /ask & /debug endpoints
├── services/
│   ├── pdf_loader.py      # PDF text extraction
│   ├── chunker.py         # Smart chunking
│   ├── embeddings.py      # Local embeddings
│   ├── vector_store.py    # FAISS management
│   └── rag_pipeline.py    # Retrieval + LLM
├── templates/
│   └── index.html         # SPA frontend
└── static/
    ├── app.js             # Frontend logic
    └── style.css          # Styling
```

### 🚀 Usage

#### Start Server
```powershell
python app.py
```

#### Upload Document
1. Navigate to http://localhost:5000
2. Drag & drop PDF or click to browse
3. Wait for "Success! Entering chat..."

#### Ask Questions
- System automatically classifies question type
- Retrieves relevant sections
- Generates context-aware answer
- Shows source citations

#### Debug Retrieval (Optional)
```bash
curl -X POST http://localhost:5000/debug/retrieval \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main contribution?"}'
```

### 🎓 Quality Gate Questions
Test with these 10 questions:
1. What dataset was used?
2. What evaluation metrics are reported?
3. What is the baseline model?
4. What is the main contribution?
5. What are the limitations?
6. What future work is suggested?
7. What are the key results?
8. What assumptions are made?
9. What hyperparameters are used?
10. What domain is this paper in?

### 🔧 Troubleshooting

**Issue:** "Not found in the paper"
- **Check:** Terminal logs for `[PHASE 3.1]` to see retrieved chunks
- **Fix:** Question might be too specific or not in the paper

**Issue:** API Error 429
- **Cause:** Rate limit hit
- **Fix:** System auto-retries with exponential backoff

**Issue:** Truncated responses
- **Cause:** 300-token limit (by design for efficiency)
- **Fix:** Increase `max_output_tokens` in `rag_pipeline.py` if needed

### 📊 Performance Metrics
- **Embedding:** Local (0 API calls)
- **Retrieval:** <100ms (FAISS)
- **Generation:** ~2-3s (API call)
- **Total:** ~3-4s per question

### 🎯 Next Steps (Optional Enhancements)
1. Multi-paper support (add paper_id to chunks)
2. Conversation history
3. Export answers to PDF
4. Advanced section detection (ML-based)
5. Streaming responses

---

**System built following the Anti-Debug-Loop Roadmap**
- ✅ Phase 0: Modular, single-responsibility code
- ✅ Phase 1: Deterministic data pipeline
- ✅ Phase 2: Local embeddings + FAISS
- ✅ Phase 3: Smart retrieval with logging
- ✅ Phase 4: Context-strict LLM
- ✅ Phase 5: Thin Flask glue
- ✅ Priorities 1-4: Quality improvements implemented
