import json
import os
import re

# Section patterns - improved detection
SECTION_PATTERNS = [
    (r'(?i)^abstract', "Abstract"),
    (r'(?i)^1[\.\s]+introduction', "Introduction"),
    (r'(?i)^introduction', "Introduction"),
    (r'(?i)^2[\.\s]+(related|background)', "Background"),
    (r'(?i)^3[\.\s]+(method|approach|proposed)', "Methodology"),
    (r'(?i)^(method|approach|proposed)', "Methodology"),
    (r'(?i)^4[\.\s]+(experiment|result|evaluation)', "Results"),
    (r'(?i)^(experiment|result|evaluation)', "Results"),
    (r'(?i)^5[\.\s]+(discussion|analysis)', "Discussion"),
    (r'(?i)^(conclusion|summary|future)', "Conclusion"),
    (r'(?i)^references', "References"),
    (r'(?i)^appendix', "Appendix")
]

def detect_section(text):
    """Detect section from text start."""
    first_line = text.strip().split('\n')[0] if text.strip() else ""
    for pattern, name in SECTION_PATTERNS:
        if re.search(pattern, first_line):
            return name
    return None

def chunk_text(full_text, chunk_size=500, overlap=75):
    """
    PHASE 1.2: Deterministic Chunking
    Smaller chunks for better retrieval precision.
    """
    print(f"[PHASE 1.2] Starting chunking. Text length: {len(full_text)}")
    
    # Split by pages
    pages = re.split(r'--- PAGE \d+ ---', full_text)
    
    chunks = []
    current_section = "Abstract"  # Start with Abstract assumption for first pages
    chunk_id = 0
    
    for page_num, page_text in enumerate(pages):
        if not page_text.strip():
            continue
            
        # Try to detect section
        detected = detect_section(page_text)
        if detected:
            current_section = detected
        elif page_num > 3 and current_section == "Abstract":
            current_section = "General"  # Move past abstract after page 3
        
        # Skip references section
        if current_section == "References":
            continue
        
        # Word-based chunking
        words = page_text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if len(chunk_words) < 30:  # Skip tiny chunks
                continue
                
            chunk_content = " ".join(chunk_words)
            
            chunks.append({
                "chunk_id": chunk_id,
                "section": current_section,
                "page": page_num,
                "text": chunk_content,
                "token_est": len(chunk_words)
            })
            chunk_id += 1

    print(f"[PHASE 1.2] Produced {len(chunks)} chunks.")
    
    # Save chunks
    output_path = os.path.join("data", "chunks.json")
    os.makedirs("data", exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    print(f"[PHASE 1.2] Chunks saved to {output_path}")
    return chunks
