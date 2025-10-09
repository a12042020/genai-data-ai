"""
Legal Assistant Agent Demo Page
"""
import os
import json
import base64
from pathlib import Path
from datetime import datetime
import streamlit as st
from mistralai import Mistral
from genai_blueprint.baml_access import extract_legal_information, resume_contract

# Page Configuration
st.set_page_config(
    page_title="Legal Assistant Agent Demo",
    page_icon="⚖️",
    layout="wide"
)

# API Key configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Session State Initialization
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

def display_pdf(file_bytes):
    """Display PDF file in Streamlit app."""
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def save_markdown_to_file(content, filename):
    """Save markdown content to a file."""
    output_dir = Path("extracted_markdowns")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(filename).stem
    output_file = output_dir / f"{base_name}_{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_file

def process_with_mistral_ocr(file_bytes, file_type):
    """Send file to Mistral OCR and retrieve markdown."""
    try:
        client = Mistral(api_key=MISTRAL_API_KEY)

        # Encode file to base64
        base64_file = base64.b64encode(file_bytes).decode('utf-8')

        # Determine MIME type
        mime_types = {
            'application/pdf': 'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        }

        mime_type = mime_types.get(file_type, 'application/pdf')

        # Call Mistral OCR API
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
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

    except Exception as e:
        st.error(f"❌ OCR Error: {str(e)}")
        return None

def main():
    """Main function to run the Streamlit app."""

    st.title("⚖️ Legal Assistant Agent Demo")
    st.markdown("Upload a legal document for automatic analysis")
    st.markdown("---")

    # File upload section
    uploaded_file = st.file_uploader(
        "Upload a legal document",
        type=["pdf", "docx", "pptx"],
        help="Supported formats: PDF, Word, PowerPoint"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

        # Read file bytes ONCE at the beginning
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()

        # Process OCR if needed
        if (st.session_state.current_file_name != uploaded_file.name or 
            not st.session_state.ocr_complete):

            st.session_state.current_file_name = uploaded_file.name
            st.session_state.ocr_complete = False
            st.session_state.markdown_content = None
            st.session_state.extracted_info = None
            st.session_state.resumed_content = None

            # Extract with Mistral OCR
            markdown_result = process_with_mistral_ocr(file_bytes, uploaded_file.type)

            if markdown_result:
                st.session_state.markdown_content = markdown_result
                saved_path = save_markdown_to_file(markdown_result, uploaded_file.name)
                st.session_state.saved_path = saved_path
                st.session_state.ocr_complete = True

        # Display results in three columns
        col1, col2, col3 = st.columns([2, 2, 2])

        # Column 1: Display original document IMMEDIATELY
        with col1:
            st.subheader("📄 Original Document")

            if uploaded_file.type == "application/pdf":
                display_pdf(file_bytes)
            else:
                st.info(f"📎 **File**: {uploaded_file.name}")
                st.write(f"**Type**: {uploaded_file.type}")
                st.write(f"**Size**: {len(file_bytes) / 1024:.2f} KB")
                st.markdown("*Content preview is only available for PDF files*")

        # Column 2: Display extracted legal information (with its own spinner)
        with col2:
            st.subheader("⚖️ Extracted Information")

            if st.session_state.ocr_complete and st.session_state.markdown_content:
                # Only show spinner in this column during extraction
                if st.session_state.extracted_info is None:
                    with st.spinner("⚖️ Extracting legal information..."):
                        try:
                            extracted = extract_legal_information(st.session_state.markdown_content)
                            st.session_state.extracted_info = extracted
                        except Exception as e:
                            st.error(f"❌ Extraction Error: {str(e)}")

                # Display the extracted info with tabs
                if st.session_state.extracted_info:
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📋 Formatted View", "{ } JSON View"])

                    with tab1:
                        # Formatted view with scrollable container
                        extracted = st.session_state.extracted_info

                        # Build HTML content for formatted view
                        content = ""
                        if isinstance(extracted, dict):
                            for key, value in extracted.items():
                                # Format the key nicely
                                display_key = key.replace('_', ' ').title()

                                if isinstance(value, list):
                                    content += f"<p><strong>{display_key}:</strong></p><ul>"
                                    for item in value:
                                        content += f"<li>{item}</li>"
                                    content += "</ul>"
                                elif isinstance(value, dict):
                                    content += f"<p><strong>{display_key}:</strong></p><ul>"
                                    for sub_key, sub_value in value.items():
                                        content += f"<li><strong>{sub_key}:</strong> {sub_value}</li>"
                                    content += "</ul>"
                                else:
                                    content += f"<p><strong>{display_key}:</strong> {value}</p>"
                        else:
                            content = str(extracted)

                        # Display in scrollable container
                        st.markdown(
                            f"""<div style='height: 650px; overflow-y: auto; 
                            border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                            {content}
                            </div>""",
                            unsafe_allow_html=True
                        )

                    with tab2:
                        # JSON view with native Streamlit json component in scrollable container
                        # Use custom CSS to make st.json scrollable
                        st.markdown(
                            """<style>
                            div[data-testid="stJson"] {
                                height: 650px;
                                overflow-y: auto;
                                border: 1px solid #ddd;
                                border-radius: 5px;
                                padding: 10px;
                            }
                            </style>""",
                            unsafe_allow_html=True
                        )
                        st.json(st.session_state.extracted_info, expanded=True)

                    json_str = json.dumps(st.session_state.extracted_info, indent=2, ensure_ascii=False)

                    st.download_button(
                        label="⬇️ Download Extracted Data (JSON)",
                        data=json_str,
                        file_name=f"extracted_{Path(uploaded_file.name).stem}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            else:
                st.info("⏳ Processing document with OCR...")

        # Column 3: Display resumed content (with its own spinner)
        with col3:
            st.subheader("📊 Contract Summary")

            if st.session_state.extracted_info:
                # Only show spinner in this column during summary generation
                if st.session_state.resumed_content is None:
                    with st.spinner("📊 Generating summary..."):
                        try:
                            resumed = resume_contract(st.session_state.extracted_info)
                            st.session_state.resumed_content = resumed
                        except Exception as e:
                            st.error(f"❌ Resume Error: {str(e)}")

                # Display the summary with scrollable container
                if st.session_state.resumed_content:
                    st.markdown(
                        f"""<div style='height: 700px; overflow-y: auto; 
                        border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                        {st.session_state.resumed_content}
                        </div>""",
                        unsafe_allow_html=True
                    )

                    # Download button for summary
                    st.download_button(
                        label="⬇️ Download Summary",
                        data=st.session_state.resumed_content,
                        file_name=f"summary_{Path(uploaded_file.name).stem}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            else:
                st.info("⏳ Waiting for extraction to complete...")

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
