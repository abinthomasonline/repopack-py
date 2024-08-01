import os
from typing import Dict, Any
from .utils.file_handler import sanitize_files
from .utils.ignore_utils import get_all_ignore_patterns, create_ignore_filter
from .output_generator import generate_output

def pack(root_dir: str, config: Dict[str, Any]) -> Dict[str, Any]:
    ignore_patterns = get_all_ignore_patterns(root_dir, config)
    ignore_filter = create_ignore_filter(ignore_patterns)

    all_file_paths = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), root_dir)
            if ignore_filter(file_path):
                all_file_paths.append(file_path)

    sanitized_files = sanitize_files(all_file_paths, root_dir, config)

    generate_output(root_dir, config, sanitized_files, all_file_paths)

    total_files = len(sanitized_files)
    total_characters = sum(len(file['content']) for file in sanitized_files)

    return {
        "total_files": total_files,
        "total_characters": total_characters,
    }
