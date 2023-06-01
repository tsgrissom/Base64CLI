from _constants import ACTION, DANGER, EXIT_CODES, SUCCESS, RESET, RETURN_CODES, QUIT_ACTION_STR
from _functions import create_action_string, log_and_exit, match_and_get_urls, match_and_replace_urls, return_to_main, sanitize_output
from binascii import Error
from colorama import Fore
from pybase64 import b64decode
from pyperclip import copy
from sys import argv


def display_and_copy(output, nocopy):
    display = output

    # Decoded contents might contain links, if they do they should be colored blue
    # TODO Replace with regex find and replace
    # TODO Change style of output
    urls = match_and_get_urls(display)
    display = match_and_replace_urls(display)

    sanitized = sanitize_output(display)
    display = sanitized[0]
    should_copy = sanitized[1]

    print(f'{SUCCESS}Decoded hash: {RESET}{Fore.BLUE}{display}')

    if should_copy and not nocopy:
        copy(output)
        print(f'{ACTION}Copied decoded to system clipboard{RESET}')


b64 = str()
decoded = str()
terminate = False

if len(argv) > 1:
    b64 = argv[1]

try:
    while not terminate:
        if b64 == '':
            b64 = input(f'> Enter your base64 hash ({QUIT_ACTION_STR}): ').strip()
        else:
            print(f'Decoding hash "{b64}" supplied as command-line argument')

        if b64.lower() in EXIT_CODES:
            log_and_exit(__file__)
            break

        try:
            no_copy = False

            if b64.endswith(' --nocopy' or b64.endswith(' -nc')):
                no_copy = True
                b64 = b64.removesuffix(' --nocopy')
                b64 = b64.removesuffix(' -nc')

            decoded = b64decode(b64, validate=True)
            decoded_str = decoded.decode('utf-8').strip()

            # Returns bytes, needs to be decoded when displayed
            display_and_copy(decoded_str, no_copy)

            action_str = create_action_string('y', 'n', 'return', QUIT_ACTION_STR)
            another = input(f'> Do you have another hash to decode? {action_str} ').lower()

            if another in RETURN_CODES:
                return_to_main()
                break
            elif another == 'y' or another == 'yes':
                continue

            terminate = True
            # User has inputted all hashes they wished to decode for the session
        except Error:
            if len(b64) > 64:
                b64 = f'{b64[:64]}...'
                # Truncate length of invalid base64 hash for clean console

            print(f'{DANGER}Invalid base64 hash "{b64}"{RESET}')
            b64 = str()
            # Program repeats because terminate != False
        except UnicodeDecodeError:
            print(f'{DANGER}Failed to decode hash "{b64}" with UTF-8!{RESET}')
            b64 = str()
except KeyboardInterrupt:
    log_and_exit(__file__)
