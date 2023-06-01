from re import Pattern

from _constants import ACTION, LINK, RESET, WARNING
from dotenv import load_dotenv
from os import path, getenv
import re
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


def sanitize_output(output):
    copyable = True
    display = output
    if "\n" in output:
        output = output.replace('\n\n', '\n')
        display = f'\n{output}{RESET}\n'
        copyable = False
    return display, copyable


# TODO Use this
def equals_any(compare, *to):
    for t in to:
        if str(compare).lower() == t: return True
    return False


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

    print(urls)
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
