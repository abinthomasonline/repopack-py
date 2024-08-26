import pytest
from unittest.mock import patch, MagicMock
from repopack.packager import pack
from repopack.exceptions import RepopackError, FileProcessingError, OutputGenerationError


@pytest.fixture
def mock_config():
    return {
        "ignore": {"use_default_patterns": True, "use_gitignore": True, "custom_patterns": []},
        "output": {"file_path": "output.txt", "top_files_length": 5},
    }


def test_pack_success(mock_config, tmp_path):
    root_dir = tmp_path / "test_repo"
    root_dir.mkdir()
    (root_dir / "file1.txt").write_text("Content 1")
    (root_dir / "file2.py").write_text("Content 2")

    with patch("repopack.packager.generate_output") as mock_generate_output, patch(
        "repopack.packager.sanitize_files"
    ) as mock_sanitize_files:

        mock_sanitize_files.return_value = [
            {"path": "file1.txt", "content": "Content 1"},
            {"path": "file2.py", "content": "Content 2"},
        ]

        result = pack(str(root_dir), mock_config, "output.txt")

    assert result["total_files"] == 2
    assert result["total_characters"] == 18
    assert len(result["file_char_counts"]) == 2
    mock_generate_output.assert_called_once()


def test_pack_file_processing_error(mock_config, tmp_path):
    root_dir = tmp_path / "test_repo"
    root_dir.mkdir()

    with patch("repopack.packager.sanitize_files") as mock_sanitize_files:
        mock_sanitize_files.side_effect = FileProcessingError("test.txt", "Test error")

        with pytest.raises(
            RepopackError,
            match="File processing error: Error processing file 'test.txt': Test error",
        ):
            pack(str(root_dir), mock_config, "output.txt")


def test_pack_output_generation_error(mock_config, tmp_path):
    root_dir = tmp_path / "test_repo"
    root_dir.mkdir()
    (root_dir / "file1.txt").write_text("Content")

    with patch("repopack.packager.generate_output") as mock_generate_output, patch(
        "repopack.packager.sanitize_files"
    ) as mock_sanitize_files:

        mock_sanitize_files.return_value = [{"path": "file1.txt", "content": "Content"}]
        mock_generate_output.side_effect = OutputGenerationError("Test error")

        with pytest.raises(RepopackError) as excinfo:
            pack(str(root_dir), mock_config, "output.txt")

        assert str(excinfo.value) == "Output generation error: Error generating output: Test error"


def test_pack_os_error(mock_config):
    with pytest.raises(RepopackError) as excinfo:
        pack("/nonexistent/path", mock_config, "output.txt")

    error_message = str(excinfo.value)

    assert any(
        phrase in error_message
        for phrase in [
            "OS error:",
            "No such file or directory",
            "Error processing files:",
            "Error generating output:",
        ]
    ), f"Unexpected error message: {error_message}"
