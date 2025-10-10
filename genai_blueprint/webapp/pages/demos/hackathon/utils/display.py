"""
Display utilities for Streamlit UI
"""
import base64

import streamlit as st

from genai_blueprint.webapp.pages.demos.hackathon.config.settings import SCROLL_HEIGHT


def display_pdf(file_bytes: bytes) -> None:
    """
    Display PDF file in an iframe.
    
    Args:
        file_bytes: PDF file content as bytes
    """
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{SCROLL_HEIGHT}" type="application/pdf" style="margin-top: 16px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_markdown_content(content: str) -> None:
    """
    Display markdown content in a scrollable container.
    
    Args:
        content: Markdown content to display
    """
    st.markdown(
        f"""<div style='height: {SCROLL_HEIGHT}px; overflow-y: auto; 
        border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-top: 16px; margin-bottom: 16px;'>
        {content}
        </div>""",
        unsafe_allow_html=True
    )


def display_formatted_json(data: dict) -> None:
    """
    Display JSON data in a formatted, human-readable way.
    
    Args:
        data: Dictionary to display
    """
    content = ""

    if isinstance(data, dict):
        for key, value in data.items():
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
        content = str(data)

    # Display in scrollable container
    st.markdown(
        f"""<div style='height: {SCROLL_HEIGHT}px; overflow-y: auto; 
        border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-top: 16px; margin-bottom: 16px;'>
        {content}
        </div>""",
        unsafe_allow_html=True
    )


def display_json_view(data: dict) -> None:
    """
    Display JSON with native Streamlit component in scrollable container.
    
    Args:
        data: Dictionary to display as JSON
    """
    st.markdown(
        f"""<style>
        div[data-testid="stJson"] {{
            height: {SCROLL_HEIGHT}px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }}
        </style>""",
        unsafe_allow_html=True
    )
    st.json(data, expanded=True)


def display_summary(content: str) -> None:
    """
    Display summary content in a scrollable container.
    
    Args:
        content: Summary content to display
    """
    st.markdown(
        f"""<div style='height: {SCROLL_HEIGHT}px; overflow-y: auto; 
        border: 1px solid #ddd; padding: 15px; border-radius: 5px;margin-top: 16px;'>
        {content}
        </div>""",
        unsafe_allow_html=True
    )

def display_kcp_analysis(content: str) -> None:
    """
    Display KCP analysis content in a scrollable container.
    
    Args:
        content: KCP analysis content to display
    """
    st.markdown(
        f"""<div style='height: {SCROLL_HEIGHT}px; overflow-y: auto; 
        border: 1px solid #ddd; padding: 15px; border-radius: 5px;margin-top: 16px;'>
        {content}
        </div>""",
        unsafe_allow_html=True
    )


def add_spacing() -> None:
    """Add vertical spacing in the UI."""
    st.markdown("<br>", unsafe_allow_html=True)
