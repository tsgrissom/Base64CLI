from _constants import DANGER, CODES_EXIT, STR_QUIT_ACTION, RESET
from _functions import create_action_string, get_python_cmd, log_and_exit, on_keyboard_interrupt, run_py
from subprocess import run
from sys import argv

ENCODE_SUBS = ['encode', 'enc', 'e']
DECODE_SUBS = ['decode', 'dec', 'd']

ENCODE_FLAGS = ['--encode', '-e']
DECODE_FLAGS = ['--decode', '-d']


def ask_method(inp):
    action_str = create_action_string('enc', 'dec', STR_QUIT_ACTION)
    resp = input(f'> Do you want to encode or decode your input "{inp}"? {action_str} ').lower()

    if resp in CODES_EXIT:
        log_and_exit(__file__)

    if resp in ENCODE_SUBS:
        run([get_python_cmd(), 'base64_encode.py', inp])
    elif resp in DECODE_SUBS:
        run([get_python_cmd(), 'base64_decode.py', inp])
    else:
        print(f'{DANGER}Unknown base64 method "{inp}"{RESET}')


# TODO Command help
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

        if input_compare in CODES_EXIT:
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
    on_keyboard_interrupt(__file__)
