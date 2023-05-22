import binascii
from colorama import Fore, Style
import pybase64
import pyperclip
import sys

EXIT_CODES = ['q', 'quit', 'exit', 'end']
ACTION = Fore.CYAN
DANGER = Fore.RED
ADVICE = Fore.LIGHTRED_EX
SUCCESS = Fore.GREEN
RESET = Style.RESET_ALL

b64 = str()
decoded = str()
terminate = False


def display_and_copy(output, copy=True):
    display = output

    if output.__contains__("https://") or output.__contains__("http://"):
        display = Fore.BLUE.join(output)

    if "\n" in output:
        output = output.replace('\n\n', '\n')
        display = f'\n{output}{RESET}\n'
        copy = False

    print(f'{SUCCESS}Decoded hash: {RESET}{Fore.BLUE}{display}')

    if copy:
        pyperclip.copy(output)
        print(f'{ACTION}Copied to system clipboard{RESET}')


def log_and_exit():
    print(f'{DANGER}Exiting base64_decode.py{RESET}')
    exit(0)


if len(sys.argv) > 1:
    b64 = sys.argv[1]

while not terminate:
    if b64 == '':
        b64 = input(f'Enter your base64 hash ({ADVICE}"Q"{RESET} to quit): ').strip()
    else:
        print(f'Decoding hash "{b64}" supplied as command-line argument')

    if b64.lower() in EXIT_CODES:
        log_and_exit()
        break

    try:
        decoded = pybase64.b64decode(b64, validate=True)
        # Returns bytes, needs to be decoded when displayed
        display_and_copy(decoded.decode('utf-8').strip())

        another = input('Do you have another hash to decode? (y/n) ').lower()

        if another == 'y' or another == 'yes':
            continue

        terminate = True
        # User has inputted all hashes they wished to decode for the session
    except binascii.Error:
        if len(b64) > 64:
            b64 = f'{b64[:64]}...'
            # Truncate length of invalid base64 hash for clean console

        print(f'{DANGER}Invalid base64 hash "{b64}"{RESET}')
        b64 = str()
        # Program repeats because terminate != False
    except UnicodeDecodeError:
        print(f'{DANGER}Failed to decode hash "{b64}" with UTF-8!{RESET}')
        b64 = str()

log_and_exit()
