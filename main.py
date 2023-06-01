from _constants import DANGER, EXIT_CODES, RESET, QUIT_ACTION_STR
from _functions import create_action_string, log_and_exit, run_py
from subprocess import run
from sys import argv

ENCODE_SUBS = ['encode', 'enc', 'e']
DECODE_SUBS = ['decode', 'dec', 'd']

ENCODE_FLAGS = ['--encode', '-e']
DECODE_FLAGS = ['--decode', '-d']


def ask_method(inp):
    action_str = create_action_string('enc', 'dec', QUIT_ACTION_STR)
    resp = input(f'> Do you want to encode or decode your input "{inp}"? {action_str} ').lower()

    if resp in EXIT_CODES:
        log_and_exit(__file__)

    if resp in ENCODE_SUBS:
        run(['python', 'base64_encode.py', inp])
    elif resp in DECODE_SUBS:
        run(['python', 'base64_decode.py', inp])
    else:
        print(f'{DANGER}Unknown base64 method "{inp}"{RESET}')


# TODO Command help
# TODO Bard recommends using argparse to simplify the method specification
# TODO Comments throughout, especially _constants & _functions

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
        input_compare = input_method.lower()
        # Preserve the capital letters of the user input

        if input_compare in EXIT_CODES:
            terminate = True
            log_and_exit(__file__)
            continue

        if should_encode or input_compare in ENCODE_SUBS:
            run_py('base64_encode.py')
            terminate = True
        elif should_decode or input_compare in DECODE_SUBS:
            run_py('base64_decode.py')
            terminate = True
        else:
            # Try to salvage their input by asking them which method they would like to input their string to
            ask_method(input_method)
except KeyboardInterrupt:
    print()
    log_and_exit(__file__)
