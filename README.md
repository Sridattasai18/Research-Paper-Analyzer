# Gemini-Only RAG Research Paper Q&A System

## What is RAG?
Retrieval-Augmented Generation (RAG) is a technique that gives an LLM (like Gemini) access to specific data (like your research paper) that it wasn't originally trained on. Instead of relying on its general knowledge, it searches through your document for relevant sections and uses them to construct an answer.

## Why Gemini Embeddings?
We use the Gemini Embedding API to turn text chunks into numbers (vectors) that represent their meaning. This allows us to compare your question to the document's content and find the most relevant parts mathematically.

## Project Flow
PDF Upload → pdfplumber Text Extraction → Chunks → Gemini Embeddings → FAISS local storage → User Question → Question Embedding → Semantic Search → Relevant Context → Gemini LLM Generation → Answer

## Running Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API key in `.env`: `GEMINI_API_KEY=your_key`
3. Run the app: `python app.py`
4. Visit `http://localhost:5000`
