#!/usr/bin/env python3
"""Example of manual LangSmith tracing configuration."""

import os
from langchain.callbacks import tracing_v2_enabled
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def example_with_manual_tracing() -> None:
    """Example using manual tracing context."""
    try:
        # Option 1: Using context manager
        with tracing_v2_enabled(project_name="genai-data-ai"):
            from genai_tk.core.llm_factory import get_llm
            llm = get_llm()
            response = llm.invoke([HumanMessage(content="Hello with manual tracing!")])
            print(f"Response: {response.content}")

        # Option 2: Using environment variables (your current setup)
        # Just ensure these are set in your .env file:
        # LANGCHAIN_TRACING_V2=true
        # LANGCHAIN_PROJECT=genai-data-ai
        # LANGCHAIN_API_KEY=your_key_here
        
    except Exception as e:
        print(f"Error: {e}")

def check_tracing_status() -> None:
    """Check if tracing is enabled."""
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    api_key_set = bool(os.getenv("LANGCHAIN_API_KEY"))
    
    print(f"🔍 LangSmith Tracing Status:")
    print(f"  LANGCHAIN_TRACING_V2: {'✅ Enabled' if tracing_enabled else '❌ Disabled'}")
    print(f"  LANGCHAIN_API_KEY: {'✅ Set' if api_key_set else '❌ Not Set'}")
    print(f"  Project: {os.getenv('LANGCHAIN_PROJECT', 'Default')}")
    
    if tracing_enabled and api_key_set:
        print("✅ LangSmith tracing should be working!")
    else:
        print("❌ LangSmith tracing is not properly configured")

if __name__ == "__main__":
    check_tracing_status()
    example_with_manual_tracing()