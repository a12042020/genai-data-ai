"""
Hash utilities for content identification and caching.
"""
import hashlib


def get_file_hash(file_bytes: bytes) -> str:
    """Generate MD5 hash for file content."""
    return hashlib.md5(file_bytes).hexdigest()


def get_content_hash(content: str) -> str:
    """Generate MD5 hash for text content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def get_analysis_hash(extracted_info: str, kcp_content: str) -> str:
    """Generate hash for KCP analysis caching."""
    combined_content = f"{extracted_info}|{kcp_content}"
    return get_content_hash(combined_content)
