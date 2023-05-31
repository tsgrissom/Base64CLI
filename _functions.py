from _constants import ACTION, DANGER, RESET
from os import path
from subprocess import run


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


def log_and_exit(filename):
    print(f'{DANGER}Exiting {path.basename(filename)}{RESET}')
    exit(0)


def return_to_main():
    print('')
    run_py('main.py')


def run_py(pyfile):
    if not pyfile.endswith('.py'):
        pyfile += '.py'
    run(['python', pyfile])
