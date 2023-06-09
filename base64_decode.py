from binascii import Error
from sys import argv

from pybase64 import b64decode
from pyperclip import copy

from _constants import CODES_EXIT, CODES_RETURN, DANGER, RESET, STR_QUIT_ACTION, SUCCESS, WARNING
from _functions import create_action_string, dprint, is_base64, is_debugging, log_and_exit, match_and_get_urls
from _functions import match_and_replace_urls, on_keyboard_interrupt, return_to_main, run_py, sanitize_output


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


b64 = str()
decoded = str()
terminate = False

if len(argv) > 1:
    b64 = argv[1]

# For graceful exit on KeyboardInterrupt
try:
    while not terminate:
        if b64 == '':
            b64 = input(f'> Enter your base64 hash ({STR_QUIT_ACTION}): ').strip()
        else:
            dprint(f'Decoding hash "{b64}" supplied as command-line argument')

        if b64.lower() in CODES_EXIT:
            run_py('main.py')
            # In this context, an exit code should return to main.py
            break

        try:
            no_copy = False

            if b64.endswith(' --nocopy' or b64.endswith(' -nc')):
                no_copy = True
                b64 = b64.removesuffix(' --nocopy')
                b64 = b64.removesuffix(' -nc')

            decoded = b64decode(b64, validate=True)
            decoded_str = decoded.decode('utf-8').strip()

            # Returns bytes, needs to be decoded when displayed
            display_and_copy(decoded_str, no_copy)

            action_str = create_action_string('y', 'n', 'return', STR_QUIT_ACTION)
            another = input(f'> Do you have another hash to decode? {action_str} ')
            another_compare = another.lower().strip()

            if is_base64(another):
                b64 = another
                continue

            if another_compare in CODES_RETURN:
                return_to_main()
                break
            elif another_compare == 'y' or another_compare == 'yes':
                continue

            terminate = True
            # User has inputted all hashes they wished to decode for the session
        except Error:
            if len(b64) > 64:
                b64 = f'{b64[:64]}...'
                # Truncate length of invalid base64 hash for clean console

            print(f'{DANGER}Invalid base64 hash "{b64}"{RESET}')
            b64 = str()
            # Program repeats because terminate != False
        except UnicodeDecodeError:
            print(f'{DANGER}Failed to decode hash "{b64}" with UTF-8!{RESET}')
            b64 = str()
except KeyboardInterrupt:
    on_keyboard_interrupt(__file__)

log_and_exit(__file__)
