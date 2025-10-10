"""
Document processor - Main orchestrator for Lawlitics document processing.

This module coordinates the document processing pipeline by delegating to
specialized components for each responsibility.
"""
from streamlit.runtime.uploaded_file_manager import UploadedFile

from ..core.session_state import initialize_document_processing
from .analysis_renderer import render_contract_summary
from .document_renderer import render_original_document
from .extraction_renderer import render_extracted_information


def process_document(file_bytes: bytes, uploaded_file: UploadedFile) -> None:
    """Initialize document processing pipeline.
    
    This function serves as the main entry point for document processing,
    setting up session state and coordinating the processing workflow.
    
    Args:
        file_bytes: File content as bytes
        uploaded_file: Streamlit UploadedFile object
    """
    # Initialize session state and get file hash
    initialize_document_processing(file_bytes, uploaded_file)


# Export the render functions for backward compatibility
__all__ = [
    'process_document',
    'render_original_document', 
    'render_extracted_information',
    'render_contract_summary'
]
