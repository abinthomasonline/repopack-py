import os
from typing import Dict, Any
from .exceptions import RepopackError, FileProcessingError, OutputGenerationError
from .utils.file_handler import sanitize_files
from .utils.ignore_utils import get_all_ignore_patterns, create_ignore_filter
from .utils.logger import logger
from .output_generator import generate_output


def pack(root_dir: str, config: Dict[str, Any]) -> Dict[str, Any]:
    logger.debug(f"Starting packing process for directory: {root_dir}")
    logger.debug(f"Configuration: {config}")

    try:
        ignore_patterns = get_all_ignore_patterns(root_dir, config)
        logger.debug(f"Ignore patterns: {ignore_patterns}")

        ignore_filter = create_ignore_filter(ignore_patterns)

        all_file_paths = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), root_dir)
                if ignore_filter(file_path):
                    all_file_paths.append(file_path)
                    logger.trace(f"Including file: {file_path}")
                else:
                    logger.trace(f"Ignoring file: {file_path}")

        logger.info(f"Total files to process: {len(all_file_paths)}")

        sanitized_files = sanitize_files(all_file_paths, root_dir, config)
        logger.debug(f"Sanitized {len(sanitized_files)} files")

        file_char_counts = {file["path"]: len(file["content"]) for file in sanitized_files}

        logger.debug("Generating output")
        generate_output(root_dir, config, sanitized_files, all_file_paths, file_char_counts)

        total_files = len(sanitized_files)
        total_characters = sum(len(file["content"]) for file in sanitized_files)

        logger.info(
            f"Packing complete. Total files: {total_files}, Total characters: {total_characters}"
        )

        return {
            "total_files": total_files,
            "total_characters": total_characters,
            "file_char_counts": file_char_counts,
        }
    except FileProcessingError as e:
        logger.error(f"Error processing files: {str(e)}")
        raise RepopackError(f"File processing error: {str(e)}") from e

    except OutputGenerationError as e:
        logger.error(f"Error generating output: {str(e)}")
        raise RepopackError(f"Output generation error: {str(e)}") from e

    except OSError as e:
        logger.error(f"OS error: {str(e)}")
        raise RepopackError(f"OS error: {str(e)}") from e

    except Exception as e:
        logger.error(f"Unexpected error during packing: {str(e)}")
        raise RepopackError(f"Unexpected error: {str(e)}") from e
