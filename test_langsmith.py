#!/usr/bin/env python3
"""Test script to verify LangSmith tracing is working."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_langsmith_config() -> None:
    """Check LangSmith configuration."""
    print("🔍 Checking LangSmith Configuration...")
    print(f"LANGCHAIN_API_KEY: {'✅ SET' if os.getenv('LANGCHAIN_API_KEY') else '❌ NOT SET'}")
    print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2', '❌ NOT SET')}")
    print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT', '❌ NOT SET')}")
    print(f"LANGCHAIN_ENDPOINT: {os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com (default)')}")
    print()


def test_langsmith_tracing() -> None:
    """Test LangSmith tracing with a simple LLM call."""
    try:
        from langchain_core.messages import HumanMessage
        from langchain_openai import ChatOpenAI

        print("🧪 Testing LangSmith tracing...")

        # Create a simple LLM instance
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # Make a simple call
        response = llm.invoke([HumanMessage(content="Say 'LangSmith test successful!'")])

        print(f"✅ LLM Response: {response.content}")
        print("🔗 Check your LangSmith dashboard at: https://smith.langchain.com/")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have langchain-openai installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check your API keys and internet connection")


def test_langsmith_client() -> None:
    """Test direct LangSmith client connection."""
    try:
        from langsmith import Client

        print("🔌 Testing LangSmith client connection...")
        client = Client()

        # Try to get user info - this will fail if API key is invalid
        user_info = client.info
        print(f"✅ Connected to LangSmith as: {user_info}")

    except ImportError:
        print("❌ LangSmith client not available")
    except Exception as e:
        print(f"❌ LangSmith client error: {e}")
        print("💡 Check your LANGCHAIN_API_KEY")


if __name__ == "__main__":
    check_langsmith_config()
    test_langsmith_client()
    test_langsmith_tracing()
