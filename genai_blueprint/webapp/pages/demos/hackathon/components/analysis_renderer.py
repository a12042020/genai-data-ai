"""
Analysis renderer - handles contract analysis and KCP analysis display.
"""
from pathlib import Path

import streamlit as st

from ..core.cache_manager import cached_contract_summary, cached_kcp_analysis
from ..core.hash_utils import get_analysis_hash, get_content_hash
from ..core.session_state import get_extracted_info, is_extraction_complete
from ..utils.display import display_summary
from ..utils.file_handler import load_kcp_file


def render_contract_summary() -> None:
    """Render contract summary column with tab."""
    st.subheader("📊 Contract Analysis")
    
    if is_extraction_complete():
        extracted_info = get_extracted_info()
        
        # Generate summary if not done yet
        if st.session_state.get('resumed_content') is None:
            try:
                info_hash = get_content_hash(extracted_info)
                resumed = cached_contract_summary(info_hash, extracted_info)
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
            _render_kcp_analysis_tab(extracted_info)
            
    else:
        st.info("⏳ Waiting for extraction to complete...")


def _render_kcp_analysis_tab(extracted_info: str) -> None:
    """Render KCP analysis tab content."""
    # Generate KCP analysis if not done yet
    if st.session_state.get('kcp_analysis') is None:
        try:
            # Load KCP file
            kcp_content = load_kcp_file("kcp_example.md")
            
            # Generate hash for caching
            analysis_hash = get_analysis_hash(extracted_info, kcp_content)
            
            # Perform KCP analysis with cache
            kcp_result = cached_kcp_analysis(analysis_hash, extracted_info, kcp_content)
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
