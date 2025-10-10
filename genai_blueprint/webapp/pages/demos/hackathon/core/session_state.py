"""
Session state management for Lawlitics application.
"""
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from .hash_utils import get_file_hash


def reset_document_state() -> None:
    """Reset all document-related session state variables."""
    keys_to_reset = [
        'ocr_complete', 'markdown_content', 'extracted_info', 
        'resumed_content', 'kcp_analysis', 'ocr_in_progress',
        'current_file_bytes', 'current_file_type'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]


def initialize_document_processing(file_bytes: bytes, uploaded_file: UploadedFile) -> str:
    """Initialize session state for new document processing.
    
    Returns:
        File hash for the current document
    """
    file_hash = get_file_hash(file_bytes)
    
    # Check if this is a new file
    if st.session_state.get('current_file_hash') != file_hash:
        st.session_state.current_file_name = uploaded_file.name
        st.session_state.current_file_hash = file_hash
        
        # Reset processing state
        reset_document_state()
        
        # Store file info for processing
        st.session_state.current_file_bytes = file_bytes
        st.session_state.current_file_type = uploaded_file.type
        st.session_state.ocr_in_progress = True
        
    return file_hash


def is_ocr_complete() -> bool:
    """Check if OCR processing is complete."""
    return bool(st.session_state.get('ocr_complete'))


def is_extraction_complete() -> bool:
    """Check if legal extraction is complete."""
    return bool(st.session_state.get('extracted_info'))


def is_analysis_complete() -> bool:
    """Check if contract analysis is complete."""
    return bool(st.session_state.get('resumed_content'))


def get_markdown_content() -> str | None:
    """Get processed markdown content."""
    return st.session_state.get('markdown_content')


def get_extracted_info() -> str | None:
    """Get extracted legal information.""" 
    return st.session_state.get('extracted_info')


def get_contract_summary() -> str | None:
    """Get contract summary."""
    return st.session_state.get('resumed_content')


def get_kcp_analysis() -> str | None:
    """Get KCP analysis."""
    return st.session_state.get('kcp_analysis')
