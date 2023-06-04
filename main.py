from subprocess import run
from sys import argv

from _constants import DANGER, CODES_EXIT, CODES_HELP, STR_QUIT_ACTION, RESET, WARNING
from _functions import create_action_string, get_python_cmd, log_and_exit, on_keyboard_interrupt, run_py

ENCODE_SUBS = ['encode', 'enc', 'e']
DECODE_SUBS = ['decode', 'dec', 'd']

ENCODE_FLAGS = ['--encode', '-e']
DECODE_FLAGS = ['--decode', '-d']

STR_COLORED_RETURN = f'{WARNING}\u2937{RESET}'
STR_HELP = [
    f'{WARNING}Base64CLI Help{RESET}',
    'encode: Unencoded string \u2794 Base64 hash',
    f'{STR_COLORED_RETURN} Aliases: enc, e',
    f'{STR_COLORED_RETURN} Flags:',
    '   --nocopy or -nc: Prevents copying of resulting hash',
    'decode: Base64 hash \u2794 Unencoded string',
    f'{STR_COLORED_RETURN} Aliases: dec, d',
    f'{STR_COLORED_RETURN} Flags:',
    '   --nocopy or -nc: Prevents copying of decoded string'
]


def ask_method(inp):
    action_str = create_action_string('enc', 'dec', STR_QUIT_ACTION)
    resp = input(f'> Do you want to encode or decode your input "{inp}"? {action_str} ').lower().strip()

    if resp in CODES_EXIT:
        log_and_exit(__file__)
    elif resp in ENCODE_SUBS:
        run([get_python_cmd(), 'base64_encode.py', inp])
    elif resp in DECODE_SUBS:
        run([get_python_cmd(), 'base64_decode.py', inp])
    else:
        print(f'{DANGER}Unknown base64 method "{inp}"{RESET}')


def print_help():
    for line in STR_HELP:
        print(line)


# TODO Greater command help
# TODO Tab completion
# TODO Check if base64 hash detected, ask if they want to decode it

should_encode = False
should_decode = False

if len(argv) > 1:
    for a in argv:
        if a.lower() in ENCODE_FLAGS: should_encode = True
        elif a.lower() in DECODE_FLAGS: should_decode = True

terminate = False

try:
    while not terminate:
        prompt = f'[Base64CLI] Do you need to encode or decode for base64? {create_action_string("enc", "dec")} '
        input_method = input(prompt)
        input_compare = input_method.lower().strip()
        # Preserve the capital letters of the user input

        if input_compare in CODES_EXIT:
            terminate = True
            log_and_exit(__file__)
            continue
        elif input_compare in CODES_HELP:
            print_help()
        elif should_encode or input_compare in ENCODE_SUBS:
            run_py('base64_encode.py')
            terminate = True
        elif should_decode or input_compare in DECODE_SUBS:
            run_py('base64_decode.py')
            terminate = True
        else:
            # Try to salvage their input by asking them which method they would like to input their string to
            ask_method(input_method)
except KeyboardInterrupt:
    on_keyboard_interrupt(__file__)
