import argparse
import os
from .packager import pack
from .config import load_config, merge_configs
from .utils.cli_output import print_summary, print_completion
from .utils.logger import logger
from .utils.spinner import Spinner
from .version import __version__


def run_cli():
    parser = argparse.ArgumentParser(description="Repopack - Pack your repository into a single AI-friendly file")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to pack")
    parser.add_argument("-o", "--output", help="Specify the output file name")
    parser.add_argument("-i", "--ignore", help="Additional ignore patterns (comma-separated)")
    parser.add_argument("-c", "--config", help="Path to a custom config file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-v", "--version", action="version", version=f"Repopack v{__version__}")
    parser.add_argument("--top-files-len", type=int, help="Specify the number of top files to display")
    args = parser.parse_args()

    logger.set_verbose(args.verbose)

    config = load_config(args.config)
    cli_config = {}
    if args.output:
        cli_config["output"] = {"file_path": args.output}
    if args.ignore:
        cli_config["ignore"] = {"custom_patterns": args.ignore.split(",")}
    if args.top_files_len is not None:
        cli_config["output"] = cli_config.get("output", {})
        cli_config["output"]["top_files_length"] = args.top_files_len
    
    merged_config = merge_configs(config, cli_config)

    spinner = Spinner("Packing files...")
    try:
        spinner.start()
        pack_result = pack(os.path.abspath(args.directory), merged_config)
        spinner.succeed("Packing completed successfully!")

        print_summary(pack_result['total_files'], pack_result['total_characters'], merged_config['output']['file_path'], 
                      pack_result['file_char_counts'], merged_config['output']['top_files_length'])
        print_completion()
    except Exception as e:
        spinner.fail(f"Error during packing: {str(e)}")
        logger.error(str(e))
        exit(1)

if __name__ == "__main__":
    run_cli()
