import pdfplumber
import os
import re

def extract_text(pdf_path) -> str:
    """
    PHASE 1.1: PDF -> Text Extraction
    Improved extraction with text cleaning.
    """
    print(f"[PHASE 1.1] Extracting text from: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        return ""

    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"[PHASE 1.1] Document has {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # Clean text: add spaces around merged words
                    # Fix common PDF extraction issues
                    clean_text = text
                    
                    # Add space before capital letters that follow lowercase (merged words)
                    clean_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean_text)
                    
                    # Add space after periods if followed by letter
                    clean_text = re.sub(r'\.([A-Za-z])', r'. \1', clean_text)
                    
                    # Remove excessive newlines
                    clean_text = "\n".join([line.strip() for line in clean_text.splitlines() if line.strip()])
                    
                    full_text += f"\n--- PAGE {i+1} ---\n{clean_text}\n"
                else:
                    print(f"[WARNING] Page {i+1} is empty.")
        
        print(f"[PHASE 1.1] Extraction complete. Total length: {len(full_text)} chars")
        return full_text
    except Exception as e:
        print(f"[ERROR] PDF Extraction failed: {e}")
        return ""
