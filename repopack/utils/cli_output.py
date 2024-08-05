from typing import Dict, List, Tuple
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)


def print_top_files(file_char_counts: Dict[str, int], top_files_length: int) -> None:
    """
    Print the top files by character count.

    Args:
        file_char_counts (Dict[str, int]): A dictionary of file paths and their character counts.
        top_files_length (int): The number of top files to display.
    """
    print(f"\n{Fore.CYAN}📈 Top {top_files_length} Files by Character Count:")
    print(f"{Fore.CYAN}──────────────────────────────────")

    sorted_files: List[Tuple[str, int]] = sorted(
        file_char_counts.items(), key=lambda x: x[1], reverse=True
    )
    for i, (file_path, char_count) in enumerate(sorted_files[:top_files_length], 1):
        print(f"{Fore.WHITE}{i}. {file_path} {Style.DIM}({char_count} chars)")


def print_summary(
    total_files: int,
    total_characters: int,
    output_path: str,
    file_char_counts: Dict[str, int],
    top_files_length: int,
) -> None:
    """
    Print a summary of the repository packing process.

    Args:
        total_files (int): The total number of files processed.
        total_characters (int): The total number of characters in all files.
        output_path (str): The path where the output file is saved.
        file_char_counts (Dict[str, int]): A dictionary of file paths and their character counts.
        top_files_length (int): The number of top files to display.
    """
    print(f"\n{Fore.CYAN}📊 Pack Summary:")
    print(f"{Fore.CYAN}────────────────")
    print(f"{Fore.WHITE}Total Files: {total_files}")
    print(f"{Fore.WHITE}Total Chars: {total_characters}")
    print(f"{Fore.WHITE}     Output: {output_path}")

    if top_files_length > 0:
        print_top_files(file_char_counts, top_files_length)


def print_completion() -> None:
    """
    Print a completion message indicating that the repository has been successfully packed.
    """
    print(f"\n{Fore.GREEN}🎉 All Done!")
    print(f"{Fore.WHITE}Your repository has been successfully packed.")
