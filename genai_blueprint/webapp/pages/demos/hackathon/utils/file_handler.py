"""
File handling utilities
"""
from datetime import datetime
from pathlib import Path

from genai_blueprint.webapp.pages.demos.hackathon.config.settings import OUTPUT_DIR


def save_markdown_to_file(content: str, filename: str) -> Path:
    """
    Save markdown content to a file.
    
    Args:
        content: Markdown content to save
        filename: Original filename
        
    Returns:
        Path to saved file
    """
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(filename).stem
    output_file = output_dir / f"{base_name}_{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_file

def load_kcp_file(filename: str = "kcp_example.md") -> str:
    """
    Load KCP markdown file from kcp directory.
    
    Args:
        filename: Name of the KCP file to load
        
    Returns:
        Content of the KCP file
        
    Raises:
        FileNotFoundError: If KCP file doesn't exist
    """
    kcp_dir = Path("kcp")
    kcp_file = kcp_dir / filename

    if not kcp_file.exists():
        raise FileNotFoundError(f"KCP file not found: {kcp_file}")

    with open(kcp_file, 'r', encoding='utf-8') as f:
        return f.read()

def get_recent_files(limit: int = 10) -> list:
    """
    Get list of recent extracted files.
    
    Args:
        limit: Maximum number of files to return
        
    Returns:
        List of Path objects
    """
    output_dir = Path(OUTPUT_DIR)

    if not output_dir.exists():
        return []

    files = sorted(
        output_dir.glob("*.md"), 
        key=lambda f: f.stat().st_mtime, 
        reverse=True
    )

    return files[:limit]


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
