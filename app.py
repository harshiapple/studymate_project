import streamlit as st
import traceback
from pdf_utils import extract_text_from_pdf, chunk_text
from vector_store import create_vector_index, search_index
from qa_engine import generate_answer

# Configure page
st.set_page_config(page_title="📘 StudyMate", layout="centered")
st.title("📘 StudyMate - Ask Questions from Your PDF")

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = None
if 'chunks' not in st.session_state:
    st.session_state.chunks = None
if 'processed_file' not in st.session_state:
    st.session_state.processed_file = None

uploaded_file = st.file_uploader("📤 Upload a PDF file", type="pdf")

if uploaded_file:
    # Check if this is a new file or the same file
    if (st.session_state.processed_file is None or 
        st.session_state.processed_file != uploaded_file.name):
        
        try:
            st.success("✅ PDF uploaded. Extracting text...")
            
            # Extract text from PDF
            text = extract_text_from_pdf(uploaded_file)
            
            # Validate extracted text
            if not text or len(text.strip()) == 0:
                st.error("❌ No text could be extracted from the PDF. Please check if the PDF contains readable text.")
                st.stop()
            
            # Chunk the text
            chunks = chunk_text(text)
            
            # Validate chunks
            if not chunks or len(chunks) == 0:
                st.error("❌ Could not create text chunks. Please try a different PDF.")
                st.stop()
            
            st.info(f"📄 PDF split into {len(chunks)} chunks.")
            st.success("✅ Creating semantic search index...")
            
            # Create vector index
            index_result = create_vector_index(chunks)
            
            # Handle different return formats from create_vector_index
            if isinstance(index_result, tuple):
                index = index_result[0]  # Assuming first element is the index
            else:
                index = index_result
            
            # Validate index creation
            if index is None:
                st.error("❌ Failed to create search index. Please try again.")
                st.stop()
            
            # Store in session state
            st.session_state.index = index
            st.session_state.chunks = chunks
            st.session_state.processed_file = uploaded_file.name
            
            st.success("✅ PDF processed successfully! You can now ask questions.")
            
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            st.error("Please try uploading a different PDF file.")
            # Optionally show detailed error for debugging
            with st.expander("Show detailed error"):
                st.code(traceback.format_exc())
            st.stop()

# Question input and processing
if st.session_state.index is not None and st.session_state.chunks is not None:
    question = st.text_input("💬 Ask a question about your PDF")
    
    if st.button("🔍 Get Answer"):
        if not question or len(question.strip()) == 0:
            st.warning("⚠️ Please enter a question first.")
        else:
            try:
                with st.spinner("🔎 Thinking..."):
                    # Search for relevant chunks
                    matched_chunks = search_index(
                        st.session_state.index, 
                        question, 
                        st.session_state.chunks
                    )
                    
                    # Validate search results
                    if not matched_chunks:
                        st.warning("⚠️ No relevant information found for your question. Try rephrasing it.")
                    else:
                        # Create context from matched chunks
                        context = " ".join(matched_chunks)
                        
                        # Generate answer
                        answer = generate_answer(context, question)
                        
                        # Validate answer
                        if not answer or len(answer.strip()) == 0:
                            st.warning("⚠️ Could not generate an answer. Try asking a different question.")
                        else:
                            st.subheader("🧠 Answer:")
                            st.write(answer)
                            
                            # Optionally show matched chunks for transparency
                            with st.expander("📄 Show relevant text chunks"):
                                for i, chunk in enumerate(matched_chunks, 1):
                                    st.text_area(f"Chunk {i}", chunk, height=100)
                
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
                with st.expander("Show detailed error"):
                    st.code(traceback.format_exc())

else:
    st.info("👆 Please upload a PDF file to get started.")
