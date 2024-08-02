from typing import Dict
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_top_files(file_char_counts: Dict[str, int], top_files_length: int):
    print(f"\n{Fore.CYAN}📈 Top {top_files_length} Files by Character Count:")
    print(f"{Fore.CYAN}──────────────────────────────────")
    
    sorted_files = sorted(file_char_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (file_path, char_count) in enumerate(sorted_files[:top_files_length], 1):
        print(f"{Fore.WHITE}{i}. {file_path} {Style.DIM}({char_count} chars)")

def print_summary(total_files, total_characters, output_path, file_char_counts, top_files_length):
    print(f"\n{Fore.CYAN}📊 Pack Summary:")
    print(f"{Fore.CYAN}────────────────")
    print(f"{Fore.WHITE}Total Files: {total_files}")
    print(f"{Fore.WHITE}Total Chars: {total_characters}")
    print(f"{Fore.WHITE}     Output: {output_path}")

    if top_files_length > 0:
        print_top_files(file_char_counts, top_files_length)

def print_completion():
    print(f"\n{Fore.GREEN}🎉 All Done!")
    print(f"{Fore.WHITE}Your repository has been successfully packed.")
    