"""
Cache management for Lawlitics operations.
"""
from typing import Any, Callable, Tuple

import streamlit as st

from genai_blueprint.baml_access import analyse_contract_kcp, extract_legal_information, resume_contract
from genai_blueprint.webapp.pages.demos.hackathon.utils.mistral_ocr import process_with_mistral_ocr


# Cache functions - optimized for speed
@st.cache_resource(show_spinner="🔍 Processing OCR (first time only)...")
def cached_mistral_ocr(file_hash: str, file_bytes: bytes, file_type: str) -> str:
    """Cache OCR results - most expensive operation."""
    return process_with_mistral_ocr(file_bytes, file_type)


@st.cache_data(ttl=3600, show_spinner="⚖️ Extracting legal information (first time only)...")
def cached_legal_extraction(content_hash: str, markdown_content: str) -> str:
    """Cache legal extraction results."""
    return extract_legal_information(markdown_content)


@st.cache_data(ttl=1800, show_spinner="📊 Generating summary (first time only)...")
def cached_contract_summary(info_hash: str, extracted_info: str) -> str:
    """Cache contract summary results."""
    return resume_contract(extracted_info)


@st.cache_data(ttl=1800, show_spinner="🔍 Analyzing KCP (first time only)...")
def cached_kcp_analysis(analysis_hash: str, extracted_info: str, kcp_content: str) -> str:
    """Cache KCP analysis results."""
    return analyse_contract_kcp(extracted_info, kcp_content)


# Fast cache check functions
def is_ocr_cached(file_hash: str) -> bool:
    """Check if OCR result is already cached without triggering computation."""
    try:
        cache_key = f"cached_mistral_ocr:{file_hash}"
        return cache_key in st.session_state.get('_streamlit_cache_hits', set())
    except Exception:
        return False


def get_cached_result_fast(cache_func: Callable, *args) -> Tuple[bool, Any]:
    """Try to get cached result fast, return (is_cached, result)."""
    try:
        result = cache_func(*args)
        return True, result
    except Exception:
        return False, None
