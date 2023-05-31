from _constants import ACTION, ADVICE, DANGER, EXIT_CODES, RESET, SUCCESS
from _functions import log_and_exit, return_to_main, sanitize_output
from binascii import Error
from colorama import Fore
from pybase64 import b64encode_as_string
from pyperclip import copy
from sys import argv


def display_and_copy(output, nocopy=False):
    sanitized = sanitize_output(output)
    output = sanitized[0]
    copyable = sanitized[1]

    print(f'{SUCCESS}Encoded your input: {RESET}{output}')

    if copyable and not nocopy:
        copy(output)
        print(f'{ACTION}Copied encoded string to system clipboard{RESET}')


unencoded = str()
terminate = False

if len(argv) > 1:
    unencoded = argv[1]

while not terminate:
    if unencoded == '':
        unencoded = input(f'Enter the input you would like to encode ({ADVICE}"Q"{RESET} to quit): ').strip()
    else:
        print(f'Encoding input "{unencoded}" supplied as command-line argument')

    if unencoded.lower() in EXIT_CODES:
        log_and_exit(__file__)
        break

    try:
        string_as_bytes = bytes(unencoded, 'utf-8')
        encoded = b64encode_as_string(string_as_bytes)
        no_copy = False

        for a in argv:
            if a.lower() == "--nocopy" or a.lower() == "-nc":
                no_copy = True

        display_and_copy(encoded, no_copy)

        another = input('Do you have another string to encode? (y/n/return) ').lower()

        if another == 'return' or another == 'menu' or another == 'back':
            return_to_main()
            break
        elif another == 'y' or another == 'yes':
            continue

        terminate = True
    except Error:
        if len(unencoded) > 64:
            unencoded = f'{unencoded[:64]}...'

        print(f'{DANGER}Unable to encode string "{unencoded}" to base64 hash!{RESET}')
        unencoded = str()
    except UnicodeDecodeError:
        print(f'{DANGER}Failed to encode hash "{unencoded}" with UTF-8!{RESET}')
        unencoded = str()

log_and_exit(__file__)
