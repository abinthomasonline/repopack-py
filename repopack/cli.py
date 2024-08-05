import argparse
import logging
import os
import sys
from typing import Dict, Any
from .packager import pack
from .config import load_config, merge_configs
from .exceptions import RepopackError, ConfigurationError
from .utils.cli_output import print_summary, print_completion
from .utils.logger import logger
from .utils.spinner import Spinner
from .version import __version__


def run_cli() -> None:
    """
    Main entry point for the Repopack CLI.
    Parses command-line arguments, loads and merges configurations, and executes the packing process.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Repopack - Pack your repository into a single AI-friendly file"
    )
    parser.add_argument("directory", nargs="?", default=".", help="Directory to pack")
    parser.add_argument("-o", "--output", help="Specify the output file name")
    parser.add_argument("-i", "--ignore", help="Additional ignore patterns (comma-separated)")
    parser.add_argument("-c", "--config", help="Path to a custom config file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-v", "--version", action="version", version=f"Repopack v{__version__}")
    parser.add_argument(
        "--top-files-len", type=int, help="Specify the number of top files to display"
    )
    parser.add_argument(
        "--output-show-line-numbers",
        action="store_true",
        help="Add line numbers to each line in the output",
    )
    parser.add_argument(
        "--output-style",
        choices=["plain", "xml"],
        default="plain",
        help="Specify the output style (plain or xml)",
    )
    args = parser.parse_args()

    # Set verbosity level
    logger.set_verbose(args.verbose)

    # Load configuration
    try:
        config: Dict[str, Any] = load_config(args.config)
    except ConfigurationError as e:
        logger.error(f"Configuration file error: {str(e)}")
        logger.debug("Stack trace:", exc_info=True)
        sys.exit(1)
    except IOError as e:
        logger.error(f"Error reading configuration file: {str(e)}")
        logger.debug("Stack trace:", exc_info=True)
        sys.exit(1)

    # Create CLI configuration
    cli_config: Dict[str, Any] = {}
    if args.output:
        cli_config["output"] = {"file_path": args.output}
    if args.ignore:
        cli_config["ignore"] = {"custom_patterns": args.ignore.split(",")}
    if args.top_files_len is not None:
        cli_config["output"] = cli_config.get("output", {})
        cli_config["output"]["top_files_length"] = args.top_files_len
    if args.output_show_line_numbers:
        cli_config["output"] = cli_config.get("output", {})
        cli_config["output"]["show_line_numbers"] = True
    if args.output_style:
        cli_config["output"] = cli_config.get("output", {})
        cli_config["output"]["style"] = args.output_style

    # Merge configurations
    try:
        merged_config: Dict[str, Any] = merge_configs(config, cli_config)
    except ConfigurationError as e:
        logger.error(f"Error merging configurations: {str(e)}")
        logger.debug("Stack trace:", exc_info=True)
        sys.exit(1)

    logger.debug(f"Merged configuration: {merged_config}")

    # Initialize spinner for visual feedback
    spinner = Spinner("Packing files...")
    try:
        spinner.start()
        # Execute packing process
        pack_result: Dict[str, Any] = pack(os.path.abspath(args.directory), merged_config)
        spinner.succeed("Packing completed successfully!")

        # Print summary and completion message
        print_summary(
            pack_result["total_files"],
            pack_result["total_characters"],
            merged_config["output"]["file_path"],
            pack_result["file_char_counts"],
            merged_config["output"]["top_files_length"],
        )
        print_completion()
    except RepopackError as e:
        spinner.fail(f"Error during packing: {str(e)}")
        logger.error(str(e))
        if logger.logger.level <= logging.DEBUG:
            logger.error("Traceback:", exc_info=True)
        sys.exit(1)
    except Exception as e:
        spinner.fail(f"Unexpected error: {str(e)}")
        logger.error(f"An unexpected error occurred: {str(e)}")
        if logger.logger.level <= logging.DEBUG:
            logger.error("Traceback:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
