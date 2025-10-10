"""
Legal Assistant Agent Demo - Main Application
"""

import streamlit as st

from genai_blueprint.webapp.pages.demos.hackathon.components.document_processor import (
    process_document,
    render_contract_summary,
    render_extracted_information,
    render_original_document,
)
from genai_blueprint.webapp.pages.demos.hackathon.config.settings import PAGE_CONFIG, SUPPORTED_FILE_TYPES


def initialize_session_state() -> None:
    """Initialize all session state variables."""
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'markdown_content' not in st.session_state:
        st.session_state.markdown_content = None
    if 'extracted_info' not in st.session_state:
        st.session_state.extracted_info = None
    if 'resumed_content' not in st.session_state:
        st.session_state.resumed_content = None
    if 'saved_path' not in st.session_state:
        st.session_state.saved_path = None
    if 'ocr_complete' not in st.session_state:
        st.session_state.ocr_complete = False
    if 'current_file_name' not in st.session_state:
        st.session_state.current_file_name = None


def main() -> None:
    """Main application function."""

    # Configure page
    st.set_page_config(**PAGE_CONFIG)

    # Initialize session state
    initialize_session_state()

    # Sidebar with cache controls
    with st.sidebar:
        st.header("🛠️ Cache Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear Cache", help="Clear all cached results"):
                st.cache_data.clear()
                st.cache_resource.clear()
                # Clear session state
                for key in ['ocr_complete', 'markdown_content', 'extracted_info', 'resumed_content', 'kcp_analysis']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("All caches cleared!")
        
        with col2:
            if st.button("🔄 Force Refresh", help="Force refresh current document"):
                # Clear session state for current document
                for key in ['ocr_complete', 'markdown_content', 'extracted_info', 'resumed_content', 'kcp_analysis']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Document refreshed!")
        
        # Show current cache status
        st.subheader("📊 Cache Status")
        
        # Count cached items
        cache_count = 0
        cache_items = []
        
        if st.session_state.get('ocr_complete'):
            cache_count += 1
            cache_items.append("✓ OCR Result")
        
        if st.session_state.get('extracted_info'):
            cache_count += 1
            cache_items.append("✓ Legal Extraction")
            
        if st.session_state.get('resumed_content'):
            cache_count += 1
            cache_items.append("✓ Contract Summary")
            
        if st.session_state.get('kcp_analysis'):
            cache_count += 1
            cache_items.append("✓ KCP Analysis")
        
        st.metric("Cached Results", cache_count)
        
        if cache_items:
            st.success("\n".join(cache_items))
        else:
            st.info("No cached results yet")
        
        # Show benefits
        st.info("📋 **Cache Benefits:**\n- OCR: Instant reload\n- Analysis: Skip API calls\n- Cost: Reduced tokens")

    # Main content
    st.title("⚖️ Lawlytics")
    st.markdown("Upload a legal document for automatic analysis")
    st.markdown("---")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload a legal document",
        type=SUPPORTED_FILE_TYPES,
        help="Supported formats: PDF, Word, PowerPoint"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

        # Read file bytes once
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()

        # Process document
        process_document(file_bytes, uploaded_file)

        # Display in three columns
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            render_original_document(file_bytes, uploaded_file)

        with col2:
            render_extracted_information()

        with col3:
            render_contract_summary()

    else:
        st.info("👆 Upload a legal document to start automatic processing")

        # Instructions
        st.markdown("""
        ### 📋 How it works
        
        1. **Upload** a legal document (PDF, DOCX, or PPTX)
        2. The document is **displayed immediately** in the first column
        3. The system **processes in parallel**:
           - OCR extraction (silent, in background)
           - Legal information extraction (spinner in column 2)
           - Contract summary generation (spinner in column 3)
        4. **Review** the results as they become available
        
        ### 🔧 Setup
        
        Set your Mistral API key as an environment variable:
        ```bash
        export MISTRAL_API_KEY="your-api-key-here"
        ```
        """)


if __name__ == "__main__":
    main()
