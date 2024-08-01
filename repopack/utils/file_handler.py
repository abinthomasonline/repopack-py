import os
import chardet
from typing import List, Dict, Any

def is_binary(file_path: str) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read()
            return False
    except:
        return True

def sanitize_files(file_paths: List[str], root_dir: str, config: Dict[str, Any]) -> List[Dict[str, str]]:
    """Sanitize files based on the given configuration."""
    sanitized_files = []
    for file_path in file_paths:
        full_path = os.path.join(root_dir, file_path)
        if not is_binary(full_path):
            content = sanitize_file(full_path, config)
            if content:
                sanitized_files.append({"path": file_path, "content": content})
    return sanitized_files

def sanitize_file(file_path: str, config: Dict[str, Any]) -> str:
    """Sanitize a single file."""
    with open(file_path, 'rb') as f:
        raw_content = f.read()
    
    encoding = chardet.detect(raw_content)['encoding'] or 'utf-8'
    content = raw_content.decode(encoding)

    if config['output']['remove_comments']:
        # Implement comment removal logic here
        pass

    if config['output']['remove_empty_lines']:
        content = remove_empty_lines(content)

    return content.strip()

def remove_empty_lines(content: str) -> str:
    """Remove empty lines from the content."""
    return '\n'.join(line for line in content.splitlines() if line.strip())
