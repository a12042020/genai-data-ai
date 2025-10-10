"""
Document renderer - handles original document display and OCR processing.
"""
from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from ..core.cache_manager import cached_mistral_ocr
from ..core.session_state import is_ocr_complete
from ..utils.display import display_markdown_content, display_pdf
from ..utils.file_handler import format_file_size, save_markdown_to_file


def process_ocr_with_spinner() -> None:
    """Process OCR with spinner (called from Markdown tab)."""
    if st.session_state.get('ocr_complete'):
        return
    
    if not st.session_state.get('current_file_hash'):
        return
        
    file_hash = st.session_state.current_file_hash
    file_bytes = st.session_state.current_file_bytes
    file_type = st.session_state.current_file_type
    
    # Process OCR with cache - spinner will show here
    try:
        markdown_result = cached_mistral_ocr(file_hash, file_bytes, file_type)
        
        if markdown_result:
            st.session_state.markdown_content = markdown_result
            saved_path = save_markdown_to_file(markdown_result, st.session_state.current_file_name)
            st.session_state.saved_path = saved_path
            st.session_state.ocr_complete = True
            st.session_state.ocr_in_progress = False
    except Exception as e:
        st.error(f"❌ OCR Error: {str(e)}")
        st.session_state.ocr_in_progress = False


def render_original_document(file_bytes: bytes, uploaded_file: UploadedFile) -> None:
    """Render original document column with tabs for PDF and Markdown."""
    st.subheader("📄 Original Document")
    
    # Create tabs for original and markdown view
    tab1, tab2 = st.tabs(["📄 Document View", "📝 Markdown View"])
    
    with tab1:
        if uploaded_file.type == "application/pdf":
            display_pdf(file_bytes)
        else:
            st.info(f"📎 **File**: {uploaded_file.name}")
            st.write(f"**Type**: {uploaded_file.type}")
            st.write(f"**Size**: {format_file_size(len(file_bytes))}")
            st.markdown("*Content preview is only available for PDF files*")
    
    with tab2:
        # Process OCR - spinner only appears here
        process_ocr_with_spinner()
        
        if is_ocr_complete() and st.session_state.get('markdown_content'):
            # Display markdown content from OCR
            display_markdown_content(st.session_state.markdown_content)
            
            # Download button
            st.download_button(
                label="⬇️ Download Markdown",
                data=st.session_state.markdown_content,
                file_name=f"{Path(uploaded_file.name).stem}.md",
                mime="text/markdown",
                use_container_width=True
            )
        elif st.session_state.get('ocr_in_progress'):
            st.info("⏳ Processing document with OCR...")
        else:
            st.info("⏳ Ready to process document with OCR")
