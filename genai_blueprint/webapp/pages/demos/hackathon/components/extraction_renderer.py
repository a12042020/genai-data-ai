"""
Extraction renderer - handles legal information extraction display.
"""
import json
from pathlib import Path

import streamlit as st

from ..core.cache_manager import cached_legal_extraction
from ..core.hash_utils import get_content_hash
from ..core.session_state import get_markdown_content, is_ocr_complete
from ..utils.display import display_formatted_json, display_json_view


def render_extracted_information() -> None:
    """Render extracted information column with tabs."""
    st.subheader("⚖️ Extracted Information")

    if is_ocr_complete() and get_markdown_content():
        # Show extraction cache status
        if st.session_state.get('extracted_info'):
            st.success("⚡ Using cached extraction result (instant!)")
        
        # Extract legal information if not done yet
        if st.session_state.get('extracted_info') is None:
            try:
                markdown_content = get_markdown_content()
                content_hash = get_content_hash(markdown_content)
                extracted = cached_legal_extraction(content_hash, markdown_content)
                st.session_state.extracted_info = extracted
            except Exception as e:
                st.error(f"❌ Extraction Error: {str(e)}")
                return
        
        # Display tabs
        if st.session_state.get('extracted_info'):
            tab1, tab2 = st.tabs(["{ } JSON View", "📋 Formatted View"])
            
            with tab1:
                display_json_view(st.session_state.extracted_info)
                
            with tab2:
                display_formatted_json(st.session_state.extracted_info)
            
            # Download button
            json_str = json.dumps(st.session_state.extracted_info, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Download Extracted Data (JSON)",
                data=json_str,
                file_name=f"extracted_{Path(st.session_state.uploaded_file.name).stem}.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("⏳ Processing document with OCR...")
