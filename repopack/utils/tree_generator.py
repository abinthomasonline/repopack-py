from typing import List, Dict, Optional


class TreeNode:
    """Represents a node in the file tree structure."""

    def __init__(self, name: str, is_directory: bool = False):
        """
        Initialize a TreeNode.

        Args:
            name (str): The name of the file or directory.
            is_directory (bool, optional): Whether this node represents a directory. Defaults to False.
        """
        self.name: str = name
        self.children: List["TreeNode"] = []
        self.is_directory: bool = is_directory


def generate_file_tree(files: List[str]) -> TreeNode:
    """
    Generate a file tree structure from a list of file paths.

    Args:
        files (List[str]): List of file paths.

    Returns:
        TreeNode: The root node of the generated file tree.
    """
    root = TreeNode("root", True)
    for file in files:
        parts = file.split("/")
        current_node = root
        for i, part in enumerate(parts):
            is_last_part = i == len(parts) - 1
            child = next((c for c in current_node.children if c.name == part), None)
            if not child:
                child = TreeNode(part, not is_last_part)
                current_node.children.append(child)
            current_node = child
    return root


def sort_tree_nodes(node: TreeNode) -> None:
    """
    Sort the children of a TreeNode recursively.

    Directories are sorted before files, and then alphabetically.

    Args:
        node (TreeNode): The node whose children should be sorted.
    """
    node.children.sort(key=lambda x: (not x.is_directory, x.name))
    for child in node.children:
        sort_tree_nodes(child)


def tree_to_string(node: TreeNode, prefix: str = "") -> str:
    """
    Convert a TreeNode structure to a string representation.

    Args:
        node (TreeNode): The root node of the tree to convert.
        prefix (str, optional): The prefix to use for indentation. Defaults to "".

    Returns:
        str: A string representation of the file tree.
    """
    sort_tree_nodes(node)
    result = ""
    for child in node.children:
        result += f"{prefix}{child.name}{'/' if child.is_directory else ''}\n"
        if child.is_directory:
            result += tree_to_string(child, prefix + "  ")
    return result


def generate_tree_string(files: List[str]) -> str:
    """
    Generate a string representation of the file tree from a list of file paths.

    Args:
        files (List[str]): List of file paths.

    Returns:
        str: A string representation of the file tree.
    """
    tree = generate_file_tree(files)
    return tree_to_string(tree).strip()
