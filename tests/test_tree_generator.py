from repopack.utils.tree_generator import generate_tree_string


def test_generate_tree_string():
    files = ["src/main.py", "src/utils/helper.py", "tests/test_main.py", "README.md"]
    expected = (
        "README.md\n"
        "src/\n"
        "  main.py\n"
        "  utils/\n"
        "    helper.py\n"
        "tests/\n"
        "  test_main.py"
    )
    result = generate_tree_string(files)
    assert result == expected
