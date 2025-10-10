"""
Document processing component
"""
import json
import streamlit as st
from pathlib import Path
from genai_blueprint.webapp.pages.demos.hackathon.utils.mistral_ocr import process_with_mistral_ocr
from genai_blueprint.webapp.pages.demos.hackathon.utils.file_handler import save_markdown_to_file, format_file_size, load_kcp_file
from genai_blueprint.webapp.pages.demos.hackathon.utils.display import (
    display_pdf,
    display_formatted_json,
    display_markdown_content,
    display_json_view,
    display_summary,
    display_kcp_analysis
)
from genai_blueprint.baml_access import extract_legal_information, resume_contract, analyse_contract_kcp

def process_document(file_bytes: bytes, uploaded_file) -> None:
    """
    Process uploaded document through OCR pipeline.
    
    Args:
        file_bytes: File content as bytes
        uploaded_file: Streamlit UploadedFile object
    """
    # Check if this is a new file or if OCR is already done
    if (st.session_state.get('current_file_name') != uploaded_file.name or 
        not st.session_state.get('ocr_complete')):
        
        st.session_state.current_file_name = uploaded_file.name
        st.session_state.ocr_complete = False
        st.session_state.markdown_content = None
        st.session_state.extracted_info = None
        st.session_state.resumed_content = None
        
        # Extract with Mistral OCR
        try:
            markdown_result = process_with_mistral_ocr(file_bytes, uploaded_file.type)
            
            if markdown_result:
                st.session_state.markdown_content = markdown_result
                saved_path = save_markdown_to_file(markdown_result, uploaded_file.name)
                st.session_state.saved_path = saved_path
                st.session_state.ocr_complete = True
        except Exception as e:
            st.error(f"❌ OCR Error: {str(e)}")


def render_original_document(file_bytes: bytes, uploaded_file) -> None:
    """
    Render original document column with tabs for PDF and Markdown.
    
    Args:
        file_bytes: File content as bytes
        uploaded_file: Streamlit UploadedFile object
    """
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
        if st.session_state.get('ocr_complete') and st.session_state.get('markdown_content'):
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
        else:
            st.info("⏳ Processing document with OCR...")


def render_extracted_information() -> None:
    """Render extracted information column with tabs."""
    st.subheader("⚖️ Extracted Information")

    if st.session_state.get('ocr_complete') and st.session_state.get('markdown_content'):
        # Extract legal information if not done yet
        if st.session_state.get('extracted_info') is None:
            with st.spinner("⚖️ Extracting legal information..."):
                try:
                    extracted = extract_legal_information(st.session_state.markdown_content)
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


def render_contract_summary() -> None:
    """Render contract summary column with tab."""
    st.subheader("📊 Contract Analysis")
    
    if st.session_state.get('extracted_info'):
        # Generate summary if not done yet
        if st.session_state.get('resumed_content') is None:
            with st.spinner("📊 Generating summary..."):
                try:
                    resumed = resume_contract(st.session_state.extracted_info)
                    st.session_state.resumed_content = resumed
                except Exception as e:
                    st.error(f"❌ Resume Error: {str(e)}")
                    return
        
        # Display in tab for consistency
        tab1, tab2 = st.tabs(["📋 Summary View", "🔍 KCP Analysis"])
        
        with tab1:
            # Display summary
            if st.session_state.get('resumed_content'):
                display_summary(st.session_state.resumed_content)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Summary",
                    data=st.session_state.resumed_content,
                    file_name=f"summary_{Path(st.session_state.uploaded_file.name).stem}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        with tab2:
            # Generate KCP analysis if not done yet
            if st.session_state.get('kcp_analysis') is None:
                with st.spinner("🔍 Analyzing contract with KCP..."):
                    try:
                        # Load KCP file
                        kcp_content = load_kcp_file("kcp_example.md")
                        
                        # Perform KCP analysis
                        kcp_result = analyse_contract_kcp(
                            st.session_state.extracted_info,
                            kcp_content
                        )
                        st.session_state.kcp_analysis = kcp_result
                    except FileNotFoundError as e:
                        st.error(f"❌ KCP File Error: {str(e)}")
                        st.info("💡 Please ensure 'kcp/kcp_example.md' exists in your project directory")
                        return
                    except Exception as e:
                        st.error(f"❌ KCP Analysis Error: {str(e)}")
                        return
            
            # Display KCP analysis
            if st.session_state.get('kcp_analysis'):
                display_summary(st.session_state.kcp_analysis)

                st.download_button(
                    label="⬇️ Download KCP Analysis",
                    data=st.session_state.kcp_analysis,
                    file_name=f"kcp_analysis_{Path(st.session_state.uploaded_file.name).stem}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
    else:
        st.info("⏳ Waiting for extraction to complete...")

def render_kcp_analysis() -> None:
    """Render KCP analysis column with tab."""
    st.subheader("🔍 KCP Analysis")
    
    if st.session_state.get('extracted_info'):
        # Placeholder for KCP analysis logic
        display_kcp_analysis("KCP Analysis feature coming soon...")
    else:
        st.info("⏳ Waiting for extraction to complete...")
