import binascii
import os
import re
from re import Pattern
from subprocess import run

import base64
from dotenv import load_dotenv

from _constants import ACTION, LINK, RESET, WARNING

load_dotenv()


def beautify_filename(filename: str) -> str:
    # Ex: base64_encode.py -> Base64 Encode
    beautiful = os.path.basename(filename).replace('.py', '')
    split = beautiful.split('_')
    beautiful = ''
    for s in split:
        beautiful += f'{s.capitalize()} '
    beautiful = beautiful.strip()

    return beautiful


def create_action_string(*actions, colored=True, entry_prefix=f'{ACTION}', delimiter='/', last_use_or=True,
                         prefix='(', suffix=')'):
    """
    Constructs a string which represents actions made available to the user.
    :param   actions: A list of strings which will be interspersed into the generated action string.
    :param   colored: Whether to add color to the formatting of the generated string.
    :param   entry_prefix: What should be prepended to each action entry in the string. Default is a color prefix.
    :param   delimiter: What should delimit each action entry in the string. Default is an uncolored forward slash.
    :param   last_use_or: Whether the last element of the action set, in sets of 3 or more should use the word or
               instead of a trailing comma.
    :param   prefix: What should be prepended to the entire action string to indicate its beginning. Default is an
               uncolored opening parentheses.
    :param   suffix: What should be appended to the entire action string to indicate its end. Default is an
               uncolored closing parentheses.
    :return: The formatted string generated by this method. Ex: (action1, action2 or action3) etc.
    """
    str_builder = f'{prefix}'
    length = len(actions)

    for i in range(length):
        if colored:
            str_builder += f'{entry_prefix}{actions[i]}{RESET}'
        else:
            str_builder += f'{actions[i]}'

        if length > 2 and i == length - 2 and last_use_or:
            str_builder += ' or '
            continue

        if i < (length - 1):
            str_builder += f'{delimiter}'

    str_builder += f'{RESET}{suffix}'

    return str_builder


def sanitize_output(output, prefix='- ', replace_newlines_with_prefix=True):
    """
    Sanitizes strings of double linebreaks
    :param output: The string to sanitize.
    :param prefix: What each entry in a
    multi-line output should be prepended with if replace_newlines_with_prefix is True.
    :param replace_newlines_with_prefix: Whether newlines should be replaced with the prefix provided by the function's
    prefix parameter.
    :return: A two-value tuple where the first value is the sanitized string and the second is a
    bool representing if any linebreaks were found, and thus if the command line should be open to automatic copying
    to system clipboard.
    """
    copyable = True
    display = output

    # Replace double linebreaks with single linebreaks
    if '\n\n' in display:
        output = output.replace('\n\n', '\n')

    if '\n' in display:
        if replace_newlines_with_prefix:
            output = f'{prefix}{output}'
            output = output.replace('\n', f'\n{prefix}')

        output = f'\n{output}{RESET}\n'
        copyable = False
    else:
        output = display

    return output, copyable


def dprint(string, prefix=f'[{WARNING}Debug{RESET}] ', should_prefix=True):
    """
    Print a debug message with the prefix '[Debug] ' if DEBUG is enabled in the environment.
    :param string: The string to be logged if debugging is active.
    :param prefix: The prefix to be prepended if should_prefix is True.
    :param should_prefix: Whether the prefix supplied by the function should be prepended to the string before printing.
    """
    if not is_debugging():
        return

    if should_prefix:
        string = f'{prefix}{string}'
    print(string)


def is_debugging():
    """
    Checks if debugging is active in the environment. Specifically checks if Debug==True in the environment (Def: .env)
    :return: Whether debugging is active in the environment.
    """
    return bool(str.lower(os.getenv('DEBUG', 'False')))


def is_base64(string):
    """
    Checks if the supplied string is a potential base64 hash.
    :param string: The string to check.
    :return: Whether the string is a base64 hash.
    """
    # Check if the string has a length divisible by 4
    if len(string) % 4 != 0:
        return False

    # Check if the string is a valid base64 string
    try:
        # Decode the string and encode it back to compare against the original
        return base64.b64encode(base64.b64decode(string)) == string.encode()
    except binascii.Error:
        return False


def is_valid_url(url):
    """
    Checks if the supplied URL is a valid URL,
      meaning if it matches the pattern supplied by #compile_url_regex_pattern()
    :param url: The URL to validate by the fixed pattern.
    :return: Whether the URL supplied is a valid one.
    """
    if not isinstance(url, str):
        raise TypeError('url must be a string')
    pattern = compile_url_regex_pattern()
    return pattern.match(url) is not None


def get_python_cmd():
    """
    Checks what the python command is within the environment. Default: "python", others could include "python3", etc.
      Set within the .env file under key "PYTHON_CMD" (see .env.example)
    :return: The results of getenv('PYTHON_CMD'), deferring to default "python" if variable is unavailable.
    """
    return os.getenv('PYTHON_CMD', 'python')


def log_and_exit(filename, exitcode=0, should_beautify=True, thankful=True, color_prefix=f'{WARNING}'):
    """
    Prints a nice exit message including the supplied filename then executes an exit code.
    :param color_prefix: The color prefix to be placed before the filename. Default: f'{WARNING}'
    :param exitcode: The exit code to use when exiting the program. Default 0 (success.)
    :param filename: Usually passed __file__ within the scope it is employed.
    :param should_beautify: Whether to apply beautify_filename to the provided filename.
    :param thankful: Whether to append a small thank you to the message. Default True.
    :return:
    """
    if not isinstance(filename, str):
        raise TypeError('filename must be a string')

    filename = beautify_filename(filename) if should_beautify else os.path.basename(filename)
    if filename == 'Main':
        filename = 'Base64CLI'
        thankful = False
    exit_msg = f'[Base64CLI] Exiting {color_prefix}{filename}{RESET}...'
    if thankful:
        exit_msg += ' Thank you for using Base64CLI \u263A'
    print(exit_msg)
    exit(exitcode)


# Inspection disabled because this is the only pattern which would succeed with our data sets
# noinspection RegExpUnnecessaryNonCapturingGroup
def compile_url_regex_pattern() -> Pattern:
    """
    Regex pattern for matching with whole URLs, including the subdirectories and trailing slashes. Thanks ChatGPT!
    :return: The compiled regex Pattern.
    """
    return re.compile(r'(https?://[^/]+\b(?:/.*?))(?=\s|\)|$)')


def match_and_get_urls(string):
    """
    Grabs all URLs contained in the string and assembles them in an array.
    :param string: The string to check.
    :return: The array of URLs as strings, or None is no URLs were found.
    """
    urls = []

    for match in compile_url_regex_pattern().findall(string):
        urls.append(match)

    if len(urls) == 0:
        return None

    return urls


def match_and_replace_urls(string):
    """
    Substitutes all URLs in a string with themselves prepended with the LINK color constant (console blue.)
    :param string: The string to replace URLs within.
    :return: The string with the URLs color-coded for console output.
    """
    matches = compile_url_regex_pattern().finditer(string)

    if matches is not None:
        for match in matches:
            domain = match.group(1)
            string = string.replace(match.group(), f'{LINK}{domain}{RESET}')

    return string


def on_keyboard_interrupt(filename, should_dprint=True, should_newline=True):
    """
    Handles the graceful exiting on KeyboardInterrupt.
    :param filename: Usually __file__ passed from the scope this is called in.
    :param should_dprint: Whether a debug print should be sent with the keyboard interrupt handling.
    :param should_newline: Whether a newline print should be sent before the keyboard interrupt handling.
    """
    if should_newline:
        print()
    if is_debugging() and should_dprint:
        debug_str = f'{WARNING}KeyboardInterrupt detected! ' \
                    f'Users can gracefully exit the program by entering "Q" on input.{RESET}'
        dprint(debug_str)
    log_and_exit(filename)


def return_to_main(should_newline=True):
    """
    Prints a newline and runs main.py to return to the application's super menu.
    :param should_newline: Whether a newline print should be sent before returning to main.
    """
    if should_newline:
        print()
    run_py('main.py')
    exit()


def run_py(pyfile, *append):
    """
    Runs a python script by substituting the environment's PYTHON_CMD for the path executable and appending the
    pyfile to it :param pyfile: The Python script to execute
    """
    if not isinstance(pyfile, str):
        raise TypeError('pyfile must be a string')
    if not pyfile.endswith('.py'):
        pyfile += '.py'

    py_command = os.getenv('PYTHON_CMD', 'python')
    run_contents = [py_command, pyfile]

    if append is not None:
        for a in append:
            run_contents.append(a)

    run(run_contents)
