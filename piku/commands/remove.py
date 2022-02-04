import os
from piku.core import config, modules, utils


def remove_command(args):
    module = args.module.lower()

    # remove module from pyproject.toml
    if not config.remove(f'tool.piku.dependencies.{module}'):
        print(f'Unable to find matching module {module} in pyproject.toml')
        suggestions = utils.similar(module, config.get('tool.piku.dependencies').keys())
        if suggestions:
            print('Did you mean')
            for suggestion in suggestions:
                print(f' * {suggestion}')
        return

    # remove file from library
    if not modules.remove(module):
        print(f'Warning: Unable to find and delete matching file in source for module {module} in project')
