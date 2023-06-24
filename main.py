import argparse
from argparse import Namespace

from _constants import DANGER, CODES_EXIT, CODES_HELP, STR_QUIT_ACTION, RESET, WARNING
from _functions import create_action_string, dprint, is_base64, log_and_exit, on_keyboard_interrupt, run_py

ENCODE_SUBS = ['encode', 'enc', 'e']
DECODE_SUBS = ['decode', 'dec', 'd']

PY_FILES = {
    'encode': 'base64_encode.py',
    'decode': 'decode.py'
}

STR_COLORED_RETURN = f'{WARNING}\u2937{RESET}'
STR_HELP = [
    'decode: Base64 hash \u2794 Unencoded string',
    f'{STR_COLORED_RETURN} Aliases: dec, d',
    f'{STR_COLORED_RETURN} Flags:',
    '   --hash: The hash to decode into a string',
    '   --nocopy or -nc: Prevents copying of decoded string',
    f'{WARNING}Base64CLI Help{RESET}',
    'encode: Unencoded string \u2794 Base64 hash',
    f'{STR_COLORED_RETURN} Aliases: enc, e',
    f'{STR_COLORED_RETURN} Flags:',
    '   --input: The string to encode into a base64 hash',
    '   --nocopy or -nc: Prevents copying of resulting hash',
    'help: Show this help message'
]


# TODO Toggle debugging from within CLI
# TODO Add pip install support
# TODO Make --help less verbose
class MainProcess:

    terminate = False

    # https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
    def parse_args(self) -> Namespace:
        parser = argparse.ArgumentParser(description='Base64CLI')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--decode', '--dec', '-d', action='store_true', help='decode base64 hash to string')
        group.add_argument('--encode', '--enc', '-e', action='store_true', help='encode input to base64 hash')
        parser.add_argument('--hash', '--input', '-i', help='input string to encode/decode', nargs='+')
        return parser.parse_args()

    def ask_method(self, inp):
        method_action_str = create_action_string('enc', 'dec', STR_QUIT_ACTION)
        resp = input(f'> Do you want to encode or decode your input "{inp}"? {method_action_str} ').lower().strip()

        if resp in CODES_EXIT:
            log_and_exit(__file__)
        elif resp in ENCODE_SUBS:
            run_py(PY_FILES['encode'], inp)
        elif resp in DECODE_SUBS:
            run_py(PY_FILES['decode'], inp)
        else:
            print(f'{DANGER}Unknown base64 method "{inp}"{RESET}')

    def handle_method_from_arg(self, args):
        should_encode = args.encode
        should_decode = args.decode
        direct_input = None if args.hash is None else ' '.join(args.hash)

        if should_encode and should_decode:
            dprint('Unable to encode and decode at the same time, defaulting to encoding for this session')
            should_decode = False

        if should_encode:
            if direct_input is None:
                run_py(PY_FILES['encode'])
            else:
                run_py(PY_FILES['encode'], '-i', direct_input)
            self.terminate = True
        elif should_decode:
            if direct_input is None:
                run_py(PY_FILES['decode'])
            else:
                run_py(PY_FILES['decode'], '-i', direct_input)
            self.terminate = True

    def handle_alternative_input(self, inp):
        if not is_base64(inp):
            self.terminate = True
            run_py(PY_FILES['encode'], '-i', inp)
            return True

        dprint('Automatically detected a base64 hash as input, asking user...')

        action_str = create_action_string('y', 'n')
        input_truncated = inp if len(inp) <= 24 else f'{inp[:24]}...'
        prompt = f'Found potential base64 hash "{input_truncated}", would you like to decode it? {action_str}'
        proceed = input(f'> {prompt} ')

        if proceed.lower().strip() in ['y', 'yes', 'proceed', 'continue']:
            dprint('User approved decoding of auto-detected hash, passing on...')
            run_py(PY_FILES['decode'], '-i', inp)
            self.terminate = True
        else:
            dprint('User aborted decoding of auto-detected hash, continuing...')

    def main(self):
        args = self.parse_args()
        self.handle_method_from_arg(args)

        try:
            while not self.terminate:
                prompt = f'[Base64CLI] Do you need to encode or decode for base64? {create_action_string("enc", "dec")}'
                prompt += ' '
                user_input = input(prompt).strip()
                input_lower = user_input.lower()

                if input_lower in CODES_EXIT:
                    self.terminate = True
                    log_and_exit(__file__)
                elif input_lower in CODES_HELP:
                    for line in STR_HELP:
                        print(line)
                    continue
                elif input_lower in ENCODE_SUBS:
                    self.terminate = True
                    run_py(PY_FILES['encode'])
                    break
                elif input_lower in DECODE_SUBS:
                    self.terminate = True
                    run_py(PY_FILES['decode'])
                    break
                else:
                    self.handle_alternative_input(user_input)
        except KeyboardInterrupt:
            on_keyboard_interrupt(__file__)


if __name__ == '__main__':
    process = MainProcess()
    process.main()
