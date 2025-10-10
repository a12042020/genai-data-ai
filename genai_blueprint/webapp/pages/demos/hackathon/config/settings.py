"""
Configuration and settings for Legal Assistant Agent
"""
import os

# API Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Legal Assistant Agent Demo",
    "page_icon": "⚖️",
    "layout": "wide"
}

# File Configuration
SUPPORTED_FILE_TYPES = ["pdf", "docx", "pptx"]
OUTPUT_DIR = "extracted_markdowns"
MAX_FILE_SIZE_MB = 200

# MIME Types Mapping
MIME_TYPES = {
    'application/pdf': 'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
}

# UI Configuration - All same height for uniformity
SCROLL_HEIGHT = 800  # Single value for all columns

# OCR Model
OCR_MODEL = "mistral-ocr-latest"