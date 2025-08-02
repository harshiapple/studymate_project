import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file):
    doc = None
    try:
        file.seek(0)
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
        return re.sub(r'\s+', ' ', text.strip())
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")
    finally:
        if doc:
            doc.close()

def chunk_text(text, chunk_size=500, overlap=50):
    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to break at sentence end
        if end < len(text):
            sentence_end = max(text.rfind('.', start, end), 
                             text.rfind('!', start, end), 
                             text.rfind('?', start, end))
            if sentence_end > start:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap if end < len(text) else len(text)
    
    return chunks
