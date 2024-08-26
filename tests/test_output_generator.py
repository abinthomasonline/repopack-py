import pytest
from repopack.output_generator import generate_output, generate_plain_output, generate_xml_output
from repopack.exceptions import OutputGenerationError


@pytest.fixture
def sample_data():
    return {
        "generationDate": "2023-04-01T12:00:00",
        "treeString": "root/\n  file1.txt\n  file2.py",
        "sanitizedFiles": [
            {"path": "file1.txt", "content": "Content of file1"},
            {"path": "file2.py", "content": "Content of file2"},
        ],
        "config": {
            "output": {
                "style": "plain",
                "remove_comments": False,
                "show_line_numbers": False,
                "header_text": "Custom header",
            }
        },
    }


def test_generate_plain_output(sample_data):
    output = generate_plain_output(sample_data)
    assert "RepopackPy Output File" in output
    assert "file1.txt" in output
    assert "file2.py" in output
    assert "Content of file1" in output
    assert "Content of file2" in output
    assert "Custom header" in output


def test_generate_xml_output(sample_data):
    sample_data["config"]["output"]["style"] = "xml"
    output = generate_xml_output(sample_data)
    assert "<summary>" in output
    assert '<file path="file1.txt">' in output
    assert '<file path="file2.py">' in output
    assert "Content of file1" in output
    assert "Content of file2" in output
    assert "<user_provided_header>" in output


def test_generate_output_plain(sample_data, tmp_path):
    output_path = tmp_path / "output.txt"
    generate_output(
        "root",
        sample_data["config"],
        sample_data["sanitizedFiles"],
        ["file1.txt", "file2.py"],
        str(output_path),
    )
    assert output_path.exists()
    content = output_path.read_text()
    assert "RepopackPy Output File" in content


def test_generate_output_xml(sample_data, tmp_path):
    sample_data["config"]["output"]["style"] = "xml"
    output_path = tmp_path / "output.xml"
    generate_output(
        "root",
        sample_data["config"],
        sample_data["sanitizedFiles"],
        ["file1.txt", "file2.py"],
        str(output_path),
    )
    assert output_path.exists()
    content = output_path.read_text()
    assert "<summary>" in content


def test_generate_output_error():
    with pytest.raises(OutputGenerationError):
        generate_output("root", {}, [], [], "/nonexistent/path/output.txt")
