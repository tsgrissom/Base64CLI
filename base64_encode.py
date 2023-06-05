from binascii import Error
from sys import argv

from pybase64 import b64encode_as_string
from pyperclip import copy

from _constants import *
from _functions import create_action_string, dprint, log_and_exit, on_keyboard_interrupt
from _functions import return_to_main, run_py, sanitize_output


def display_and_copy(inp, out, nocopy=False):
    """
    Provides the user-facing results of running the encoding command.
    :param inp: The string input by the user.
    :param out: The output to be transformed after any per-process modifications preceding this method.
    :param nocopy: Whether a copyable output should be copied to system clipboard.
    :return: None. Method is print-only because it is for this file's scope.
    """
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

# Handles graceful exit from Ctrl+C
try:
    while not terminate:
        if unencoded == '':
            unencoded = input(f'> Enter the input you would like to encode ({STR_QUIT_ACTION}): ').strip()
        else:
            dprint(f'Encoding input "{unencoded}" supplied as command-line argument')

        if unencoded.lower() in CODES_EXIT:
            run_py('main.py')
            break

        try:
            no_copy = False

            # TODO Replace with argparse
            if unencoded.endswith(' --nocopy' or unencoded.endswith(' -nc')):
                no_copy = True
                unencoded = unencoded.removesuffix(' --nocopy')
                unencoded = unencoded.removesuffix(' -nc')

            string_as_bytes = bytes(unencoded, 'utf-8')
            encoded = b64encode_as_string(string_as_bytes)

            display_and_copy(unencoded, encoded, no_copy)

            action_string = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
            another = input(f'> Do you have another string to encode? {action_string} ').lower().strip()

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
    on_keyboard_interrupt(__file__)

log_and_exit(__file__)
