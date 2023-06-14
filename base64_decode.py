import binascii

import argparse
from pybase64 import b64decode
from pyperclip import copy

from _constants import CODES_EXIT, CODES_RETURN, DANGER, RESET, STR_QUIT_ACTION, SUCCESS, WARNING
from _functions import create_action_string, dprint, is_base64, is_debugging, log_and_exit, match_and_get_urls
from _functions import match_and_replace_urls, on_keyboard_interrupt, return_to_main, run_py, sanitize_output

ARG_HELP = {
    'hash': 'base64 hash to decode',
    'nocopy': 'disable copying the decoded hash to the system clipboard'
}


# Decoded contents might contain links, if they do they should be colored blue
def display_and_copy(output, nocopy):
    display = output

    if is_debugging():
        matches = match_and_get_urls(display)
        if matches is not None:
            dprint(f'URLs discovered in decoded hash: {matches}')

    # Colors URLs discovered by regex to blue
    display = match_and_replace_urls(display)

    # sanitize_output() returns two values
    # 1. The sanitized string
    # 2. Whether said string is copyable (does it contain linebreaks?)
    sanitized = sanitize_output(display)
    display = sanitized[0]
    copyable = sanitized[1]

    print(f'{SUCCESS}Decoded hash: {RESET}{display}')

    if copyable and not nocopy:
        copy(output)
        print(f'{WARNING}Copied decoded to system clipboard{RESET}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hash', '--input', '-i', help=ARG_HELP['hash'], metavar='BASE64 HASH', type=str)
    parser.add_argument('--nocopy', '-nc', action='store_true', default=False, help=ARG_HELP['nocopy'])
    args = parser.parse_args()

    b64 = args.hash
    no_copy = args.nocopy

    while True:
        try:
            if b64 is None:
                user_input = input(f'> Enter your base64 hash ({STR_QUIT_ACTION}): ').strip()

                if user_input.lower() in CODES_EXIT:
                    break
                elif user_input.lower() in CODES_RETURN:
                    return_to_main(should_newline=False)
                    break

                b64 = user_input

            try:
                decoded = b64decode(b64, validate=True)
                decoded_str = decoded.decode('utf-8').strip()
                display_and_copy(decoded_str, no_copy)

                action_str = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
                another = input(f'> Do you have another hash to decode? {action_str} ')
                another_compare = another.lower().strip()

                if is_base64(another):
                    b64 = another
                    continue

                if another_compare in ['y', 'yes']:
                    b64 = None
                    continue
                elif another_compare in CODES_RETURN:
                    return_to_main(should_newline=False)
                    break
                else:
                    break

            except binascii.Error:
                b64 = b64 if len(b64) <= 64 else f'{b64[:64]}...'
                print(f'{DANGER}Invalid base64 hash "{b64}"{RESET}')
                b64 = None

            except UnicodeDecodeError:
                print(f'{DANGER}Failed to decode hash "{b64}" with UTF-8!{RESET}')
                b64 = None

        except KeyboardInterrupt:
            on_keyboard_interrupt(__file__)


if __name__ == '__main__':
    main()

log_and_exit(__file__)
