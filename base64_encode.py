from _constants import *
from _functions import log_and_exit, return_to_main, sanitize_output, create_action_string
from binascii import Error
from pybase64 import b64encode_as_string
from pyperclip import copy
from sys import argv
from time import sleep


def display_and_copy(inp, out, nocopy=False):
    sanitized = sanitize_output(out)
    out = sanitized[0]
    copyable = sanitized[1]

    print(f'{RESET} \u2022 {WARNING}Your input: {RESET}"{inp}"')
    print(f'{RESET} \u2937 {SUCCESS}Encoded: {RESET}{out}')

    if copyable and not nocopy:
        copy(out)
        print(f'{RESET} \u2937 {WARNING}Copied encoded string to system clipboard{RESET}')


unencoded = str()
terminate = False

if len(argv) > 1:
    unencoded = argv[1]

try:
    while not terminate:
        if unencoded == '':
            unencoded = input(f'> Enter the input you would like to encode ({QUIT_ACTION_STR}): ').strip()
        else:
            print(f'Encoding input "{unencoded}" supplied as command-line argument')

        if unencoded.lower() in CODES_EXIT:
            log_and_exit(__file__)
            break

        try:
            no_copy = False

            if unencoded.endswith(' --nocopy' or unencoded.endswith(' -nc')):
                no_copy = True
                unencoded = unencoded.removesuffix(' --nocopy')
                unencoded = unencoded.removesuffix(' -nc')

            string_as_bytes = bytes(unencoded, 'utf-8')
            encoded = b64encode_as_string(string_as_bytes)

            sleep(0.75)

            display_and_copy(unencoded, encoded, no_copy)

            action_string = create_action_string('y', 'n', 'return', QUIT_ACTION_STR)
            another = input(f'> Do you have another string to encode? {action_string} ').lower()

            if another in CODES_RETURN:
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
except KeyboardInterrupt:
    log_and_exit(__file__)