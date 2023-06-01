from _constants import ACTION, LINK, RESET, WARNING
from dotenv import load_dotenv
from os import path, getenv
import re
from re import Pattern
from subprocess import run

load_dotenv()


def create_action_string(*actions, last_use_or=True):
    str_builder = '('
    length = len(actions)

    for i in range(length):
        str_builder += f'{ACTION}{actions[i]}{RESET}'

        if length > 2 and i == length - 2 and last_use_or:
            str_builder += ' or '
            continue

        if i < (length - 1):
            str_builder += '/'

    str_builder += f'{RESET})'

    return str_builder


# TODO Reconsider how this is set up
def sanitize_output(output):
    copyable = True
    display = output
    if "\n" in output:
        output = output.replace('\n\n', '\n')
        display = f'\n{output}{RESET}\n'
        copyable = False
    return display, copyable


def dprint(string):
    if is_debugging():
        print(f'[Debug] {string}')


# TODO Use this
def equals_any(compare, *to, ignore_case=True):
    """
    Returns True if the `compare` value is equal to any of the `to` values, False otherwise.
    :param compare: The value to compare.
    :param to: A list of values to compare against.
    :param ignore_case: Whether to ignore case when comparing values.
    :return: Whether `compare` equals any of the `to` values, False otherwise.
    """
    if not isinstance(compare, str):
        raise TypeError('compare must be a string.')
    if not isinstance(ignore_case, bool):
        raise TypeError('ignore_case must be a boolean value.')

    if len(to) == 0:
        if len(compare) == 0:
            return True
        else:
            return False

    for t in to:
        if ignore_case:
            compare = str(compare).lower()
            t = t.lower()
        if compare == t:
            return True
    return False


def is_debugging():
    return bool(str.lower(getenv("DEBUG", "False")))


def is_valid_url(url):
    pattern = compile_url_regex_pattern()
    return pattern.match(url) is not None


def get_python_cmd():
    return getenv('PYTHON_CMD', 'python')


def log_and_exit(filename, exitcode=0, thankful=True):
    exit_msg = f'[Base64CLI] Exiting {WARNING}{path.basename(filename)}{RESET}...'
    if thankful:
        exit_msg += f" Thank you for using Base64CLI \u263A"
    print(exit_msg)
    exit(exitcode)


# noinspection RegExpUnnecessaryNonCapturingGroup
def compile_url_regex_pattern() -> Pattern:
    return re.compile(r'(https?://[^/]+\b(?:/.*?))(?=\s|\)|$)')


def match_and_get_urls(string):
    urls = []

    for match in compile_url_regex_pattern().findall(string):
        urls.append(match)

    if len(urls) == 0:
        return None

    return urls


def match_and_replace_urls(string):
    matches = compile_url_regex_pattern().finditer(string)

    if matches is not None:
        for match in matches:
            domain = match.group(1)
            string = string.replace(match.group(), f'{LINK}{domain}{RESET}')

    return string


def return_to_main():
    print('')
    run_py('main.py')
    exit()


def run_py(pyfile):
    if not pyfile.endswith('.py'):
        pyfile += '.py'
    run([getenv('PYTHON_CMD', 'python'), pyfile])
