import argparse

from _constants import DANGER, CODES_EXIT, CODES_HELP, STR_QUIT_ACTION, RESET, WARNING
from _functions import create_action_string, dprint, is_base64, log_and_exit, on_keyboard_interrupt, run_py

ENCODE_SUBS = ['encode', 'enc', 'e']
DECODE_SUBS = ['decode', 'dec', 'd']

PY_FILES = {
    'encode': 'base64_encode.py',
    'decode': 'base64_decode.py'
}

STR_COLORED_RETURN = f'{WARNING}\u2937{RESET}'
STR_HELP = [
    f'{WARNING}Base64CLI Help{RESET}',
    'encode: Unencoded string \u2794 Base64 hash',
    f'{STR_COLORED_RETURN} Aliases: enc, e',
    f'{STR_COLORED_RETURN} Flags:',
    '   --input: The string to encode into a base64 hash',
    '   --nocopy or -nc: Prevents copying of resulting hash',
    'decode: Base64 hash \u2794 Unencoded string',
    f'{STR_COLORED_RETURN} Aliases: dec, d',
    f'{STR_COLORED_RETURN} Flags:',
    '   --hash: The hash to decode into a string',
    '   --nocopy or -nc: Prevents copying of decoded string'
]


def ask_method(inp):
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


def print_help():
    for line in STR_HELP:
        print(line)


# TODO Toggle debugging from within CLI
# TODO Assess cognitive complexity of each method
# TODO Add pip install support
# TODO Support --input flag from this file
# https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3

parser = argparse.ArgumentParser(description='Base64CLI')
group = parser.add_mutually_exclusive_group()
group.add_argument('--encode', '--enc', '-e', action='store_true', help='Encode input to base64 hash')
group.add_argument('--decode', '--dec', '-d', action='store_true', help='Decode base64 hash to string')
args = parser.parse_args()

should_encode = args.encode
should_decode = args.decode
terminate = False

if should_encode:
    run_py(PY_FILES['encode'])
    terminate = True
elif should_decode:
    run_py(PY_FILES['decode'])
    terminate = True

try:
    while not terminate:
        prompt = f'[Base64CLI] Do you need to encode or decode for base64? {create_action_string("enc", "dec")} '
        # Somewhat confusing varname, this is just the user input for the main python process. It could be an action,
        #  an exit code, a help code, or otherwise it is either an encoded or a string to be encoded.
        user_input = input(prompt).strip()
        # Preserve the capital letters of the user input

        if user_input.lower() in CODES_EXIT:
            terminate = True
            log_and_exit(__file__)
            break
        elif user_input.lower() in CODES_HELP:
            print_help()
        elif user_input.lower() in ENCODE_SUBS:
            terminate = True
            run_py(PY_FILES['encode'])
            break
        elif user_input.lower() in DECODE_SUBS:
            terminate = True
            run_py(PY_FILES['decode'])
            break
        else:
            if not is_base64(user_input):
                run_py(PY_FILES['encode'], '--input', user_input)

            dprint('Automatically detected a base64 hash as input, asking user...')

            action_str = create_action_string('y', 'n')
            input_truncated = user_input if len(user_input.lower()) <= 24 else f'{user_input[:24]}...'
            prompt = f'Found potential base64 hash "{input_truncated}", would you like to decode it? {action_str}'
            proceed = input(f'> {prompt} ')

            if proceed.lower().strip() in ['y', 'yes', 'proceed', 'continue']:
                dprint('User approved decoding of auto-detected hash, passing on...')
                run_py(PY_FILES['decode'], '--hash', user_input)
            else:
                dprint('User aborted decoding of auto-detected hash, continuing...')
                continue

            break
except KeyboardInterrupt:
    on_keyboard_interrupt(__file__)
