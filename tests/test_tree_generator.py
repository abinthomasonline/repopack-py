from typing import List
from repopack.utils.tree_generator import generate_tree_string


def test_generate_tree_string() -> None:
    """
    Test the generate_tree_string function to ensure it correctly generates
    a tree-like string representation of the given file structure.
    """
    # Input: List of file paths
    files: List[str] = ["src/main.py", "src/utils/helper.py", "tests/test_main.py", "README.md"]

    # Expected output: Tree-like string representation
    expected: str = (
        "src/\n"
        "  utils/\n"
        "    helper.py\n"
        "  main.py\n"
        "tests/\n"
        "  test_main.py\n"
        "README.md"
    )

    # Generate the tree string
    result: str = generate_tree_string(files)

    # Assert that the generated string matches the expected output
    assert result == expected, "The generated tree string does not match the expected output"
