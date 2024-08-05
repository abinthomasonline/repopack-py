from typing import List, Dict


class TreeNode:
    def __init__(self, name: str, is_directory: bool = False):
        self.name = name
        self.children = []
        self.is_directory = is_directory


def generate_file_tree(files: List[str]) -> TreeNode:
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


def sort_tree_nodes(node: TreeNode):
    node.children.sort(key=lambda x: (not x.is_directory, x.name))
    for child in node.children:
        sort_tree_nodes(child)


def tree_to_string(node: TreeNode, prefix: str = "") -> str:
    sort_tree_nodes(node)
    result = ""
    for child in node.children:
        result += f"{prefix}{child.name}{'/' if child.is_directory else ''}\n"
        if child.is_directory:
            result += tree_to_string(child, prefix + "  ")
    return result


def generate_tree_string(files: List[str]) -> str:
    tree = generate_file_tree(files)
    return tree_to_string(tree).strip()
