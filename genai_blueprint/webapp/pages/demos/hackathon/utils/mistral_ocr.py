"""
OCR processing with Mistral API
"""
import base64
from mistralai import Mistral
from genai_blueprint.webapp.pages.demos.hackathon.config.settings import MISTRAL_API_KEY, MIME_TYPES, OCR_MODEL


def process_with_mistral_ocr(file_bytes: bytes, file_type: str) -> str:
    """
    Send file to Mistral OCR and retrieve markdown.
    
    Args:
        file_bytes: File content as bytes
        file_type: MIME type of the file
        
    Returns:
        Extracted markdown content
        
    Raises:
        Exception: If OCR processing fails
    """
    client = Mistral(api_key=MISTRAL_API_KEY)

    # Encode file to base64
    base64_file = base64.b64encode(file_bytes).decode('utf-8')

    # Get MIME type
    mime_type = MIME_TYPES.get(file_type, 'application/pdf')

    # Call Mistral OCR API
    ocr_response = client.ocr.process(
        model=OCR_MODEL,
        document={
            "type": "document_url",
            "document_url": f"data:{mime_type};base64,{base64_file}"
        },
        include_image_base64=False
    )

    # Combine markdown from all pages
    markdown_content = ""
    for page in ocr_response.pages:
        markdown_content += page.markdown + "\n\n"

    return markdown_content.strip()
