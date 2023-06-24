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


class EncodeProcess:

    args = None
    to_encode = None
    no_copy = False

    terminate = False

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--hash', '--input', '-i', help=ARG_HELP['input'], metavar='STRING', nargs='?', type=str)
        parser.add_argument('--nocopy', '-nc', action='store_true', default=False, help=ARG_HELP['nocopy'])
        return parser.parse_args()

    def __init__(self):
        self.args = self.parse_args()
        self.to_encode = self.args.hash
        self.no_copy = self.args.nocopy

    def request_input(self):
        inp = input(f'> Enter your string to encode with base64 ({STR_QUIT_ACTION}): ').strip()

        if inp.lower() in CODES_EXIT:
            self.terminate = True
        elif inp.lower() in CODES_RETURN:
            self.terminate = True
            return_to_main(should_newline=False)

        self.to_encode = inp

    def display_and_copy(self, inp, out, nocopy=False):
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

    def encode_input(self):
        try:
            string_as_bytes = bytes(self.to_encode, 'utf-8')
            encoded = b64encode_as_string(string_as_bytes)

            self.display_and_copy(self.to_encode, encoded, self.no_copy)
        except binascii.Error:
            unencoded = self.to_encode if len(self.to_encode) <= 64 else f'{self.to_encode[:32]}...'
            print(f'{DANGER}Unable to encode string "{unencoded}" to base64 hash!{RESET}')
            self.to_encode = None
        except UnicodeEncodeError:
            print(f'{DANGER}Failed to encode hash "{self.to_encode}" with UTF-8!{RESET}')
            self.to_encode = None

    def encode_input_repeat(self):
        self.encode_input()

        action_str = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
        another = input(f'> Do you have another string to encode? {action_str} ')
        another_san = another.lower().strip()

        if another_san in CODES_RETURN:
            self.terminate = True
            return_to_main()
        elif another_san in CODES_EXIT:
            self.terminate = True
        else:
            self.to_encode = another

    def main(self):
        while not self.terminate:
            try:
                if self.to_encode is None:
                    self.request_input()

                self.encode_input_repeat()
            except KeyboardInterrupt:
                on_keyboard_interrupt(__file__)


if __name__ == '__main__':
    process = EncodeProcess()
    process.main()

log_and_exit(__file__)