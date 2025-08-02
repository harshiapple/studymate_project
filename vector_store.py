import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_index(chunks):
    if not chunks:
        return None, None, []
    
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings, dtype=np.float32)
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    return index, embeddings, chunks

def search_index(index, question, chunks, k=3):
    if not question or not chunks:
        return []
    
    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding, dtype=np.float32)
    
    k = min(k, len(chunks))
    distances, indices = index.search(question_embedding, k)
    
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]
