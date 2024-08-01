import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_summary(total_files, total_characters, output_path):
    print(f"\n{Fore.CYAN}📊 Pack Summary:")
    print(f"{Fore.CYAN}────────────────")
    print(f"{Fore.WHITE}Total Files: {total_files}")
    print(f"{Fore.WHITE}Total Chars: {total_characters}")
    print(f"{Fore.WHITE}     Output: {output_path}")

def print_completion():
    print(f"\n{Fore.GREEN}🎉 All Done!")
    print(f"{Fore.WHITE}Your repository has been successfully packed.")
    