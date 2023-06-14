import argparse
import binascii

from pybase64 import b64encode_as_string
from pyperclip import copy

from _constants import CODES_EXIT, CODES_RETURN, DANGER, RESET, STR_QUIT_ACTION, SUCCESS, WARNING
from _functions import create_action_string, log_and_exit, on_keyboard_interrupt
from _functions import return_to_main, sanitize_output

ARG_HELP = {
    'input': 'string to encode to base64',
    'nocopy': 'disable copying the encoded string to the system clipboard'
}


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hash', '--input', '-i', help=ARG_HELP['input'], metavar='STRING', nargs='?', type=str)
    parser.add_argument('--nocopy', '-nc', action='store_true', default=False, help=ARG_HELP['nocopy'])
    args = parser.parse_args()

    unencoded = args.hash
    no_copy = args.nocopy

    while True:
        try:
            if unencoded is None:
                user_input = input(f'> Enter your string to encode with base64 ({STR_QUIT_ACTION}): ').strip()

                if user_input.lower() in CODES_EXIT:
                    break
                elif user_input.lower() in CODES_RETURN:
                    return_to_main(should_newline=False)
                    break

                unencoded = user_input

            try:
                string_as_bytes = bytes(unencoded, 'utf-8')
                encoded = b64encode_as_string(string_as_bytes)

                display_and_copy(unencoded, encoded, no_copy)

                action_str = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
                another = input(f'> Do you have another string to encode? {action_str} ').lower().strip()

                if another in ['y', 'yes']:
                    continue
                elif another in CODES_RETURN:
                    return_to_main()
                    break
                else:
                    break

            except binascii.Error:
                unencoded = unencoded if len(unencoded) <= 64 else f'{unencoded[:unencoded]}...'
                print(f'{DANGER}Unable to encode string "{unencoded}" to base64 hash!{RESET}')
                unencoded = ''

            except UnicodeEncodeError:
                print(f'{DANGER}Failed to encode hash "{unencoded}" with UTF-8!{RESET}')
                unencoded = ''

        except KeyboardInterrupt:
            on_keyboard_interrupt(__file__)


if __name__ == '__main__':
    main()

log_and_exit(__file__)
