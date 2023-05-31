from colorama import Fore, Style

EXIT_CODES = ['q', 'quit', 'exit', 'end']
ACTION = Fore.CYAN
DANGER = Fore.RED
ADVICE = Fore.LIGHTRED_EX
SUCCESS = Fore.GREEN
RESET = Style.RESET_ALL
QUIT_ACTION_STR = f'{ADVICE}Q{RESET} to quit'
