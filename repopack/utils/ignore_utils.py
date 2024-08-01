import os
from typing import List, Dict, Any
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

DEFAULT_IGNORE_LIST = [
    '.git', '.gitignore', 'node_modules', '*.pyc', '__pycache__',
    '.vscode', '.idea', '*.log', '*.swp', '*.swo'
]

def get_ignore_patterns(filename: str, root_dir: str) -> List[str]:
    """Get ignore patterns from a file."""
    ignore_path = os.path.join(root_dir, filename)
    if os.path.exists(ignore_path):
        with open(ignore_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def get_all_ignore_patterns(root_dir: str, config: Dict[str, Any]) -> List[str]:
    """Get all ignore patterns based on the configuration."""
    patterns = []
    if config['ignore']['use_default_patterns']:
        patterns.extend(DEFAULT_IGNORE_LIST)
    if config['ignore']['use_gitignore']:
        patterns.extend(get_ignore_patterns('.gitignore', root_dir))
    patterns.extend(get_ignore_patterns('.repopackignore', root_dir))
    patterns.extend(config['ignore']['custom_patterns'])
    return patterns

def create_ignore_filter(patterns: List[str]):
    """Create an ignore filter function based on the given patterns."""
    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    return lambda path: not spec.match_file(path)
