import argparse
from argparse import Namespace
import binascii

from pybase64 import b64decode
from pyperclip import copy

from _constants import CODES_EXIT, CODES_RETURN, DANGER, RESET, STR_QUIT_ACTION, SUCCESS, WARNING
from _functions import create_action_string, dprint, is_base64, is_debugging, log_and_exit, match_and_get_urls
from _functions import match_and_replace_urls, on_keyboard_interrupt, return_to_main, sanitize_output

ARG_HELP = {
    'hash': 'base64 hash to decode',
    'nocopy': 'disable copying the decoded hash to the system clipboard'
}


class DecodeProcess:

    hash = None
    no_copy = False
    terminate = False

    def parse_args(self) -> Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('--hash', '--input', '-i', help=ARG_HELP['hash'], metavar='BASE64 HASH', type=str)
        parser.add_argument('--nocopy', '-nc', action='store_true', default=False, help=ARG_HELP['nocopy'])
        return parser.parse_args()

    def request_hash(self):
        inp = input(f'> Enter your base64 hash ({STR_QUIT_ACTION}): ').strip()

        if inp.lower() in CODES_EXIT:
            self.terminate = True
            return
        elif inp.lower() in CODES_EXIT:
            self.terminate = True
            return_to_main(should_newline=False)
            return

        self.hash = inp

    def display_and_copy(self, decoded, nocopy, encoding='utf-8'):
        if not isinstance(decoded, bytes):
            raise TypeError('Cannot display non-byte decoded value')

        decoded_str = decoded.decode(encoding).strip()
        display = decoded_str

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
            copy(decoded_str)
            print(f'{WARNING}Copied decoded value to system clipboard{RESET}')

    def decode_hash(self):
        if self.hash is None:
            raise TypeError('Cannot decode a hash of None')

        try:
            decoded = b64decode(self.hash, validate=True)
            self.display_and_copy(decoded, self.no_copy)
        except binascii.Error:
            # TODO Truncate method here and below?
            b64 = self.hash if len(self.hash) <= 64 else f'{self.hash[:64]}...'
            print(f'{DANGER}Invalid base64 hash "{b64}"{RESET}')
            self.hash = None
        except UnicodeDecodeError:
            print(f'{DANGER}Failed to decode hash "{self.hash}" with UTF-8!{RESET}')
            self.hash = None

    def decode_hash_repeat(self):
        self.decode_hash()

        action_str = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
        another = input(f'> Do you have another hash to decode? {action_str} ')
        another_low = another.lower().strip()

        if is_base64(another):
            self.hash = another
        if another_low in ['y', 'yes']:
            self.hash = None
        elif another_low in CODES_RETURN:
            self.terminate = True
            return_to_main(should_newline=False)
        else:
            self.terminate = True

    def main(self):
        args = self.parse_args()
        self.no_copy = args.nocopy

        while not self.terminate:
            try:
                if self.hash is None:
                    self.request_hash()

                self.decode_hash_repeat()
            except KeyboardInterrupt:
                on_keyboard_interrupt(__file__)


if __name__ == '__main__':
    process = DecodeProcess()
    process.main()

log_and_exit(__file__)
