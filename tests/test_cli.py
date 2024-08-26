import pytest
from unittest.mock import patch, MagicMock
from repopack.cli import run_cli
from repopack.exceptions import RepopackError, ConfigurationError


def test_run_cli_success():
    with patch("repopack.cli.argparse.ArgumentParser.parse_args") as mock_parse_args, patch(
        "repopack.cli.load_config"
    ) as mock_load_config, patch("repopack.cli.merge_configs") as mock_merge_configs, patch(
        "repopack.cli.pack"
    ) as mock_pack, patch(
        "repopack.cli.print_summary"
    ) as mock_print_summary, patch(
        "repopack.cli.print_completion"
    ) as mock_print_completion:

        mock_parse_args.return_value = MagicMock(directory=".", verbose=False)
        mock_load_config.return_value = {}
        mock_merge_configs.return_value = {
            "output": {"file_path": "output.txt", "top_files_length": 5}
        }
        mock_pack.return_value = {
            "total_files": 10,
            "total_characters": 1000,
            "file_char_counts": {},
        }

        run_cli()

        mock_pack.assert_called_once()
        mock_print_summary.assert_called_once()
        mock_print_completion.assert_called_once()


def test_run_cli_repopack_error():
    with patch("repopack.cli.argparse.ArgumentParser.parse_args") as mock_parse_args, patch(
        "repopack.cli.load_config"
    ) as mock_load_config, patch("repopack.cli.merge_configs") as mock_merge_configs, patch(
        "repopack.cli.pack"
    ) as mock_pack, patch(
        "repopack.cli.logger.error"
    ) as mock_logger_error, patch(
        "repopack.cli.Spinner"
    ) as mock_spinner:

        mock_parse_args.return_value = MagicMock(directory=".", verbose=False)
        mock_load_config.return_value = {}
        mock_merge_configs.return_value = {
            "output": {"file_path": "output.txt", "top_files_length": 5}
        }
        mock_pack.side_effect = RepopackError("Test error")
        mock_spinner_instance = MagicMock()
        mock_spinner.return_value = mock_spinner_instance

        with pytest.raises(SystemExit):
            run_cli()

        mock_spinner_instance.fail.assert_called_with("Error during packing: Test error")
        mock_logger_error.assert_called_with("Test error")
